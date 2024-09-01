from server.fakemcserveur import search_and_clean_jars
import time

def monitor_files():
    while True:
        try:
            search_and_clean_jars()
        except Exception as e:
            print(f"Erreur dans la recherche et le nettoyage des fichiers JAR : {e}")
        time.sleep(15)