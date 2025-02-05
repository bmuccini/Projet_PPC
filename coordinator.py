import sysv_ipc
import pickle
from Vehicule import Vehicule
from Feu import Feu
import socket
import time
from shared_memory import create_shared_memory, get_shared_lights  # Importer la mémoire partagée

# Clés pour les files de messages
KEY_NORD = 1000
KEY_SUD = 1001
KEY_EST = 1002
KEY_OUEST = 1003

# Port de communication avec `display.py`
DISPLAY_PORT = 65433

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

def send_update_to_display(lights, vehicules):
    """Envoie l'état des feux et des véhicules à `display.py` via sockets."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", DISPLAY_PORT))
            data = {"lights": lights, "vehicles": vehicules}
            s.sendall(pickle.dumps(data))
    except ConnectionRefusedError:
        print("⚠️ `display.py` n'est pas en cours d'exécution.")
    except Exception as e:
        print(f"⚠️ Erreur de connexion avec `display.py` : {e}")

###Ce que j'ai fait###
def gerer_traffic(queue_nord, queue_sud, queue_est, queue_ouest, shm):
    shared_lights = get_shared_lights(shm)
    liste_vehicules = list()
    
    for direction, queue in [("N", queue_nord), ("S", queue_sud), ("E", queue_est), ("W", queue_ouest)]:
        feu = shared_lights[direction]

        while queue.current_messages == 0:
            message, _ = queue.receive()
            vehicule = (pickle.loads(message))

            if verif_vehicule_devant(vehicule, queue) :
                vehicule.arreter()
            
            elif feu.couleur == "rouge":
                if verif_feu (vehicule, feu) :
                    vehicule.arreter()

            elif  (-100 < vehicule.position_x < 100) and (-100 < vehicule.position_y < 100) : #coordonnées à modifier
                if direction == "N" :
                    queue_face = queue_sud
                elif direction == "S" :
                    queue_face = queue_nord
                elif direction == "E" :
                    queue_face = queue_ouest
                else :
                    queue_face = queue_est
                
                if verif_priorite_droite (vehicule, queue_face):
                    vehicule.arreter()
            
            else :
                verif_virage (vehicule)
                vehicule.avancer()

            liste_vehicules.append(vehicule)

    send_update_to_display(shared_lights, liste_vehicules)

def verif_feu (vehicule, feu) :

    difference_position_x = abs(vehicule.position_x - feu.position_x)
    difference_position_y = abs(vehicule.position_y - feu.position_y)

    if difference_position_x < 50 and difference_position_y < 50 and vehicule.orientation != feu.orientation: #coordonnées à changer
        return True
    
    else :
        return False

def verif_vehicule_devant (vehicule, queue) :
    while queue.current_messages == 0:
        message, _ = queue.receive()
        vehicule_devant = (pickle.loads(message))

        if vehicule_devant != vehicule :
            difference_position_x = abs(vehicule.position_x - vehicule_devant.position_x)
            difference_position_y = abs(vehicule.position_y - vehicule_devant.position_y)

            if difference_position_x < 50 and difference_position_y < 50 and vehicule.orientation == vehicule_devant.orientation: #coordonnées à changer
                return True 
            
    return False


def verif_priorite_droite (vehicule, queue_face):
    if vehicule.prochain_virage == "face" or vehicule.prochain_virage == "droite" :
        return False
    
    else : 
        while queue_face.current_messages == 0:
            message, _ = queue_face.receive()
            vehicule_face = (pickle.loads(message))

            if vehicule_face != vehicule :
                difference_position_x = abs(vehicule.position_x - vehicule_face.position_x)
                difference_position_y = abs(vehicule.position_y - vehicule_face.position_y)

                if difference_position_x < 50 and difference_position_y < 50 and vehicule.orientation != vehicule_face.orientation: #coordonnées à changer
                    
                    if vehicule_face.prochain_virage == "face" or vehicule_face.prochain_virage == "droite" :
                        return True
       
    return False

def verif_virage (vehicule):
    if vehicule.arrivee == "N":
        point_virage_x = 0 #a changer
        point_virage_y = 0 #a changer

    elif vehicule.arrivee == "S":
        point_virage_x = 0 #a changer
        point_virage_y = 0 #a changer

    elif vehicule.arrivee == "E":
        point_virage_x = 0 #a changer
        point_virage_y = 0 #a changer

    elif vehicule.arrivee == "W":
        point_virage_x = 0 #a changer
        point_virage_y = 0 #a changer
    
    
    if abs(vehicule.position_x - point_virage_x < 5) and abs(vehicule.position_y - point_virage_y < 5) : 
        if vehicule.prochain_virage == "gauche":
            vehicule.tourner_gauche()

        elif vehicule.prochain_virage == "droite":
             vehicule.tourner_droite()


if __name__ == "__main__":
    shm = create_shared_memory()  # Mémoire partagée commune
    #shared_lights = create_shared_memory()  # Initialisation mémoire partagée
    queue_nord, queue_sud, queue_est, queue_ouest = ouvrir_files_messages()  # Ouverture files de messages
    gerer_traffic(queue_nord, queue_sud, queue_est, queue_ouest, shm)  # Démarrage gestion du trafic