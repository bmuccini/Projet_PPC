import sysv_ipc
import pickle
from Vehicule import Vehicule
from Feu import Feu
import socket
import time
from shared_memory import  get_shared_lights, connect_to_shared_memory  # Importer la mémoire partagée

# Clés pour les files de messages
KEY_NORD = 1000
KEY_SUD = 1001
KEY_EST = 1002
KEY_OUEST = 1003

liste_vehicules = []
shm = connect_to_shared_memory()

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
            s.connect(('localhost', 65437))
            data = {"lights": lights, "vehicules": vehicules}
            s.sendall(pickle.dumps(data))
  
    except ConnectionRefusedError:
        print("⚠️ `display.py` n'est pas en cours d'exécution.")
    except Exception as e:
        print(f"⚠️ Erreur de connexion avec `display.py` : {e}")

def recuperer_vehicules(queues):
    for queue in queues:
        try:
            message, _ = queue.receive(block = False)
            vehicule = pickle.loads(message)
            liste_vehicules.append(vehicule)
        except sysv_ipc.BusyError:
            pass

def gerer_trafic():
    shared_lights = get_shared_lights(shm)
    for vehicule in liste_vehicules:
        if not doit_arreter_au_feu(vehicule) and not doit_arreter_derriere_vehicule(vehicule) or vehicule.prioritaire:
            vehicule.avancer()
            vehicule.tourner()
    supprimer_vehicules()
    send_update_to_display(shared_lights, liste_vehicules)

def supprimer_vehicules():
    liste_vehicules[:] = [vehicule for vehicule in liste_vehicules if not vehicule_est_sorti(vehicule)]

def doit_arreter_au_feu(vehicule : Vehicule):
    feux = get_shared_lights(shm)
    feu = feux[vehicule.depart]

    if vehicule.avant_feu():
        if feu.couleur == "rouge" :
            return True
        else:
            return False

def doit_arreter_derriere_vehicule(vehicule : Vehicule):
    for v in liste_vehicules:
        if v == vehicule:
            continue
        if vehicule.doit_arreter_derriere(v):
            return True
    return False

def vehicule_est_sorti(vehicule):
    return vehicule.position_x < 0 or vehicule.position_x > 1200 or vehicule.position_y < 0 or vehicule.position_y > 800


if __name__ == "__main__":
    shm = connect_to_shared_memory() # Mémoire partagée commune
    
    queue_nord, queue_sud, queue_est, queue_ouest = ouvrir_files_messages()  # Ouverture files de messages
    queues = [queue_sud, queue_nord, queue_est, queue_ouest]
    while True: 
        recuperer_vehicules(queues= queues)
        gerer_trafic()
        time.sleep(0.4)
