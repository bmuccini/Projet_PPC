"""from multiprocessing import Manager

def create_shared_memory():
    #Fonction qui crée une mémoire partagée sous forme de dictionnaire géré par Manager().dict() pour stocker l'état des feux
    manager = Manager()
    shared_lights = manager.dict({  # multiprocessing.Manager().dict() permet de stocker plusieurs valeurs (feux N, S, E, W), mieux que Value() ou Array()
        "N": "rouge",
        "S": "rouge",  # C’est juste la valeur de départ au lancement du programme, ne signifie pas que le feu du sud restera toujours rouge
        "E": "vert",
        "W": "vert"
    })
    return shared_lights"""

import sysv_ipc
import pickle

# Clé unique pour la mémoire partagée (identique pour tous les processus)
SHM_KEY = 1234

def create_shared_memory():
    """Crée ou se connecte à un segment de mémoire partagée avec sysv_ipc."""
    try:
        shm = sysv_ipc.SharedMemory(SHM_KEY, sysv_ipc.IPC_CREX, size=4096)
    except sysv_ipc.ExistentialError:
        shm = sysv_ipc.SharedMemory(SHM_KEY)
    
    # Initialiser les feux si c'est la première création
    try:
        initial_data = {"N": "rouge", "S": "rouge", "E": "vert", "W": "vert"}
        shm.write(pickle.dumps(initial_data))
    except sysv_ipc.ExistentialError:
        pass
    
    return shm

def get_shared_lights(shm):
    """Lit les états des feux depuis la mémoire partagée."""
    data = shm.read()
    return pickle.loads(data.strip(b'\x00'))  # Supprimer les octets nuls

def set_shared_lights(shm, lights_dict):
    """Écrit les états des feux dans la mémoire partagée."""
    shm.write(pickle.dumps(lights_dict))