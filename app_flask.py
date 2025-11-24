
from flask import Flask, render_template, request, jsonify, send_from_directory
from deepface import DeepFace
from scipy.spatial.distance import cosine
import os
import pickle
import cv2
import numpy as np
import base64
from datetime import datetime
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['SECRET_KEY'] = 'celebrity-lookalike-secret-key-2024'

# Global state
SIMILARITY_THRESHOLD = 30.0
database = []
celebrity_images = {}
leaderboard = []

def load_database():
    """Load pre-encoded celebrity embeddings once at startup"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pickle_path = os.path.join(script_dir, "deepface_encodings_PROTOTYPE.pickle")
    
    logger.info(f"Loading database from: {pickle_path}")
    try:
        with open(pickle_path, "rb") as f:
            data = pickle.load(f)
        logger.info(f"✓ Loaded {len(data)} celebrity encodings")
        return data
    except Exception as e:
        logger.error(f"✗ Error loading database: {e}")
        return []

def preload_celebrity_images():
    """Load all celebrity images into memory for instant access"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    album_dir = os.path.join(script_dir, "dataset")
    
    celeb_imgs = {}
    
    if not os.path.exists(album_dir):
        logger.error(f"Dataset folder not found: {album_dir}")
        return celeb_imgs
    
    logger.info(f"Preloading celebrity images from: {album_dir}")
    
    for celeb_folder in os.listdir(album_dir):
        celeb_path = os.path.join(album_dir, celeb_folder)
        
        if os.path.isdir(celeb_path):
            for img_file in os.listdir(celeb_path):
                if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(celeb_path, img_file)
                    try:
                        img = cv2.imread(img_path)
                        if img is not None:
                            display_name = celeb_folder.replace("_", " ").replace("'", "'").title()
                            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            celeb_imgs[display_name] = img_rgb
                            logger.info(f"  ✓ Loaded: {display_name}")
                            break
                    except Exception as e:
                        logger.error(f"  ✗ Error loading {celeb_folder}: {e}")
                        continue
    
    logger.info(f"✓ Preloaded {len(celeb_imgs)} celebrity images")
    return celeb_imgs

def resize_image(image, target_height=400):
    """Resize image maintaining aspect ratio"""
    if image is None:
        return None
    
    h, w = image.shape[:2]
    aspect_ratio = w / h
    new_width = int(target_height * aspect_ratio)
    
    resized = cv2.resize(image, (new_width, target_height), interpolation=cv2.INTER_LINEAR)
    
    if new_width > target_height * 1.3:
        start_x = (new_width - target_height) // 2
        resized = resized[:, start_x:start_x + target_height]
    
    return resized

