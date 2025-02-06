from Feu import Feu
import time
import sysv_ipc
import threading
import socket
from shared_memory import create_shared_memory, get_shared_lights, set_shared_lights

SOCKET_PORT = 65432

class TrafficLight:
    def __init__(self):
        self.shm = create_shared_memory()
        self.priority_event = threading.Event()
        self.priority_direction = None
        self._setup_socket_server()
        #self.cycle_paused = False  # Flag pour gérer l'interruption

        self.feux = get_shared_lights(self.shm)

        self.feu_N = self.feux["N"]
        self.feu_S = self.feux["S"]
        self.feu_E = self.feux["E"]
        self.feu_W = self.feux["W"]

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

        for feu in self.feux.values() :
            feu.rouge()

        self.feux[self.priority_direction].vert()

        set_shared_lights(self.shm, self.feux)
        print(f"🚨 FEU {self.priority_direction} VERT (5s)")
        time.sleep(5)

        #Tous les feux rouges
        for feu in self.feux.values() :
            feu.rouge()
        set_shared_lights(self.shm, self.feux)
        print("🔴 Tous les feux rouges (1s)")
        time.sleep(1)

        self.priority_event.clear()

    def normal_cycle(self):

        self.feu_N.vert()
        self.feu_S.vert()
        self.feu_E.rouge()
        self.feu_W.rouge()
        feux = {"N": self.feu_N, "S": self.feu_S, "E": self.feu_E, "W": self.feu_W}
        set_shared_lights(self.shm, feux)
        print (f"Feux verts Nord et Sud")
        time.sleep (5)

        self.feu_N.rouge()
        self.feu_S.rouge()
        self.feu_E.rouge()
        self.feu_W.rouge()
        feux = {"N": self.feu_N, "S": self.feu_S, "E": self.feu_E, "W": self.feu_W}
        set_shared_lights(self.shm, feux)
        print(f"Tous les feux sont rouges")
        time.sleep (2)

        self.feu_N.rouge()
        self.feu_S.rouge()
        self.feu_E.vert()
        self.feu_W.vert()
        feux = {"N": self.feu_N, "S": self.feu_S, "E": self.feu_E, "W": self.feu_W}
        set_shared_lights(self.shm, feux)
        print (f"Feux verts Est et Ouest")
        time.sleep (5)

        self.feu_N.rouge()
        self.feu_S.rouge()
        self.feu_E.rouge()
        self.feu_W.rouge()
        feux = {"N": self.feu_N, "S": self.feu_S, "E": self.feu_E, "W": self.feu_W}
        set_shared_lights(self.shm, feux)
        print(f"Tous les feux sont rouges")
        time.sleep (2)


if __name__ == "__main__":
    TrafficLight().run_cycle()

