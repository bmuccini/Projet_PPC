from multiprocessing import Process, Manager
from Vehicule import Vehicule
from random import randint
import time

def generation_trafic_normal(queue_nord, queue_sud, queue_est, queue_ouest):    

    #Creation des vehicules
    while True :
        liste_direction = ["N","S","E","W"] #On prend la première lettre de chaque direction (N pour nord par exemple)

        depart = liste_direction[randint(0,3)]
        liste_direction.remove(depart)

        print(liste_direction)
        
        arrivee = liste_direction[randint(0,2)]

        vehicule = Vehicule(depart, arrivee, False)

        if depart == "N":
            queue_nord.put(vehicule)
            print(f"Véhicule Nord ajouté : {vehicule}")
        elif depart == "S":
            queue_sud.put(vehicule)
            print(f"Véhicule Sud ajouté : {vehicule}")
        elif depart == "E":
            queue_est.put(vehicule)
            print(f"Véhicule Est ajouté : {vehicule}")
        else:
            queue_ouest.put(vehicule)
            print(f"Véhicule Ouest ajouté : {vehicule}")

        time.sleep(2) #temps entre chaque généraation de véhicule


if __name__ == "__main__":
    # Créer un Manager pour partager les files de messages
    with Manager() as manager:
        # Créer les files de messages partagées
        queue_nord = manager.Queue()
        queue_sud = manager.Queue()
        queue_est = manager.Queue()
        queue_ouest = manager.Queue()

        # Démarrer le processus de génération de trafic
        Process(target=generation_trafic_normal, args=(queue_nord, queue_sud, queue_est, queue_ouest)).start()

        # Garder le programme principal en vie
        while True:
            time.sleep(1)
