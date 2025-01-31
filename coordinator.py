from multiprocessing import Queue
from normal_trafic_gen import queue_nord, queue_sud, queue_est, queue_ouest
import time

def gerer_traffic():
    """Lit les véhicules des files de messages et les traite."""
    while True:
        # Lire les véhicules des files de messages
        if not queue_nord.empty():
            vehicule_nord = queue_nord.get()
            print(f"Véhicule Nord traité : {vehicule_nord}")

        if not queue_sud.empty():
            vehicule_sud = queue_sud.get()
            print(f"Véhicule Sud traité : {vehicule_sud}")

        if not queue_est.empty():
            vehicule_est = queue_est.get()
            print(f"Véhicule Est traité : {vehicule_est}")

        if not queue_ouest.empty():
            vehicule_ouest = queue_ouest.get()
            print(f"Véhicule Ouest traité : {vehicule_ouest}")

        time.sleep(1)  # Vérifier les files toutes les secondes



if __name__ == "__main__":
    gerer_traffic()

