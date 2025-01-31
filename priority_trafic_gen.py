from multiprocessing import Queue
import time
from random import randint
from Vehicule import Vehicule


def generation_trafic_prioritaire():

    liste_direction = ["N","S","E","W"]

    #Creation des vehicules
    while True :
        depart = liste_direction[randint(0,3)]
        liste_direction.remove(depart)
        
        arrivee = liste_direction[randint(0,2)]

        vehicule = Vehicule(depart, arrivee, True) #True pour signifier véhicule prioritaire

        time.sleep(12) #temps entre chaque généraation de véhicule prioritaire





