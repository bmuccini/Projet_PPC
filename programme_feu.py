#
"""
import time
from Feu import Feu


#C'est de la forme avec Feu qui est l'objet Feu
#dico_feu = {"feu_N" : Feu, "feu_S" : Feu, "feu_E" : Feu, "feu_W" : Feu}

def generation_feu():
    dico_feu = {}

    dico_feu["feu_N"] = Feu("N") #ici on donne la position nord 
    dico_feu["feu_S"] = Feu("S")
    dico_feu["feu_E"] = Feu("E")
    dico_feu["feu_W"] = Feu("W")

    return dico_feu


def changement_feu(dico_feu):
    feu_N = dico_feu["feu_N"] 
    feu_S = dico_feu["feu_S"] 
    feu_E = dico_feu["feu_E"] 
    feu_W = dico_feu["feu_W"] 

#Alternance des feux
    while True:
        feu_N.vert()
        feu_S.vert()
        feu_E.rouge()
        feu_W.rouge()
        time.sleep(10) #On prend un temps reglementaire
        feu_N.rouge()
        feu_S.rouge()
        feu_E.rouge()
        feu_W.rouge()
        time.sleep(2)
        feu_N.rouge()
        feu_S.rouge()
        feu_E.vert()
        feu_W.vert()
        time.sleep(10)

def priorite_traffic_feu(dico_feu, position):
    
    for feu in dico_feu.values() :
        
        if feu.position == position :
            feu.vert()
        else :
            feu.rouge()
"""

"""
import time
from shared_memory import create_shared_memory

def changement_feu(shared_lights):
    #Alterner les feux et mettre à jour la mémoire partagée
    while True:
        # Étape 1 : Feux N/S au vert, E/W au rouge
        shared_lights["N"] = "vert"  # Met à jour directement la mémoire partagée
        shared_lights["S"] = "vert"
        shared_lights["E"] = "rouge"
        shared_lights["W"] = "rouge"
        print(f"🔄 Feux mis à jour : {dict(shared_lights)}")
        time.sleep(10)

        # Étape 2 : Tous les feux au rouge (phase de sécurité)
        shared_lights["N"] = "rouge"
        shared_lights["S"] = "rouge"
        shared_lights["E"] = "rouge"
        shared_lights["W"] = "rouge"
        print(f"🚦 Phase de sécurité : {dict(shared_lights)}")
        time.sleep(2)

        # Étape 3 : Feux E/W au vert, N/S au rouge
        shared_lights["N"] = "rouge"
        shared_lights["S"] = "rouge"
        shared_lights["E"] = "vert"
        shared_lights["W"] = "vert"
        print(f"🔄 Feux mis à jour : {dict(shared_lights)}")
        time.sleep(10)

        # Étape 4 : Tous les feux au rouge (phase de sécurité)
        shared_lights["N"] = "rouge"
        shared_lights["S"] = "rouge"
        shared_lights["E"] = "rouge"
        shared_lights["W"] = "rouge"
        print(f"🚦 Phase de sécurité : {dict(shared_lights)}")
        time.sleep(2)

"""
"""
def priorite_traffic_feu(shared_lights, position):
    #Donner la priorité à un véhicule d'urgence en changeant le feu concerné en vert
    for direction in shared_lights.keys():
        if direction == position:
            shared_lights[direction] = "vert"
        else:
            shared_lights[direction] = "rouge"
    print(f"🚨 Priorité accordée au véhicule sur {position} : {dict(shared_lights)}")




if __name__ == "__main__":
    # Initialisation de la mémoire partagée
    shared_lights = create_shared_memory()  # Crée un dictionnaire partagé pour stocker les états des feux

    # Lancer le changement automatique des feux
    changement_feu(shared_lights)

# Maintenant, changement_feu() peut mettre à jour la mémoire partagée
"""


import time
#import sysv_ipc
import threading
import socket
from shared_memory import create_shared_memory, get_shared_lights, set_shared_lights

SOCKET_PORT = 65432

# Clé du sémaphore de signalisation
#SIGNAL_KEY = 5678

# Initialisation de l'Event pour gérer les véhicules prioritaires
#priorite_event = threading.Event()

#def ecouter_signal_prioritaire():
    #"""Thread qui écoute les signaux des véhicules prioritaires."""
    #signal_semaphore = sysv_ipc.Semaphore(SIGNAL_KEY, sysv_ipc.IPC_CREAT, initial_value=0)
    
    #while True:
        #signal_semaphore.acquire()  # Attendre un signal de `priority_trafic_gen.py`
        #priorite_event.set()  # Déclencher l'event pour la gestion prioritaire

