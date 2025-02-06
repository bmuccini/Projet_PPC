import pygame
import socket
import threading
import pickle
from Feu import Feu
from Vehicule import Vehicule

pygame.init()

# Dimensions de la fenêtre

WIDTH, HEIGHT = 1200, 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Dimensions des routes
ROAD_WIDTH = 200  # Largeur chaque route
LANE_WIDTH = ROAD_WIDTH // 2  # Largeur une voie

# Position du carrefour
CROSSROAD_X = WIDTH // 2 - ROAD_WIDTH // 2
CROSSROAD_Y = HEIGHT // 2 - ROAD_WIDTH // 2


class Display() : 

    def __init__(self):
        #pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simulation Carrefour")
        self._receive_updates()
        self.feux = {}
        self.liste_vehicules = []


    # Fonction pour dessiner les routes
    def draw_roads(self):
        # Route horizontale
        pygame.draw.rect(self.screen, GRAY, (0, CROSSROAD_Y, WIDTH, ROAD_WIDTH))
        # Route verticale
        pygame.draw.rect(self.screen, GRAY, (CROSSROAD_X, 0, ROAD_WIDTH, HEIGHT))

        # Lignes séparatrices des voies
        pygame.draw.line(self.screen, WHITE, (0, CROSSROAD_Y + LANE_WIDTH), (WIDTH, CROSSROAD_Y + LANE_WIDTH), 2)
        pygame.draw.line(self.screen, WHITE, (CROSSROAD_X + LANE_WIDTH, 0), (CROSSROAD_X + LANE_WIDTH, HEIGHT), 2)


    def _receive_updates(self):
 
        def listener():
    
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', 65435))
                s.listen()
                print("🖥️ `display.py` en attente des mises à jour...")
                while True:
                    try:
                        conn, _ = s.accept()
                        with conn:
                            data = conn.recv(4096)
                            if data:
                                update = pickle.loads(data)
                            
                                self.feux = update["lights"]
                                self.liste_vehicules = update["vehicules"]
                    except Exception as e:
                        print(f"Erreur de réception de données: {e}")

        threading.Thread(target=listener, daemon=True).start()

    # Fonction pour dessiner les feux
    def draw_lights(self):

        if not self.feux:  # pour éviter les erreurs quand aucun feu n'est disponible
            return
        
        for feu in self.feux.values() :
            if feu.couleur == "vert":
                couleur = GREEN
            else :
                couleur = RED

            pygame.draw.circle(self.screen, couleur, (feu.position_x, feu.position_y), 15)

    # Fonction pour dessiner les véhicules
    def draw_vehicles(self):
           if not self.liste_vehicules:  # pour éviter les erreurs quand aucun véhicule n'est disponible
               return
           
           for vehicule in self.liste_vehicules :

            if vehicule.prioritaire == True :
                couleur = BLUE
            else:
                couleur = YELLOW
            
            pygame.draw.rect(self.screen, couleur, (vehicule.position_x, vehicule.position_y, 20, 20))


# Boucle principale
display = Display()

running = True
while running:
  
    for event in pygame.event.get():  # Parcoure et récupère les événements utilisateur
        if event.type == pygame.QUIT:  # Vérifie si l'événement est une demande de fermeture
            running = False

    # Fond d'écran noir
    display.screen.fill(BLACK)

    # Dessine les routes
    display.draw_roads()


    display.draw_lights()
    display.draw_vehicles()

    # Mets à jour l'affichage
    pygame.display.flip()
    pygame.time.delay(30)  # Rafraîchissement à 30 FPS
    pygame.time.wait(50)

# Quitte Pygame
pygame.quit()