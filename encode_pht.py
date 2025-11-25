import os
import pickle
import numpy as np 
from deepface import DeepFace
male_list = [
    # Bollywood (50)
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
    
    # Hollywood (9)
    "Brad Pitt", "Denzel Washington", "Hugh Jackman", "Johnny Depp", "Leonardo DiCaprio",
    "Robert Downey Jr.", "Tom Cruise", "Tom Hanks", "Will Smith",
    
    # Global Sports (5)
    # Removed: Harry Kane
    "Cristiano Ronaldo", "Kobe Bryant", "ms_dhoni", "sachin_tendulkar", "virat_kohli",

    # Sri Lankan Cricketers (29)
    "Aravinda de Silva", "Arjuna Ranatunga", "Chaminda Vaas", "Charith Asalanka", 
    "Dhananjaya de Silva", "Dimuth Karunaratne", "Dinesh Chandimal", "Dushmantha Chameera",
    "Kumar Sangakkara", "Kusal Mendis", "Kusal Perera", "Lahiru Thirimanne", "Lasith Malinga",
    "Maheesh Theekshana", "Mahela Jayawardene", "Marvan Atapattu", "Matheesha Pathirana",
    "Muttiah Muralitharan", "Niroshan Dickwella", "Nuwan Kulasekara", "Pathum Nissanka",
    "Pramod Madushan", "Rangana Herath", "Romesh Kaluwitharana", "Sanath Jayasuriya",
    "Suranga Lakmal", "Thisara Perera", "Tillakaratne Dilshan", "Upul Tharanga",

    # South Asian Cricketers (10)
    "Babar Azam", "Imran Khan", "Mashrafe Mortaza", "Rohit Sharma", "Shahid Afridi",
    "Shakib Al Hasan", "Shoaib Akhtar", "Tamim Iqbal", "Wasim Akram", "Yuvraj Singh"
]

female_list = [
    # Bollywood (49)
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
    
    # Hollywood (8)
    "Angelina Jolie", "Jennifer Lawrence", "Kate Winslet", "Megan Fox", "Natalie Portman",
    "Nicole Kidman", "Sandra Bullock", "Scarlett Johansson",
    
    # Global Sports (2)
    "Maria Sharapova", "mithali_raj",

    # Sri Lankan Cricketers (7)
    "Anushka Sanjeewani", "Chamari Athapaththu", "Kavisha Dilhari", "Nilakshi de Silva",
    "Oshadi Ranasinghe", "Shashikala Siriwardene", "Sugandika Kumari",

    # South Asian Cricketers (7)
    "Bismah Maroof", "Harmanpreet Kaur", "Jahanara Alam", "Jemimah Rodrigues",
    "Kainat Imtiaz", "Nida Dar", "Smriti Mandhana"
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
        
       
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            
            if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            try:
               
                embedding_obj = DeepFace.represent(
                    img_path=image_path, 
                    model_name=model_name,
                    enforce_detection=True
                )
                
                person_embeddings.append(embedding_obj[0]["embedding"])
                
            except Exception as e:
                
                print(f"    [SKIP] Could not process '{image_path}': {e}")

      
        if len(person_embeddings) > 0:
            
            master_embedding = np.mean(person_embeddings, axis=0)
            
            
            all_master_encodings.append({
                "name": check_name_clean, 
                "embedding": master_embedding,
                "gender": gender
            })
            print(f"    [OK] Created master fingerprint for {person_name} from {len(person_embeddings)} photos.")
        else:
            print(f"    [FAIL] No valid photos found for {person_name}, skipping.")
            

output_file = "deepface_encodings_PROTOTYPE.pickle"
print(f"\n[INFO] Serializing {len(all_master_encodings)} total master encodings...")
with open(output_file, "wb") as f:
    f.write(pickle.dumps(all_master_encodings))

print(f"[INFO] All faces encoded and saved to '{output_file}'")