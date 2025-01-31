from multiprocessing import Process, Manager
from normal_trafic_gen import queue_nord, queue_sud, queue_est, queue_ouest
import time


class coordinator:

    def __init__(self):
        self.bonjour = 1


    def lire_trafic(self):

        # Lire les véhicules des files de messages
        if not queue_nord.empty():
            self.queue_nord = queue_nord.get()

        if not queue_sud.empty():
            self.queue_sud = queue_sud.get()

        if not queue_est.empty():
            self.queue_est = queue_est.get()

        if not queue_ouest.empty():
            self.vehicule_ouest = queue_ouest.get()

        time.sleep(1)  # Vérifier les files toutes les secondes





