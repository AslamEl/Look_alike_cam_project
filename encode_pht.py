import os
import pickle
import numpy as np 
from deepface import DeepFace
import cv2

def augment_image(image_path, num_variations=2):
    """Create multiple variations from 1 photo"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return [image_path]
        
        variations = []
        dir_name = os.path.dirname(image_path)
        base_name = os.path.basename(image_path)
        name_without_ext, ext = os.path.splitext(base_name)
        
        # Original path
        variations.append(image_path)
        
        if num_variations >= 2:
            # Horizontal flip (mirror)
            flipped = cv2.flip(img, 1)
            temp_flipped_path = os.path.join(dir_name, f"{name_without_ext}_flipped_temp{ext}")
            cv2.imwrite(temp_flipped_path, flipped)
            variations.append(temp_flipped_path)
        
        if num_variations >= 3:
            # Brightness increase
            bright = cv2.convertScaleAbs(img, alpha=1.2, beta=30)
            temp_bright_path = os.path.join(dir_name, f"{name_without_ext}_bright_temp{ext}")
            cv2.imwrite(temp_bright_path, bright)
            variations.append(temp_bright_path)
        
        if num_variations >= 4:
            # Brightness decrease
            dark = cv2.convertScaleAbs(img, alpha=0.8, beta=-30)
            temp_dark_path = os.path.join(dir_name, f"{name_without_ext}_dark_temp{ext}")
            cv2.imwrite(temp_dark_path, dark)
            variations.append(temp_dark_path)
        
        if num_variations >= 5:
            # Slight rotation (5 degrees)
            height, width = img.shape[:2]
            center = (width // 2, height // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, 5, 1.0)
            rotated = cv2.warpAffine(img, rotation_matrix, (width, height))
            temp_rotated_path = os.path.join(dir_name, f"{name_without_ext}_rotated_temp{ext}")
            cv2.imwrite(temp_rotated_path, rotated)
            variations.append(temp_rotated_path)
        
        return variations
    except Exception as e:
        print(f"      [WARN] Augmentation failed: {e}")
        return [image_path]  # Return original if augmentation fails

male_list = [
    "AB de Villiers", "Adam Gilchrist", "Andre Russell", "Barack Obama", 
    "Ben Stokes", "Benedict Cumberbatch", "Bill Gates", "Brett Lee", 
    "Brian Lara", "Brock Lesnar", "Chiranjeevi", "Chris Evans", 
    "Chris Gayle", "Chris Hemsworth", "Cillian Murphy", "David Warner", 
    "Donald Trump", "Dulquer Salmaan", "Dwayne Bravo", "Ed Sheeran", 
    "Elon Musk", "Faf du Plessis", "Fahadh Faasil", "Glenn Maxwell", 
    "Harry Styles", "Jacques Kallis", "Jeff Bezos", "John Cena", 
    "Keanu Reeves", "Kieron Pollard", "KL Rahul", "Lewis Hamilton", 
    "Mammootty", "Mark Zuckerberg", "Max Verstappen", "Mike Tyson", 
    "Mitchell Starc", "Mohanlal", "Muhammad Ali", "Nagarjuna", 
    "Nani actor", "Nivin Pauly", "Pat Cummins", "Prithviraj Sukumaran", 
    "Rashid Khan", "Ravindra Jadeja", "Ricky Ponting", "Roman Reigns", 
    "Ryan Gosling", "Seth Rollins", "Shikhar Dhawan", "Silambarasan", 
    "Tom Holland", "Tovino Thomas", "Vijay Sethupathi", "Vin Diesel",

    "Anura Kumara Dissanayake", "Basil Rajapaksa", "Chamal Rajapaksa", "Douglas Devananda", 
    "Dullas Alahapperuma", "Edward Jayakody", "Gotabaya Rajapaksa", "Harin Fernando", 
    "Mahinda Rajapaksa", "Mahindananda Aluthgamage", "Namal Rajapaksa", "Nimal Siripala de Silva", 
    "Prasanna Ranatunga", "Ranil Wickremesinghe", "Sajith Premadasa", "Sunil Edirisinghe", 
    "Sunil Perera", "Vasudeva Nanayakkara",

   "Ashok Pathirage", "Deshamanya Mahesh Amalean", "Dhanush", 
    "Dr.Harsha de Silva", "Krishan Balendra", "Michael Ondaatje", 
    "Prabhu Deva", "Prof. G. L. Peiris", "Prof. Malik Peiris", 
    "Randika Gunathilaka", "Shehan Karunatilaka",
    "Aamir_Khan", "Abhay_Deol", "Abhishek_Bachchan", "Aftab_Shivdasani", "Ajay_Devgn",
    "Akshay_Kumar", "Akshaye_Khanna", "Amitabh_Bachchan", "Anil_Kapoor", "Arjun_Kapoor",
    "Arjun_Rampal", "Arshad_Warsi", "Ayushmann_Khurrana", "Bobby_Deol", "Emraan_Hashmi",
    "Farhan_Akhtar", "Govinda", "Hrithik_Roshan", "Irrfan_Khan", "John_Abraham",
    "Kartik_Aaryan", "Kunal_Khemu", "Manoj_Bajpayee", "Nana_Patekar", "Naseeruddin_Shah",
    "Paresh_Rawal", "Prabhas", "R_Madhavan", "Rajkummar_Rao", "Ranbir_Kapoor",
    "Randeep_Hooda", "Ranveer_Singh", "Riteish_Deshmukh", "Saif_Ali_Khan", "Salman_Khan",
    "Sanjay_Dutt", "Shah_Rukh_Khan", "Shahid_Kapoor", "Shreyas_Talpade", "Sidharth_Malhotra",
    "Suniel_Shetty", "Sunny_Deol", "Sushant_Singh_Rajput", 
    "Tiger_Shroff", "Tusshar_Kapoor", "Uday_Chopra", "Varun_Dhawan", "Vicky_Kaushal", "Vivek_Oberoi",
    "Brad Pitt", "Denzel Washington", "Hugh Jackman", "Johnny Depp", "Leonardo DiCaprio",
    "Robert Downey Jr.", "Tom Cruise", "Tom Hanks", "Will Smith",
    "Cristiano Ronaldo", "Kobe Bryant", "ms_dhoni", "sachin_tendulkar", "virat_kohli",
    "Aravinda de Silva", "Arjuna Ranatunga", "Chaminda Vaas", "Charith Asalanka", 
    "Dhananjaya de Silva", "Dimuth Karunaratne", "Dinesh Chandimal", "Dushmantha Chameera",
    "Kumar Sangakkara", "Kusal Mendis", "Kusal Perera", "Lahiru Thirimanne", "Lasith Malinga",
    "Maheesh Theekshana", "Mahela Jayawardene", "Marvan Atapattu", "Matheesha Pathirana",
    "Muttiah Muralitharan", "Niroshan Dickwella", "Nuwan Kulasekara", "Pathum Nissanka",
    "Pramod Madushan", "Rangana Herath", "Romesh Kaluwitharana", "Sanath Jayasuriya",
    "Suranga Lakmal", "Thisara Perera", "Tillakaratne Dilshan", "Upul Tharanga",
    "Babar Azam", "Imran Khan", "Mashrafe Mortaza", "Rohit Sharma", "Shahid Afridi",
    "Shakib Al Hasan", "Shoaib Akhtar", "Tamim Iqbal", "Wasim Akram", "Yuvraj Singh",
    "Kusal Maduranga", "Raveen Kanishka", "Saranga Disasekara", "Uddika Premarathna"
]

female_list = [

    "Chandrika Kumaratunga", "Pabitra Wanniarachchi",

   "Alka Yagnik", "Anoka Abeyrathne", "Asha de Vos", 
    "Chandralekha Perera", "Chathurika Peiris", "Dilhani Ekanayake", 
    "Iranganie Serasinghe", "Kasturi Chellaraja Wilson", "Linda Speldewinde", 
    "Nanda Malini", "Nayanathara", "Pooja Umashankar", 
    "Radhika Coomaraswamy", "Raini Charuka", "Samitha Mudunkotuwa", 
    "Sandani Fernando", "Sangeetha Weeraratne", "Shreya Ghoshal", 
    "Sonali Bendre", "Sridevi", "Sunidhi Chauhan", "Umaria Sinhawansa",
    "Aishwarya_Rai", "Alia_Bhatt", "Ameesha_Patel", "Amrita_Rao", "Amy_Jackson",
    "Anushka_Sharma", "Anushka_Shetty", "Asin", "Bhumi_Pednekar", "Bipasha_Basu",
    "Deepika_Padukone", "Disha_Patani", "Esha_Gupta", "Huma_Qureshi", 
    "Jacqueline_Fernandez", "Juhi_Chawla", "Kajal_Aggarwal", "Kajol", "Kangana_Ranaut",
    "Kareena_Kapoor", "Karisma_Kapoor", "Katrina_Kaif", "Kiara_Advani", "Kriti_Kharbanda",
    "Kriti_Sanon", "Lara_Dutta", "Madhuri_Dixit", "Mrunal_Thakur", "Nargis_Fakhri",
    "Nushrat_Bharucha", "Parineeti_Chopra", "Pooja_Hegde", "Prachi_Desai", "Preity_Zinta",
    "Priyanka_Chopra", "Rani_Mukerji", "Richa_Chadda", "Sara_Ali_Khan", "Shilpa_Shetty",
    "Shraddha_Kapoor", "Shruti_Haasan", "Sonakshi_Sinha", "Sonam_Kapoor", "Taapsee_Pannu",
    "Tabu", "Tamannaah_Bhatia", "Vaani_Kapoor", "Vidya_Balan", "Yami_Gautam", "Zareen_Khan",
    "Angelina Jolie", "Jennifer Lawrence", "Kate Winslet", "Megan Fox", "Natalie Portman",
    "Nicole Kidman", "Sandra Bullock", "Scarlett Johansson",
    "Maria Sharapova", "mithali_raj",
    "Anushka Sanjeewani", "Chamari Athapaththu", "Kavisha Dilhari", "Nilakshi de Silva",
    "Oshadi Ranasinghe", "Shashikala Siriwardene", "Sugandika Kumari",
    "Bismah Maroof", "Harmanpreet Kaur", "Jahanara Alam", "Jemimah Rodrigues",
    "Kainat Imtiaz", "Nida Dar", "Smriti Mandhana",
    
    "Aishwarya Lekshmi", "Amala Paul", "Anne Hathaway", "Anupama Parameswaran", 
    "Becky Lynch", "Billie Eilish", "Cardi B", "Dua Lipa", 
    "Emma Watson", "Gal Gadot", "Katy Perry", "Keerthy Suresh", 
    "Kristen Stewart", "Krithi Shetty", "Malavika Mohanan", "Manju Warrier", 
    "Margot Robbie", "Nazriya Nazim", "Nicki Minaj", "Nithya Menen", 
    "Ronda Rousey", "Sai Pallavi", "Sreeleela", "Zendaya",
    "Chulakshi Ranathunga",
    "Dinakshie Priyasad",
    "Geethma Bandara",
    "Maheshi Madusanka",
    "Nayanathara Wickramarachchi",
    "Nethmi Roshel",
    "Oshadhi Himasha",
    "Paboda Sandeepani",
    "Piyumi Boteju",
    "Rashiprabha Sandeepani",
    "Shanudrie Priyasad",
    "Shehani Kahandagama",
    "Sheril Decker",
    "Suhandi Upethma",
    "Susila Kottegoda",
    "Thathsarani Piyumika",
    "Tina Shanell",
    "Upeksha Swarnamali",
    "Yohani Hettiarachchi",
    "Yureni Noshika"
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
        check_name_clean = person_name.replace("_", " ").replace("'", "'").title()

        gender = "Unknown"
       
        if person_name in male_list or check_name_underscores in male_list or check_name_clean in male_list:
            gender = "Man"
        elif person_name in female_list or check_name_underscores in female_list or check_name_clean in female_list:
            gender = "Woman"
        
        if gender == "Unknown":
            print(f"  [WARN] Skipping {person_name}: Not in gender lists. (Check spelling?)")
            continue
        
        # Count photos in folder
        photo_files = [f for f in os.listdir(person_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        photo_count = len(photo_files)
        
        # Determine augmentation level based on photo count
        if photo_count < 20:
            num_variations = 5
        elif photo_count < 40:
            num_variations = 4
        else:
            num_variations = 3
        
        print(f"  [INFO] Processing: {person_name} (Gender: {gender}, Photos: {photo_count}, Variations per photo: {num_variations})")
        
        person_embeddings = []
        
        for image_name in photo_files:
            image_path = os.path.join(person_dir, image_name)
            
            try:
                # Decide if we need augmentation
                if num_variations > 1:
                    image_variations = augment_image(image_path, num_variations)
                    print(f"    [AUG] Creating {num_variations} variations for {image_name}")
                else:
                    image_variations = [image_path]
                
                # Process each variation
                for img_data in image_variations:
                    try:
                        embedding_obj = DeepFace.represent(
                            img_path=img_data, 
                            model_name=model_name,
                            enforce_detection=True,
                            detector_backend='opencv'
                        )
                        
                        person_embeddings.append(embedding_obj[0]["embedding"])
                        
                    except Exception as e:
                        print(f"      [SKIP] Variation failed: {e}")
                        continue
                
            except Exception as e:
                print(f"    [SKIP] Could not process '{image_path}': {e}")

        if len(person_embeddings) > 0:
            master_embedding = np.mean(person_embeddings, axis=0)
            
            all_master_encodings.append({
                "name": check_name_clean, 
                "embedding": master_embedding,
                "gender": gender
            })
            print(f"    [OK] Created master fingerprint for {person_name} from {len(person_embeddings)} embeddings.")
        else:
            print(f"    [FAIL] No valid photos found for {person_name}, skipping.")

output_file = "deepface_encodings_PROTOTYPE.pickle"
print(f"\n[INFO] Serializing {len(all_master_encodings)} total master encodings...")
with open(output_file, "wb") as f:
    f.write(pickle.dumps(all_master_encodings))

print(f"[INFO] All faces encoded and saved to '{output_file}'")