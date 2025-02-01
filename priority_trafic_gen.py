import sysv_ipc
from Vehicule import Vehicule
from random import randint
import time
import pickle


# Clés pour les files de message qui doivent etre les meme que celles pour les véhicules normaux
KEY_NORD = 1000
KEY_SUD = 1001
KEY_EST = 1002
KEY_OUEST = 1003

#Ouvre les files de messages
def ouvrir_files_messages():
    try:
        queue_nord = sysv_ipc.MessageQueue(KEY_NORD)
        queue_sud = sysv_ipc.MessageQueue(KEY_SUD)
        queue_est = sysv_ipc.MessageQueue(KEY_EST)
        queue_ouest = sysv_ipc.MessageQueue(KEY_OUEST)
        return queue_nord, queue_sud, queue_est, queue_ouest
    except sysv_ipc.ExistentialError:
        print("Erreur : Les files de messages n'existent pas.")
        exit(1)

# Genère des véhicules prioritaires et les ajoutes aux files de messages
def generation_trafic_prioritaire(queue_nord, queue_sud, queue_est, queue_ouest):

    #Creation des vehicules
    while True :
        liste_direction = ["N","S","E","W"]  # Doit etre dans la boucle pour que la taille de la liste reste constante
        depart = liste_direction[randint(0,3)]
        liste_direction.remove(depart)
        
        arrivee = liste_direction[randint(0,2)]

        vehicule = Vehicule(depart, arrivee, True) #True pour signifier véhicule prioritaire
        message = pickle.dumps(vehicule)  # Sérialiser avec pickle

        if depart == "N":
            queue_nord.send(message)
            print(f"Véhicule prioritaire Nord ajouté : {vehicule}")
        elif depart == "S":
            queue_sud.send(message)
            print (f"Véhicule prioritaire Sud ajouté : {vehicule}")
        elif depart == "S":
            queue_est.send(message)
            print (f"Véhicule prioritaire Est ajouté : {vehicule}")
        else:
            queue_ouest.send(message)
            print (f"Véhicule prioritaire Ouest ajouté : {vehicule}")

        time.sleep(6) #temps entre chaque généraation de véhicule prioritaire


if __name__ == "__main__":
    # Ouvrir les files de messages
    queue_nord, queue_sud, queue_est, queue_ouest = ouvrir_files_messages()

    # Démarrer la génération de trafic prioritaire
    generation_trafic_prioritaire(queue_nord, queue_sud, queue_est, queue_ouest)