class TrafficLight:
    def __init__(self):
        self.shm = create_shared_memory()
        self.priority_event = threading.Event()
        self.priority_direction = None
        self._setup_socket_server()
        #self.cycle_paused = False  # Flag pour gérer l'interruption

    def _setup_socket_server(self):
        def listener():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', SOCKET_PORT))
                s.listen()
                while True:
                    conn, _ = s.accept()
                    with conn:
                        data = conn.recv(1024).decode()
                        if data.startswith('PRIORITY'):
                            _, direction = data.split(':')
                            self.priority_direction = direction
                            self.priority_event.set()
                            print(f"🚨 Signal reçu : priorité à {direction}")

        threading.Thread(target=listener, daemon=True).start()

    def run_cycle(self):
        while True:
            if self.priority_event.is_set():
                # Phase prioritaire (4s vert + 1s rouge)
                self._handle_priority()
            else:
                # Cycle normal
                self.normal_cycle()

    def _handle_priority(self):
        """Gère l'activation des feux prioritaires."""
        # Feu prioritaire vert
        lights = {d: "rouge" for d in ["N", "S", "E", "W"]}
        lights[self.priority_direction] = "vert"
        set_shared_lights(self.shm, lights)
        print(f"🚨 FEU {self.priority_direction} VERT (5s)")
        time.sleep(5)

        #Tous les feux rouges
        lights = {d: "rouge" for d in ["N", "S", "E", "W"]}
        set_shared_lights(self.shm, lights)
        print("🔴 Tous les feux rouges (2s)")
        time.sleep(2)

        self.priority_event.clear()

    def normal_cycle(self):
        """Gère le cycle normal des feux."""
        lights = {"N": "vert", "S": "vert", "E": "rouge", "W": "rouge"}
        set_shared_lights(self.shm, lights)
        print("🟢 N/S verts | 🔴 E/W rouges")
        time.sleep(10)

        lights = {"N": "rouge", "S": "rouge", "E": "rouge", "W": "rouge"}
        set_shared_lights(self.shm, lights)
        print("🔴 Transition : Tous rouges")
        time.sleep(2)

        lights = {"E": "vert", "W": "vert", "N": "rouge", "S": "rouge"}
        set_shared_lights(self.shm, lights)
        print("🟢 E/W verts | 🔴 N/S rouges")
        time.sleep(10)

        lights = {"N": "rouge", "S": "rouge", "E": "rouge", "W": "rouge"}
        set_shared_lights(self.shm, lights)
        print("🔴 Transition : Tous rouges")
        time.sleep(2)


if __name__ == "__main__":
    TrafficLight().run_cycle()


""""
def changement_feu(shm):
    #Gère l'alternance normale des feux dans la mémoire partagée et réagit aux véhicules prioritaires
    while True:

        # Cycle normal des feux
        # Étape 1 : Feux N/S verts, E/W rouges
        lights = get_shared_lights(shm)
        lights.update({"N": "vert", "S": "vert", "E": "rouge", "W": "rouge"})
        set_shared_lights(shm, lights)
        print(f"Feux N/S verts : {lights}")
        time.sleep(10)

        # Étape 2 : Transition (tout rouge)
        lights.update({"N": "rouge", "S": "rouge"})
        set_shared_lights(shm, lights)
        print(f"Transition : {lights}")
        time.sleep(2)

        # Étape 3 : Feux E/W verts, N/S rouges
        lights.update({"E": "vert", "W": "vert", "N": "rouge", "S": "rouge"})
        set_shared_lights(shm, lights)
        print(f"Feux E/W verts : {lights}")
        time.sleep(10)

        # Étape 4 : Transition (tout rouge)
        lights.update({"E": "rouge", "W": "rouge"})
        set_shared_lights(shm, lights)
        print(f"Transition : {lights}")
        time.sleep(2)"""

#if __name__ == "__main__":
#    shm = create_shared_memory()
#    traffic_light = TrafficLight()
#    traffic_light.run(shm)

    # Lancer le thread qui écoute le signal des véhicules prioritaires
    #signal_thread = threading.Thread(target=ecouter_signal_prioritaire, daemon=True)
    #signal_thread.start()

    # Lancer la gestion des feux
    #changement_feu(shm)