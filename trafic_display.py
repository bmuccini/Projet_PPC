import pygame

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de carrefour")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Dimensions des routes
ROAD_WIDTH = 200  # Largeur de chaque route
LANE_WIDTH = ROAD_WIDTH // 2  # Largeur d'une voie

# Position du carrefour
CROSSROAD_X = WIDTH // 2 - ROAD_WIDTH // 2
CROSSROAD_Y = HEIGHT // 2 - ROAD_WIDTH // 2

# Fonction pour dessiner les routes
def draw_roads():
    # Route horizontale (West-East)
    pygame.draw.rect(screen, GRAY, (0, CROSSROAD_Y, WIDTH, ROAD_WIDTH))
    # Route verticale (North-South)
    pygame.draw.rect(screen, GRAY, (CROSSROAD_X, 0, ROAD_WIDTH, HEIGHT))

    # Lignes séparatrices des voies
    pygame.draw.line(screen, WHITE, (0, CROSSROAD_Y + LANE_WIDTH), (WIDTH, CROSSROAD_Y + LANE_WIDTH), 2)
    pygame.draw.line(screen, WHITE, (CROSSROAD_X + LANE_WIDTH, 0), (CROSSROAD_X + LANE_WIDTH, HEIGHT), 2)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacer l'écran
    screen.fill(BLACK)

    # Dessiner les routes
    draw_roads()

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()