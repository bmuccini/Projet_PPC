import pygame

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

# Fonction pour dessiner les routes
def draw_roads():
    # Route horizontale
    pygame.draw.rect(screen, GRAY, (0, CROSSROAD_Y, WIDTH, ROAD_WIDTH))
    # Route verticale
    pygame.draw.rect(screen, GRAY, (CROSSROAD_X, 0, ROAD_WIDTH, HEIGHT))

    # Lignes séparatrices des voies
    pygame.draw.line(screen, WHITE, (0, CROSSROAD_Y + LANE_WIDTH), (WIDTH, CROSSROAD_Y + LANE_WIDTH), 2)
    pygame.draw.line(screen, WHITE, (CROSSROAD_X + LANE_WIDTH, 0), (CROSSROAD_X + LANE_WIDTH, HEIGHT), 2)

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

    # Mets à jour l'affichage
    pygame.display.flip()

# Quitte Pygame
pygame.quit()