"""import sysv_ipc
from Vehicule import Vehicule
from random import randint
import time
import pickle
import socket

# Clés pour les files de message qui doivent etre les meme que celles pour les véhicules normaux
KEY_NORD = 1000
KEY_SUD = 1001
KEY_EST = 1002
KEY_OUEST = 1003

# Clé pour le signal des véhicules prioritaires
#SIGNAL_KEY = 5678

#Ouvre les files de messages
def ouvrir_files_messages():
    try:
        queue_nord = sysv_ipc.MessageQueue(KEY_NORD)
        queue_sud = sysv_ipc.MessageQueue(KEY_SUD)
        queue_est = sysv_ipc.MessageQueue(KEY_EST)
        queue_ouest = sysv_ipc.MessageQueue(KEY_OUEST)
        return queue_nord, queue_sud, queue_est, queue_ouest
    except sysv_ipc.ExistentialError:
        print("Erreur : Les files de messages n'existent pas.")
        exit(1)

def send_priority_signal(direction):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 65432))
        s.sendall(f'PRIORITY:{direction}'.encode())  # Envoyer la direction

# Genère des véhicules prioritaires et les ajoutes aux files de messages
def generation_trafic_prioritaire(queue_nord, queue_sud, queue_est, queue_ouest):
    #semaphore_signal = sysv_ipc.Semaphore(SIGNAL_KEY, sysv_ipc.IPC_CREAT)

    #Creation des vehicules
    while True :
        liste_direction = ["N","S","E","W"]  # Doit etre dans la boucle pour que la taille de la liste reste constante
        depart = liste_direction[randint(0,3)]
        liste_direction.remove(depart)
        
        arrivee = liste_direction[randint(0,2)]

        vehicule = Vehicule(depart, arrivee, True) #True pour signifier véhicule prioritaire
        message = pickle.dumps(vehicule)  # Sérialiser avec pickle

        if depart == "N":
            queue_nord.send(message)
            print(f"Véhicule prioritaire Nord ajouté : {vehicule}")
        elif depart == "S":
            queue_sud.send(message)
            print (f"Véhicule prioritaire Sud ajouté : {vehicule}")
        elif depart == "E":
            queue_est.send(message)
            print (f"Véhicule prioritaire Est ajouté : {vehicule}")
        else:
            queue_ouest.send(message)
            print (f"Véhicule prioritaire Ouest ajouté : {vehicule}")

        # Signaler à lights.py de modifier les feux
        #semaphore_signal.release()
        #print(f"📢 Signal envoyé à lights.py pour prioriser {depart}")
        send_priority_signal(depart)
        time.sleep(8) #temps entre chaque généraation de véhicule prioritaire

# Exemple d'utilisation
#send_priority_signal(depart)


if __name__ == "__main__":
    # Ouvrir les files de messages
    queue_nord, queue_sud, queue_est, queue_ouest = ouvrir_files_messages()

    # Démarrer la génération de trafic prioritaire
    generation_trafic_prioritaire(queue_nord, queue_sud, queue_est, queue_ouest)"""


import sysv_ipc
from Vehicule import Vehicule
from random import randint
import time
import pickle
import socket

# Configuration
KEY_NORD = 1000
KEY_SUD = 1001
KEY_EST = 1002
KEY_OUEST = 1003

SOCKET_PORT = 65432

def creation_files_messages():
    """Crée les files de messages System V."""
    try:
        queue_nord = sysv_ipc.MessageQueue(KEY_NORD, sysv_ipc.IPC_CREAT)
        queue_sud = sysv_ipc.MessageQueue(KEY_SUD, sysv_ipc.IPC_CREAT)
        queue_est = sysv_ipc.MessageQueue(KEY_EST, sysv_ipc.IPC_CREAT)
        queue_ouest = sysv_ipc.MessageQueue(KEY_OUEST, sysv_ipc.IPC_CREAT)
        return queue_nord, queue_sud, queue_est, queue_ouest
    except sysv_ipc.ExistentialError:
        print("Erreur : Les files de messages existent déjà.")
        exit(1)

def send_signal(direction):
    """Envoie un signal à `programme_feu.py` pour donner la priorité à un véhicule prioritaire."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)  # Timeout de 2 secondes
            s.connect(('localhost', SOCKET_PORT))
            s.sendall(f'PRIORITY:{direction}'.encode())
            print(f"📢 Signal envoyé à programme_feu.py pour donner la priorité au feu {direction}")
    except ConnectionRefusedError:
        print("⚠️ Erreur : programme_feu.py ne semble pas être en cours d'exécution.")
    except Exception as e:
        print(f"⚠️ Erreur inattendue : {e}")


def generation_trafic_prioritaire(queue_nord, queue_sud, queue_est, queue_ouest):
    """Génère des véhicules et les ajoute aux files de messages."""
    while True:
        liste_direction = ["N", "S", "E", "W"]
        depart = liste_direction[randint(0, 3)]
        liste_direction.remove(depart)
        arrivee = liste_direction[randint(0, 2)]

        vehicule = Vehicule(depart, arrivee, True)

        message = pickle.dumps(vehicule)  

        if depart == "N":
            queue_nord.send(message)
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

        send_signal(depart)
        time.sleep(2)



if __name__ == "__main__":
 
    queue_nord, queue_sud, queue_est, queue_ouest = creation_files_messages()
    generation_trafic_prioritaire(queue_nord, queue_sud, queue_est, queue_ouest)

