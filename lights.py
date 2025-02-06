from Feu import Feu
import time
import sysv_ipc
import threading
import socket
from shared_memory import connect_to_shared_memory, get_shared_lights, set_shared_lights

SOCKET_PORT = 65432

class TrafficLight:
    def __init__(self):
        self.shm = connect_to_shared_memory()
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
        """Main loop that runs forever, handling priority vs normal cycles."""
        while True:
            if self.priority_event.is_set():
                self._handle_priority()
            else:
                self.normal_cycle()

    def _handle_priority(self):
        """Handles the 'priority' phase (e.g. ambulance) by making the chosen direction green."""
        self.feux = get_shared_lights(shm=self.shm)

        # Set all lights red
        for feu in self.feux.values():
            feu.rouge()

        # The priority direction turns green
        self.feux[self.priority_direction].vert()

        # Update shared memory
        set_shared_lights(self.shm, self.feux)
        print(f"🚨 FEU {self.priority_direction} VERT (5s)")
        time.sleep(5)

        # Turn all lights red again
        for feu in self.feux.values():
            feu.rouge()
        set_shared_lights(self.shm, self.feux)
        print("🔴 Tous les feux rouges (1s)")
        time.sleep(1)

        # Clear the event so future normal cycles can proceed
        self.priority_event.clear()

    def normal_cycle(self):
        """Runs the standard traffic light cycle, but breaks early if priority_event is set."""
        # Step 1: North & South = green, East & West = red
        self.feu_N.vert()
        self.feu_S.vert()
        self.feu_E.rouge()
        self.feu_W.rouge()
        feux = {"N": self.feu_N, "S": self.feu_S, "E": self.feu_E, "W": self.feu_W}
        set_shared_lights(self.shm, feux)
        print("Feux verts Nord et Sud")
        self.wait_with_priority_check(5)
        if self.priority_event.is_set():
            return  # Stop normal cycle if priority is triggered

        # Step 2: All red
        self.feu_N.rouge()
        self.feu_S.rouge()
        self.feu_E.rouge()
        self.feu_W.rouge()
        feux = {"N": self.feu_N, "S": self.feu_S, "E": self.feu_E, "W": self.feu_W}
        set_shared_lights(self.shm, feux)
        print("Tous les feux sont rouges")
        self.wait_with_priority_check(1)
        if self.priority_event.is_set():
            return

        # Step 3: East & West = green, North & South = red
        self.feu_N.rouge()
        self.feu_S.rouge()
        self.feu_E.vert()
        self.feu_W.vert()
        feux = {"N": self.feu_N, "S": self.feu_S, "E": self.feu_E, "W": self.feu_W}
        set_shared_lights(self.shm, feux)
        print("Feux verts Est et Ouest")
        self.wait_with_priority_check(5)
        if self.priority_event.is_set():
            return

        # Step 4: All red again
        self.feu_N.rouge()
        self.feu_S.rouge()
        self.feu_E.rouge()
        self.feu_W.rouge()
        feux = {"N": self.feu_N, "S": self.feu_S, "E": self.feu_E, "W": self.feu_W}
        set_shared_lights(self.shm, feux)
        print("Tous les feux sont rouges")
        self.wait_with_priority_check(1)
        if self.priority_event.is_set():
            return

    def wait_with_priority_check(self, duration, check_interval=0.1):
        """
        Sleeps for `duration` seconds, but checks `self.priority_event`
        every `check_interval` seconds to break early if needed.
        """
        end_time = time.time() + duration
        while time.time() < end_time:
            if self.priority_event.is_set():
                return  # Abort immediately if we have priority
            time.sleep(check_interval)


if __name__ == "__main__":
    TrafficLight().run_cycle()

