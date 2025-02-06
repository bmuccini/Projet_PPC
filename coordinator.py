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
            s.settimeout(2)
            s.connect(('localhost', 65435))
            data = {"lights": lights, "vehicules": vehicules}
            s.sendall(pickle.dumps(data))
  
    except ConnectionRefusedError:
        print("⚠️ `display.py` n'est pas en cours d'exécution.")
    except Exception as e:
        print(f"⚠️ Erreur de connexion avec `display.py` : {e}")


def gerer_traffic(queue_nord, queue_sud, queue_est, queue_ouest, shm):
    shared_lights = get_shared_lights(shm)
    liste_vehicules = []

    for direction, queue in [("N", queue_nord), ("S", queue_sud), ("E", queue_est), ("W", queue_ouest)]:
        feu = shared_lights[direction]

        messages_temp = []  # Stockage temporaire des véhicules

        while True:
            try:
                message, _ = queue.receive(block=False)  # Lire sans bloquer
                vehicule : Vehicule = pickle.loads(message)

                # 🚦 Gestion du trafic
                if verif_vehicule_devant(vehicule, queue):
                    vehicule.arreter()
                
                elif feu.couleur == "rouge" and verif_feu(vehicule, feu):
                    vehicule.arreter()

                elif -100 < vehicule.position_x < 100 and -100 < vehicule.position_y < 100:  # Dans le carrefour
                    if direction == "N" :
                        queue_face = queue_sud
                    elif direction == "S" :
                        queue_face = queue_nord
                    elif direction == "E" :
                        queue_face = queue_ouest
                    else :
                        queue_face = queue_est

                    if verif_priorite_droite(vehicule, queue_face):
                        vehicule.arreter()
                    elif verif_virage(vehicule):
                        if vehicule.prochain_virage == "gauche":
                            vehicule.tourner_gauche()
                        elif vehicule.prochain_virage == "droite":
                            vehicule.tourner_droite()
                        vehicule.avancer()
                else:
                    vehicule.avancer()

                # 🚗 Ajouter le véhicule dans la liste s'il est toujours dans la simulation
                if not verif_sortie_display(vehicule):
                    messages_temp.append(vehicule)

            except sysv_ipc.BusyError:
                break  # La file est vide, on arrête la boucle

        # 📨 Réinsérer les véhicules dans la file
        for vehicule in messages_temp:
            queue.send(pickle.dumps(vehicule))
            liste_vehicules.append(vehicule)

    print('proutiflex')

    # 📡 Mise à jour de l'affichage
    send_update_to_display(shared_lights, liste_vehicules)



def verif_feu (vehicule, feu) :

    difference_position_x = abs(vehicule.position_x - feu.position_x)
    difference_position_y = abs(vehicule.position_y - feu.position_y)

    if difference_position_x < 50 and difference_position_y < 50 and vehicule.orientation != feu.orientation: #coordonnées à changer
        return True
    
    else :
        return False

def verif_vehicule_devant (vehicule, queue) :
    messages_temp = []
    while True:
        try:
            message, _ = queue.receive(block=False)  # Lire sans bloquer
            vehicule_devant = (pickle.loads(message))

            messages_temp.append(vehicule)

            if vehicule_devant != vehicule :
                difference_position_x = abs(vehicule.position_x - vehicule_devant.position_x)
                difference_position_y = abs(vehicule.position_y - vehicule_devant.position_y)

                if difference_position_x < 50 and difference_position_y < 50 and vehicule.orientation == vehicule_devant.orientation: #coordonnées à changer
                    return True 

        except sysv_ipc.BusyError:
                break  # La file est vide, on arrête la boucle

    for vehicule in messages_temp:
            queue.send(pickle.dumps(vehicule))
            
        


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
    if vehicule.depart == "N":
        if vehicule.arrivee == "E":
            point_virage_x = 0 #a changer
            point_virage_y = 0 #a changer
        elif vehicule.arrivee == "W":
            point_virage_x = 0 #a changer
            point_virage_y = 0 #a changer

    elif vehicule.depart == "S":
        if vehicule.arrivee == "E":
            point_virage_x = 0 #a changer
            point_virage_y = 0 #a changer
        elif vehicule.arrivee == "W":
            point_virage_x = 0 #a changer
            point_virage_y = 0 #a changer

    elif vehicule.depart == "E":
        if vehicule.arrivee == "N":
            point_virage_x = 0 #a changer
            point_virage_y = 0 #a changer
        elif vehicule.arrivee == "S":
            point_virage_x = 0 #a changer
            point_virage_y = 0 #a changer

    elif vehicule.depart == "W":
        if vehicule.arrivee == "N":
            point_virage_x = 0 #a changer
            point_virage_y = 0 #a changer
        elif vehicule.arrivee == "S":
            point_virage_x = 0 #a changer
            point_virage_y = 0 #a changer
    
    if abs(vehicule.position_x - point_virage_x < 5) and abs(vehicule.position_y - point_virage_y < 5) : 
         return True
    
    else :
        return False


def verif_sortie_display (vehicule):

    if ( 0 <= vehicule.position_x <= 1200 ) and ( 0 <= vehicule.position_y <= 800 ):
        return False
    
    else : 
        return True



if __name__ == "__main__":
    shm = create_shared_memory()  # Mémoire partagée commune
    #shared_lights = create_shared_memory()  # Initialisation mémoire partagée
    
    while True: 
        queue_nord, queue_sud, queue_est, queue_ouest = ouvrir_files_messages()  # Ouverture files de messages
        gerer_traffic(queue_nord, queue_sud, queue_est, queue_ouest, shm)  # Démarrage gestion du trafic