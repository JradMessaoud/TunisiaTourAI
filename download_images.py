import os
import requests
from urllib.parse import urlparse

# Dossier où enregistrer les images
dest_folder = 'images'
os.makedirs(dest_folder, exist_ok=True)

# Liste des fichiers locaux et noms EXACTS d'images Wikimedia Commons
images = [
    ("sidi_bou_said.jpg", "Sidi_Bou_Said_2016.jpg"),
    ("tozeur.jpg", "Tozeur_Oasis.jpg"),
    ("hammamet.jpg", "Hammamet_beach_2015.jpg"),
    ("ain_draham.jpg", "Ain_Draham_vue_generale.jpg"),
    ("djerba.jpg", "Djerba_Beach_Tunisia.jpg"),
    ("tabarka.jpg", "Tabarka_Coastline.jpg"),
    ("monastir.jpg", "Monastir_Ribat_2015.jpg"),
    ("sousse.jpg", "Sousse_Medina_2015.jpg"),
    ("nabeul.jpg", "Nabeul_Pottery_2010.jpg"),
    ("kelibia.jpg", "Kelibia_Fortress_2010.jpg"),
    ("zarzis.jpg", "Zarzis_Beach_2010.jpg"),
    ("gafsa.jpg", "Gafsa_Oasis_2010.jpg"),
    ("le_kef.jpg", "Le_Kef_Citadel_2010.jpg"),
    ("bizerte.jpg", "Bizerte_Harbor_2010.jpg"),
    ("mahdia.jpg", "Mahdia_Beach_2010.jpg"),
    ("el_jem.jpg", "El_Jem_Amphitheatre_2015.jpg"),
    ("okba_kairouan.jpg", "Great_Mosque_of_Kairouan_Courtyard_2010.jpg"),
    ("carthage.jpg", "Carthage_Baths_of_Antoninus_2010.jpg"),
    ("dougga.jpg", "Dougga_Theatre_2015.JPG"),
    ("ribat_monastir.jpg", "Monastir_Ribat_2015.jpg"),
    ("medina_tunis.jpg", "Tunis_Medina_2010.jpg"),
    ("medina_sousse.jpg", "Sousse_Medina_2015.jpg"),
    ("medina_sfax.jpg", "Sfax_Medina_2010.jpg"),
    ("bourguiba_mausoleum.jpg", "Bourguiba_Mausoleum_2010.jpg"),
    ("cathedrale_st_louis.jpg", "Carthage_Cathedral_2010.jpg"),
    ("temple_eaux.jpg", "Zaghouan_Temple_2010.jpg"),
    ("fort_kelibia.jpg", "Kelibia_Fortress_2010.jpg"),
    ("citadelle_kef.jpg", "Le_Kef_Citadel_2010.jpg"),
    ("zitouna.jpg", "Zitouna_Mosque_2010.jpg"),
    ("port_bizerte.jpg", "Bizerte_Harbor_2010.jpg"),
    ("medina_mahdia.jpg", "Mahdia_Medina_2010.jpg"),
    ("bulla_regia.jpg", "Bulla_Regia_2010.jpg"),
    ("thuburbo_majus.jpg", "Thuburbo_Majus_2010.jpg"),
    ("medina_testour.jpg", "Testour_Medina_2010.jpg"),
    ("makthar.jpg", "Makthar_Ruins_2010.jpg"),
]

def get_commons_image_url(filename, width=800):
    endpoint = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": width,
        "format": "json"
    }
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "imageinfo" in page:
                return page["imageinfo"][0]["thumburl"]
    except Exception as e:
        print(f"Erreur lors de la récupération de l'URL pour {filename} : {e}")
    return None

def download_image(url, dest_path):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ImageDownloader/1.0)"}
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(r.content)
        print(f"Succès : {dest_path}")
    except Exception as e:
        print(f"Erreur lors du téléchargement de {dest_path} : {e}")

for local_name, commons_name in images:
    print(f"Téléchargement de {local_name} ...")
    url = get_commons_image_url(commons_name)
    if url:
        dest_path = os.path.join(dest_folder, local_name)
        download_image(url, dest_path)
    else:
        print(f"Image non trouvée sur Wikimedia Commons : {commons_name}")

print("Téléchargement terminé !") 