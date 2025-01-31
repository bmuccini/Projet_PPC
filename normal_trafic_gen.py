from Vehicule import Vehicule
from random import randint
import time

def generation_trafic_normal():

    liste_direction = ["N","S","E","W"] #On prend la première lettre de chaque direction (N pour nord par exemple)

    #Creation des vehicules
    while True :
        depart = liste_direction[randint(0,3)]
        liste_direction.remove(depart)
        
        arrivee = liste_direction[randint(0,2)]

        vehicule = Vehicule(depart, arrivee, False)

        time.sleep(2) #temps entre chaque généraation de véhicule
