import os
import pickle
import numpy as np 
from deepface import DeepFace


male_list = [
    "virat_kohli"
]

female_list = [
    "Aishwarya_Rai"
]

print(f"[INFO] Starting to encode all {len(male_list) + len(female_list)} celebrities...")


album_dirs = ["./dataset"]

model_name = "ArcFace"
all_master_encodings = [] 

for celebrity_dir in album_dirs:
    print(f"[INFO] Processing album: {celebrity_dir}")
    if not os.path.exists(celebrity_dir):
        print(f"[WARN] Directory not found, skipping: {celebrity_dir}")
        continue

  
    for person_name in os.listdir(celebrity_dir):
        person_dir = os.path.join(celebrity_dir, person_name)
        
        if not os.path.isdir(person_dir):
            continue

    
        check_name_underscores = person_name.replace(" ", "_")
        check_name_clean = person_name.replace("_", " ").replace("ΓÇÖ", "'").title()

        gender = "Unknown"
       
        if person_name in male_list or check_name_underscores in male_list or check_name_clean in male_list:
            gender = "Man"
        elif person_name in female_list or check_name_underscores in female_list or check_name_clean in female_list:
            gender = "Woman"
        
        if gender == "Unknown":
            print(f"  [WARN] Skipping {person_name}: Not in gender lists. (Check spelling?)")
            continue
            
        print(f"  [INFO] Processing: {person_name} (Gender: {gender})")
        
       
        person_embeddings = []
        
        # Now we loop through all their photos
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            
            if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            try:
                # Get the "fingerprint" for this single photo
                embedding_obj = DeepFace.represent(
                    img_path=image_path, 
                    model_name=model_name,
                    enforce_detection=True
                )
                # Add the fingerprint to our person's list
                person_embeddings.append(embedding_obj[0]["embedding"])
                
            except Exception as e:
                # This just skips a blurry/bad photo
                print(f"    [SKIP] Could not process '{image_path}': {e}")

      
        if len(person_embeddings) > 0:
            # This is the magic line.
            # np.mean averages all the lists together into one "master" list.
            master_embedding = np.mean(person_embeddings, axis=0)
            
            # Save the ONE master fingerprint
            all_master_encodings.append({
                "name": check_name_clean, # Save the clean name
                "embedding": master_embedding,
                "gender": gender
            })
            print(f"    [OK] Created master fingerprint for {person_name} from {len(person_embeddings)} photos.")
        else:
            print(f"    [FAIL] No valid photos found for {person_name}, skipping.")
            
# --- END OF NEW LOGIC ---

# --- Save to your final "cheat sheet" file ---
output_file = "deepface_encodings_PROTOTYPE.pickle"
print(f"\n[INFO] Serializing {len(all_master_encodings)} total master encodings...")
with open(output_file, "wb") as f:
    f.write(pickle.dumps(all_master_encodings))

print(f"[INFO] All faces encoded and saved to '{output_file}'")