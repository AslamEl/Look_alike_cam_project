import os
from bing_image_downloader import downloader

# --- Member 2 List ---
celebrity_list = [
    "Chanuka Prabuddha", "Lavan Abhishek", "Pramod Ganearachchi", "Sachin Liyanage",
    "Randika Gunathilaka", "Isuru Lokuhettiarachchi", "Ravindra Randeniya", "Sriyantha Mendis",
    "Pubudu Chathuranga", "Yash Weerasinghe", "Arjuna Ranatunga", "Aravinda de Silva",
    "Sanath Jayasuriya", "Muttiah Muralitharan", "Chaminda Vaas", "Lasith Malinga",
    "Tillakaratne Dilshan", "Dinesh Chandimal", "Dimuth Karunaratne", "Kusal Perera",
    "Kusal Mendis", "Niroshan Dickwella", "Dhananjaya de Silva", "Charith Asalanka",
    "Pathum Nissanka", "Nuwan Kulasekara", "Rangana Herath", "Suranga Lakmal",
    "Thisara Perera", "Upul Tharanga", "Marvan Atapattu", "Romesh Kaluwitharana",
    "Hashan Tillakaratne", "Dushmantha Chameera", "Maheesh Theekshana", "Matheesha Pathirana",
    "Pramod Madushan", "Asanka Gurusinha", "Roshan Mahanama", "Lahiru Thirimanne",
    "Chamari Athapaththu", "Shashikala Siriwardene", "Inoka Ranaweera", "Oshadi Ranasinghe",
    "Nilakshi de Silva", "Harshitha Samarawickrama", "Kavisha Dilhari", "Sugandika Kumari",
    "Anushka Sanjeewani", "Hasini Perera"
]

# --- Output Folder ---
base_output_dir = 'dataset_2' 

# --- The Download Loop ---
print(f"Starting download for {len(celebrity_list)} celebrities (Member 2)...")

for name in celebrity_list:
    query = name
    print(f"\nDownloading images for: {name}")
    
    downloader.download(
        query=query,
        limit=15,
        output_dir=base_output_dir,
        filter='photo',
        force_replace=False,
        timeout=60,
        verbose=True
    )

print("\n--- Member 2 Download Complete ---")
print(f"Images are in: '{base_output_dir}'")