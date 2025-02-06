import sysv_ipc
from Vehicule import Vehicule
from random import randint
import time
import pickle

# Clés pour les files de messages
KEY_NORD = 1000  # Clé unique qui identifie la file de messages nord
KEY_SUD = 1001
KEY_EST = 1002
KEY_OUEST = 1003

def creation_files_messages():
    """Crée les files de messages en utilisant le mécanisme de communication inter-processus (IPC) de System V."""
    try:
        queue_nord = sysv_ipc.MessageQueue(KEY_NORD, sysv_ipc.IPC_CREAT)  # sysv_ipc.IPC_CREAT : flag qui indique que la file de messages doit être créée si elle n'existe pas déjà. Sinon qu'elle est simplement ouverte
        queue_sud = sysv_ipc.MessageQueue(KEY_SUD, sysv_ipc.IPC_CREAT)  # Crée et ouvre la file de messages sud
        queue_est = sysv_ipc.MessageQueue(KEY_EST, sysv_ipc.IPC_CREAT)
        queue_ouest = sysv_ipc.MessageQueue(KEY_OUEST, sysv_ipc.IPC_CREAT)
        return queue_nord, queue_sud, queue_est, queue_ouest
    except sysv_ipc.ExistentialError:
        print("Erreur : Les files de messages existent déjà.")
        exit(1)

def generation_trafic_normal(queue_nord, queue_sud, queue_est, queue_ouest):
    """Génère des véhicules et les ajoute aux files de messages."""
    while True:
        liste_direction = ["N", "S", "E", "W"]
        depart = liste_direction[randint(0, 3)]
        liste_direction.remove(depart)
        arrivee = liste_direction[randint(0, 2)]

        vehicule = Vehicule(depart, arrivee, False)

        message = pickle.dumps(vehicule)  #  module pickle sérialiser vehicule en une chaîne de bytes (format qui peut être transmis)

        if depart == "N":
            queue_nord.send(message)  # Envoie un message dans la file de messages nord
            print(f"Véhicule Nord ajouté : {vehicule}")
        elif depart == "S":
            queue_sud.send(message)
            print(f"Véhicule Sud ajouté : {vehicule}")
        elif depart == "E":
            queue_est.send(message)
            print(f"Véhicule Est ajouté : {vehicule}")
        else:
            queue_ouest.send(message)
            print(f"Véhicule Ouest ajouté : {vehicule}")

        time.sleep(2)

if __name__ == "__main__":
    """Point d'entrée du programme.
    Crée les files de messages et commence la génération du trafic."""
    queue_nord, queue_sud, queue_est, queue_ouest = creation_files_messages()
    generation_trafic_normal(queue_nord, queue_sud, queue_est, queue_ouest)