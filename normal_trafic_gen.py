from multiprocessing import Queue
from Vehicule import Vehicule
from random import randint
import time

# Taille des files de messages
QUEUE_SIZE = 10

# Files de messages pour les 4 directions
queue_nord = Queue(QUEUE_SIZE)
queue_sud = Queue(QUEUE_SIZE)
queue_est = Queue(QUEUE_SIZE)
queue_ouest = Queue(QUEUE_SIZE)


def generation_trafic_normal():

    

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
    generation_trafic_normal()