def image_to_base64(image):
    """Convert numpy image to base64 string"""
    _, buffer = cv2.imencode('.jpg', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    return base64.b64encode(buffer).decode('utf-8')

# Initialize at startup
logger.info("=" * 60)
logger.info("INITIALIZING CELEBRITY LOOK-ALIKE FINDER")
logger.info("=" * 60)
database = load_database()
celebrity_images = preload_celebrity_images()
logger.info("=" * 60)
logger.info("✓ APPLICATION READY FOR PRODUCTION")
logger.info("=" * 60)

@app.route('/')
def index():
    """Serve main application page"""
    return render_template('index.html', 
                         total_celebs=len(database),
                         threshold=SIMILARITY_THRESHOLD)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded image and find celebrity match with AUTO-GENDER FILTER"""
    try:
        # Get image from request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        # Read image
        file_bytes = np.frombuffer(file.read(), np.uint8)
        user_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if user_image is None:
            return jsonify({'error': 'Invalid image file'}), 400
        
        # --- STEP 1: DETECT GENDER AUTOMATICALLY ---
        detected_gender = "All"
        try:
            analysis_results = DeepFace.analyze(
                img_path=user_image,
                actions=['gender'],
                enforce_detection=True,
                detector_backend='opencv'
            )
            # DeepFace returns a list for each face found. Take the first one.
            detected_gender = analysis_results[0]['dominant_gender']  # Returns "Man" or "Woman"
            logger.info(f"Detected Gender: {detected_gender}")
            
        except Exception as e:
            logger.error(f"Gender detection failed: {e}")
            # Fallback: If detection fails, search everyone
            detected_gender = "All"

        # --- STEP 2: FILTER DATABASE BY DETECTED GENDER ---
        known_names = []
        known_embeddings = []
        
        for data in database:
            # Match celebrities with detected gender
            if detected_gender == "All" or data.get("gender") == detected_gender:
                known_names.append(data["name"])
                known_embeddings.append(data["embedding"])
        
        if len(known_names) == 0:
            return jsonify({'error': f'No celebrities found for detected gender: {detected_gender}'}), 400

        # --- STEP 3: CREATE EMBEDDING (ArcFace) ---
        try:
            face_obj = DeepFace.represent(
                img_path=user_image,
                model_name="ArcFace",
                enforce_detection=True,
                detector_backend='opencv'
            )
            
            if not face_obj or len(face_obj) == 0:
                return jsonify({'error': 'No face detected in the image. Please ensure your face is clearly visible.'}), 400
                
            user_embedding = face_obj[0]["embedding"]
            
        except ValueError as ve:
            logger.error(f"Face detection failed: {ve}")
            return jsonify({'error': 'No face detected in the image. Please ensure your face is clearly visible, well-lit, and facing the camera.'}), 400

        # --- STEP 4: FIND BEST MATCH ---
        distances = [cosine(user_embedding, celeb_embedding) 
                    for celeb_embedding in known_embeddings]
        
        best_match_index = int(np.argmin(distances))
        best_match_name = known_names[best_match_index]
        
        # Get the raw ArcFace score (usually 0.2 to 0.8 for matches)
        raw_similarity = 1 - distances[best_match_index]
        
        # "Gamify" the score for display
        # Map the range [0.30, 0.80] to [50%, 98%] for better presentation
        if raw_similarity > 0.30:
            display_score = min(99.0, (raw_similarity * 100) + 20)
        else:
            display_score = raw_similarity * 100
        
        similarity_percent = float(display_score)
        
        # Add to leaderboard
        leaderboard.append({
            'name': best_match_name,
            'score': float(similarity_percent),
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        
        # Prepare response
        response = {
            'success': True,
            'match_name': best_match_name,
            'similarity': round(similarity_percent, 1),
            'detected_gender': detected_gender,
            'meets_threshold': similarity_percent >= SIMILARITY_THRESHOLD
        }
        
        # Process images for display
        user_image_rgb = cv2.cvtColor(user_image, cv2.COLOR_BGR2RGB)
        celeb_image = celebrity_images.get(best_match_name)
        
        if celeb_image is not None:
            user_resized = resize_image(user_image_rgb, 400)
            celeb_resized = resize_image(celeb_image, 400)
            
            response['user_image'] = image_to_base64(user_resized)
            response['celeb_image'] = image_to_base64(celeb_resized)
        
        # Determine match quality
        if similarity_percent >= 70:
            response['quality'] = 'EXCELLENT MATCH'
            response['color'] = '#10b981'
        elif similarity_percent >= 50:
            response['quality'] = 'GOOD MATCH'
            response['color'] = '#f59e0b'
        elif similarity_percent >= 30:
            response['quality'] = 'FAIR MATCH'
            response['color'] = '#ef4444'
        else:
            response['quality'] = 'POOR MATCH'
            response['color'] = '#6b7280'
        
        return jsonify(response)
    
    except ValueError as e:
        logger.error(f"Face detection error: {e}")
        return jsonify({'error': 'No face detected. Please ensure good lighting and face visibility.'}), 400
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Analysis error: {e}\n{error_trace}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get current leaderboard"""
    sorted_board = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:5]
    return jsonify(sorted_board)

@app.route('/leaderboard/clear', methods=['POST'])
def clear_leaderboard():
    """Clear leaderboard"""
    global leaderboard
    leaderboard = []
    return jsonify({'success': True})

if __name__ == '__main__':
    # Production-ready configuration
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
