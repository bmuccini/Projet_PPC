from Feu import Feu
import sysv_ipc
import pickle

# Clé unique pour la mémoire partagée (identique pour tous les processus)
SHM_KEY = 1234

def create_shared_memory():
    """Crée ou se connecte à un segment de mémoire partagée avec sysv_ipc."""
    try:
        shm = sysv_ipc.SharedMemory(SHM_KEY)
        shm.remove()
    except sysv_ipc.ExistentialError:
        pass

    feu_nord = Feu("N")
    feu_sud = Feu("S")
    feu_est = Feu("E")
    feu_ouest = Feu("W")
    
    
    shm = sysv_ipc.SharedMemory(SHM_KEY, sysv_ipc.IPC_CREX, size=4096)
    initial_data = {"N": feu_nord , "S": feu_sud, "E": feu_est, "W": feu_ouest}  #les objets ne sont pas toujours bien sérialisés avec pickle en mémoire partagée
    shm.write(pickle.dumps(initial_data))
   
    return shm

def connect_to_shared_memory():
    """Se connecte à la mémoire partagée existante sans la recréer."""
    try:
        return sysv_ipc.SharedMemory(SHM_KEY)  # Retourne la mémoire partagée si elle existe
    except sysv_ipc.ExistentialError:
        print("❌ La mémoire partagée n'existe pas !")
        return None  # Retourne None si elle n'existe pas



def get_shared_lights(shm):
    """Lit les états des feux depuis la mémoire partagée."""
    data = shm.read()
    try:
        objet_deserialized = pickle.loads(data.strip(b'\x00'))
        #print (objet_deserialized)
        #return pickle.loads(data.strip(b'\x00'))  # Supprimer les octets nuls et désérialiser
        

        return objet_deserialized
    except pickle.UnpicklingError:
        print("Erreur de lecture mémoire partagée, relecture en cours...")
        return None

def set_shared_lights(shm, lights):
    """Écrit les états des feux dans la mémoire partagée."""
    shm.write(pickle.dumps(lights))


def update_shared_lights(shm, key, new_value):
    lights = get_shared_lights(shm)
    lights[key] = new_value
    set_shared_lights(shm, lights)