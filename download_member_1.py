import os
from bing_image_downloader import downloader

# --- Member 1 List ---
celebrity_list = [
    "Malani Fonseka", "Swarna Mallawarachchi", "Veena Jayakody", "Kanchana Mendis",
    "Shalani Tharaka", "Gayathri Dias", "Saranga Disasekara", "Dinakshie Priyasad",
    "Shanudrie Priyasad", "Sheshadrie Priyasad", "Yureni Noshika", "Hemal Perera",
    "Roshan Ranawana", "Michelle", "Sajitha Anthony", "Akila Dhanuddara",
    "Raveen Kanishka", "Shehani Kahandagama", "Piyumi Boteju", "Chulakshi Ranathunga",
    "Maheshi Madusanka", "Upeksha Swarnamali", "Yohani Hettiarachchi", "Geethma Bandara",
    "Rashiprabha Sandeepani", "Dusheni Miyurangi", "Paboda Sandeepani", "Sachini Ayendra",
    "Dasuni Senethma", "Nadeesha Hemamali", "Susila Kottegoda", "Sheril Decker",
    "Sandani Fernando", "Nilushi Pawanya", "Oshadhi Himasha", "Tina Shanell",
    "Nayanathara Wickramarachchi", "Nethmi Roshel", "Shenaya Anisha", "Suhandi Upethma",
    "Thathsarani Piyumika", "Miyona de Silva", "Pooja Umashankar", "Udari Warnakulasuriya",
    "Udari Perera", "Ishi Rathnayake", "Uddika Premarathna", "Dhananjaya",
    "Kusal Maduranga", "Priyantha Siri Kumara"
]

# --- Output Folder ---
base_output_dir = 'dataset_1' 

# --- The Download Loop ---
print(f"Starting download for {len(celebrity_list)} celebrities (Member 1)...")

for name in celebrity_list:
    query = name
    print(f"\nDownloading images for: {name}")
    
    downloader.download(
        query=query,
        limit=15,  # Download 15, then manually clean to keep 5-10
        output_dir=base_output_dir,
        filter='photo',
        force_replace=False,
        timeout=60,
        verbose=True
    )

print("\n--- Memeber 1 Download Complete ---")
print(f"Images are in: '{base_output_dir}'")