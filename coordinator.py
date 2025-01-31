import sysv_ipc
import pickle
from Vehicule import Vehicule
import time

# Clés pour les files de messages
KEY_NORD = 1000
KEY_SUD = 1001
KEY_EST = 1002
KEY_OUEST = 1003

def ouvrir_files_messages():
    """Ouvre les files de messages System V."""
    try:
        queue_nord = sysv_ipc.MessageQueue(KEY_NORD)
        queue_sud = sysv_ipc.MessageQueue(KEY_SUD)
        queue_est = sysv_ipc.MessageQueue(KEY_EST)
        queue_ouest = sysv_ipc.MessageQueue(KEY_OUEST)
        return queue_nord, queue_sud, queue_est, queue_ouest
    except sysv_ipc.ExistentialError:
        print("Erreur : Les files de messages n'existent pas.")
        exit(1)

def gerer_traffic(queue_nord, queue_sud, queue_est, queue_ouest):
    """Lit les véhicules des files de messages et les traite."""
    while True:
        try:
            message_nord, _ = queue_nord.receive(block=False)
            vehicule_nord = pickle.loads(message_nord)  # Désérialiser avec pickle
            print(f"Véhicule Nord traité : {vehicule_nord}")
        except sysv_ipc.BusyError:
            pass

        try:
            message_sud, _ = queue_sud.receive(block=False)
            vehicule_sud = pickle.loads(message_sud)
            print(f"Véhicule Sud traité : {vehicule_sud}")
        except sysv_ipc.BusyError:
            pass

        try:
            message_est, _ = queue_est.receive(block=False)
            vehicule_est = pickle.loads(message_est)
            print(f"Véhicule Est traité : {vehicule_est}")
        except sysv_ipc.BusyError:
            pass

        try:
            message_ouest, _ = queue_ouest.receive(block=False)
            vehicule_ouest = pickle.loads(message_ouest)
            print(f"Véhicule Ouest traité : {vehicule_ouest}")
        except sysv_ipc.BusyError:
            pass

        time.sleep(1)

if __name__ == "__main__":
    queue_nord, queue_sud, queue_est, queue_ouest = ouvrir_files_messages()
    gerer_traffic(queue_nord, queue_sud, queue_est, queue_ouest)