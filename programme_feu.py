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
from shared_memory import create_shared_memory, get_shared_lights, set_shared_lights
import threading
import sysv_ipc

# Clé du sémaphore de signalisation
SIGNAL_KEY = 5678

# Initialisation de l'Event pour gérer les véhicules prioritaires
priorite_event = threading.Event()

def ecouter_signal_prioritaire():
    """Thread qui écoute les signaux des véhicules prioritaires."""
    signal_semaphore = sysv_ipc.Semaphore(SIGNAL_KEY, sysv_ipc.IPC_CREAT, initial_value=0)
    
    while True:
        signal_semaphore.acquire()  # Attendre un signal de `priority_trafic_gen.py`
        priorite_event.set()  # Déclencher l'event pour la gestion prioritaire

def changement_feu(shm):
    """Gère l'alternance normale des feux dans la mémoire partagée et réagit aux véhicules prioritaires"""
    while True:

        if priorite_event.is_set():  # Si un véhicule prioritaire est signalé
            lights = get_shared_lights(shm)

            # On garde l'état du feu avant l'interruption
            print(f"⚠️ Passage véhicule prioritaire, arrêt du cycle normal.")
            priorite_event.clear()  # Reset du signal pour la prochaine alerte

            # Lire l'origine du véhicule prioritaire (en supposant que c'est stocké dans la mémoire partagée)
            origine_prioritaire = lights["priorite"]  # Stocke la direction du véhicule prioritaire

            # Tous les feux en rouge sauf celui d'origine du véhicule prioritaire
            for direction in ["N", "S", "E", "W"]:
                lights[direction] = "rouge"
            lights[origine_prioritaire] = "vert"

            set_shared_lights(shm, lights)  # Mettre à jour la mémoire partagée
            print(f"🚨 Feu prioritaire activé : {origine_prioritaire} est maintenant vert.")

            time.sleep(5)  # Laisse passer le véhicule prioritaire

            # Rétablir le cycle normal des feux après le passage du véhicule prioritaire
            print("🔄 Reprise du cycle normal.")
            priorite_event.clear()  # Réinitialiser l'event pour attendre un nouveau véhicule prioritaire
        else :
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
            time.sleep(2)

if __name__ == "__main__":
    shm = create_shared_memory()
    
    # Lancer le thread qui écoute le signal des véhicules prioritaires
    signal_thread = threading.Thread(target=ecouter_signal_prioritaire, daemon=True)
    signal_thread.start()

    # Lancer la gestion des feux
    changement_feu(shm)