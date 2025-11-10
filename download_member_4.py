import os
from bing_image_downloader import downloader

# --- Member 4 List ---
celebrity_list = [
    "Nanda Malini", "Latha Walpola", "Neela Wickramasinghe", "Chandralekha Perera",
    "Deepika Priyadarshini", "Umaria Sinhawansa", "Raini Charuka", "Samitha Mudunkotuwa",
    "Athma Liyanage", "Iranganie Serasinghe", "Ken Balendra", "Susantha Ratnayake",
    "Krishan Balendra", "Ashok Pathirage", "Deshamanya Mahesh Amalean", "Ajay Amalean",
    "Dr. Hans Wijayasuriya", "Shehan Karunatilaka", "Michael Ondaatje", "Geoffrey Bawa",
    "Romesh de Silva", "Dr. Harsha de Silva", "Prof. G. L. Peiris",
    "Dr. Paikiasothy Saravanamuttu", "Prof. Malik Peiris", "Dr. Nalin de Silva",
    "D. S. Senanayake", "Sir Nicholas Attygalle", "George Keyt", "H. L. de Silva",
    "Asha de Vos", "Kasturi Chellaraja Wilson", "Sheamalee Wickramasingha", "Shiromal Cooray",
    "Linda Speldewinde", "Radhika Coomaraswamy", "Shirani Bandaranayake",
    "Prof. Savitri Goonesekere", "Indira Samarasinghe", "Jean Arasanayagam",
    "Yasmine Gooneratne", "Anila Dias Bandaranaike", "Saskia Fernando",
    "Nayantara Fonseka", "Sybil Wettasinghe", "Anoka Abeyrathne", "Sumitra Peries",
    "Manik Sandrasagra", "Savithri Rodrigo", "Aruni Rajakarier"
]

# --- Output Folder ---
base_output_dir = 'dataset_4'

# --- The Download Loop ---
print(f"Starting download for {len(celebrity_list)} celebrities (Member 4)...")

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

print("\n--- Member 4 Download Complete ---")
print(f"Images are in: '{base_output_dir}'")