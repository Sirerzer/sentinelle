from monitoring.docker.usage import check_and_stop_containers



def monitor_files():
    while True:
        try:
            check_and_stop_containers()
        except Exception as e:
            print(f"Erreur lors de la vérification et de l'arrêt des conteneurs : {e}")
