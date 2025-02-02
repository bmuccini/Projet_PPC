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

# Dimensions des routes
ROAD_WIDTH = 200  # Largeur chaque route
LANE_WIDTH = ROAD_WIDTH // 2  # Largeur une voie

# Position du carrefour
CROSSROAD_X = WIDTH // 2 - ROAD_WIDTH // 2
CROSSROAD_Y = HEIGHT // 2 - ROAD_WIDTH // 2

# États initiaux des feux et véhicules
traffic_lights = {"N": "rouge", "S": "rouge", "E": "vert", "W": "vert"}
vehicles = []

# Fonction pour dessiner les routes
def draw_roads():
    # Route horizontale
    pygame.draw.rect(screen, GRAY, (0, CROSSROAD_Y, WIDTH, ROAD_WIDTH))
    # Route verticale
    pygame.draw.rect(screen, GRAY, (CROSSROAD_X, 0, ROAD_WIDTH, HEIGHT))

    # Lignes séparatrices des voies
    pygame.draw.line(screen, WHITE, (0, CROSSROAD_Y + LANE_WIDTH), (WIDTH, CROSSROAD_Y + LANE_WIDTH), 2)
    pygame.draw.line(screen, WHITE, (CROSSROAD_X + LANE_WIDTH, 0), (CROSSROAD_X + LANE_WIDTH, HEIGHT), 2)

# Fonction pour dessiner les feux
def draw_lights():
    positions = {
        "N": (CROSSROAD_X + ROAD_WIDTH // 4 -30, CROSSROAD_Y - 30),
        "S": (CROSSROAD_X + ROAD_WIDTH // 4 + 130, CROSSROAD_Y + ROAD_WIDTH + 10),
        "E": (CROSSROAD_X + ROAD_WIDTH + 10, CROSSROAD_Y + ROAD_WIDTH // 4 - 30),
        "W": (CROSSROAD_X - 30, CROSSROAD_Y + ROAD_WIDTH // 4 + 130)
    }
    for direction, (x, y) in positions.items():
        color = GREEN if traffic_lights[direction] == "vert" else RED
        pygame.draw.circle(screen, color, (x, y), 15)

# Fonction pour dessiner les véhicules
def draw_vehicles():
    for vehicle in vehicles:
        depart, arrivee, prioritaire = vehicle
        x, y = get_vehicle_position(depart)
        color = (0, 0, 255) if not prioritaire else (255, 255, 0)  # Bleu pour normal, Jaune pour prioritaire
        pygame.draw.rect(screen, color, (x, y, 20, 10))

# Fonction pour obtenir la position initiale du véhicule
def get_vehicle_position(direction):
    positions = {
        "N": (CROSSROAD_X + ROAD_WIDTH // 4, CROSSROAD_Y - 50),
        "S": (CROSSROAD_X + ROAD_WIDTH // 4, CROSSROAD_Y + ROAD_WIDTH + 50),
        "E": (CROSSROAD_X + ROAD_WIDTH + 50, CROSSROAD_Y + ROAD_WIDTH // 4),
        "W": (CROSSROAD_X - 50, CROSSROAD_Y + ROAD_WIDTH // 4)
    }
    return positions.get(direction, (WIDTH // 2, HEIGHT // 2))

# Fonction pour recevoir les mises à jour de `coordinator.py`
def receive_updates():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 65433))
        s.listen()
        print("🖥️ `display.py` en attente des mises à jour...")
        while True:
            conn, _ = s.accept()
            with conn:
                data = conn.recv(4096)
                if data:
                    update = pickle.loads(data)
                    global traffic_lights, vehicles
                    traffic_lights = update["lights"]
                    vehicles = update["vehicles"]

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

# Quitte Pygame
pygame.quit()