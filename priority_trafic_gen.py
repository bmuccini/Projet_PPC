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
QUEUE_KEYS = {"N": 1000, "S": 1001, "E": 1002, "W": 1003}
SOCKET_PORT = 65432

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

    #except (ConnectionRefusedError, TimeoutError) as e:
    #    print(f"⚠️ Erreur de connexion : {e}. Vérifiez que programme_feu.py est lancé.")
    #except Exception as e:
    #    print(f"⚠️ Erreur inattendue : {e}")

def generate_priority_vehicles():
    # Ouvrir les files de messages
    queues = {dir: sysv_ipc.MessageQueue(key) for dir, key in QUEUE_KEYS.items()}
    
    while True:
        try:
            # Générer un véhicule prioritaire
            depart = ["N", "S", "E", "W"][randint(0, 3)]
            arrivee = [d for d in ["N", "S", "E", "W"] if d != depart][randint(0, 2)]
            
            vehicule = Vehicule(depart, arrivee, True)
            queues[depart].send(pickle.dumps(vehicule))
            print(f"🚑 Véhicule prioritaire {depart}→{arrivee}")

            # Envoyer le signal pour prioriser ce véhicule
            send_signal(depart)
            
            time.sleep(16)  # Attendre 8 secondes avant de générer un autre véhicule prioritaire
        
        #except KeyboardInterrupt:
        #    print("\nArrêt de la génération de trafic prioritaire.")
        #    break
        except Exception as e:
            print(f"⚠️ Erreur critique : {e}")
            time.sleep(5)  # Attendre avant de réessayer

if __name__ == "__main__":
    generate_priority_vehicles()

