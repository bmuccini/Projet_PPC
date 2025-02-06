import pygame
import socket
import threading
import pickle

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de carrefour")


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

###########
feux = {}
liste_vehicules = []

###############

# Fonction pour dessiner les routes
def draw_roads():
    # Route horizontale
    pygame.draw.rect(screen, GRAY, (0, CROSSROAD_Y, WIDTH, ROAD_WIDTH))
    # Route verticale
    pygame.draw.rect(screen, GRAY, (CROSSROAD_X, 0, ROAD_WIDTH, HEIGHT))

    # Lignes séparatrices des voies
    pygame.draw.line(screen, WHITE, (0, CROSSROAD_Y + LANE_WIDTH), (WIDTH, CROSSROAD_Y + LANE_WIDTH), 2)
    pygame.draw.line(screen, WHITE, (CROSSROAD_X + LANE_WIDTH, 0), (CROSSROAD_X + LANE_WIDTH, HEIGHT), 2)


def receive_updates():
    global feux, liste_vehicules
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 65433))
        s.listen()
        print("🖥️ `display.py` en attente des mises à jour...")
        while True:
            conn, _ = s.accept()
            with conn:
                data = conn.recv(4096)
                if data:
                    update = pickle.loads(data)
                 
                    #global traffic_lights, vehicles
                    feux = update["lights"]
                    liste_vehicules = update["vehicules"]

# Fonction pour dessiner les feux
def draw_lights():
    global feux
    
    for feu in feux.values() :
        if feu.couleur == "vert":
            couleur = GREEN
        else :
            couleur = RED

        pygame.draw.circle(screen, couleur, (feu.position_x, feu.position_y), 15)

# Fonction pour dessiner les véhicules
def draw_vehicles():
    global liste_vehicules

    for vehicule in liste_vehicules :

        if vehicule.prioritaire == True :
            couleur = BLUE
        else:
            couleur = YELLOW
        
        pygame.draw.rect(screen, couleur, (vehicule.position_x, vehicule.position_y, 20, 20))



# Lancer un thread pour écouter `coordinator.py`
threading.Thread(target=receive_updates, daemon=True).start()

# Boucle principale
running = True
while running:
  
    for event in pygame.event.get():  # Parcoure et récupère les événements utilisateur
        if event.type == pygame.QUIT:  # Vérifie si l'événement est une demande de fermeture
            running = False


    # Fond d'écran noir
    screen.fill(BLACK)

    # Dessine les routes
    draw_roads()


    draw_lights()
    draw_vehicles()

    # Mets à jour l'affichage
    pygame.display.flip()
    pygame.time.delay(30)  # Rafraîchissement à 30 FPS

# Quitte Pygame
pygame.quit()