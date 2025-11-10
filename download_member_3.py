import os
from bing_image_downloader import downloader

# --- Member 3 List ---
celebrity_list = [
    "Sirimavo Bandaranaike", "Chandrika Kumaratunga", "Sudugala Sudarshani Fernandopulle",
    "Pabitra Wanniarachchi", "Thalatha Atukorale", "Ranil Wickremesinghe",
    "Anura Kumara Dissanayake", "Sajith Premadasa", "Mahinda Rajapaksa", "Namal Rajapaksa",
    "Gotabaya Rajapaksa", "Basil Rajapaksa", "Chamal Rajapaksa", "Harin Fernando",
    "Manusha Nanayakkara", "Johnston Fernando", "Wijeyadasa Rajapakshe",
    "Nimal Siripala de Silva", "Wimal Weerawansa", "Udaya Gammanpila", "Vasudeva Nanayakkara",
    "Rauff Hakeem", "M. A. Sumanthiran", "Douglas Devananda", "Patali Champika Ranawaka",
    "Sarath Fonseka", "Mahindananda Aluthgamage", "Keheliya Rambukwella",
    "Dullas Alahapperuma", "Prasanna Ranatunga", "Clarence Wijewardena", "W. D. Amaradeva",
    "Victor Rathnayake", "Sunil Perera", "Piyal Perera", "Bathiya Jayakody",
    "Santhush Weeraman", "Kasun Kalhara", "Nadeemal Perera", "Chitral Somapala",
    "Rookantha Gunathilake", "Iraj Weeraratne", "Lahiru Perera", "Gration Ananda",
    "Sunil Edirisinghe", "Edward Jayakody", "T. M. Jayaratne", "Lester James Peries",
    "Tony Ranasinghe", "Gamini Fonseka"
]

# --- Output Folder ---
base_output_dir = 'dataset_3' 

# --- The Download Loop ---
print(f"Starting download for {len(celebrity_list)} celebrities (Member 3)...")

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

print("\n--- Member 3 Download Complete ---")
print(f"Images are in: '{base_output_dir}'")