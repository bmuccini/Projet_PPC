import pygame

class Feu:

    def __init__(self, direction):
        self.direction= direction

        self.couleur = "rouge" #On l'initialise  à rouge pour la sécurité

        self.positionnement_feu ()

    def positionnement_feu (self):
        if self.direction == "N":
            self.position_x = 0
            self.position_y = 0

        elif self.direction == "S":
            self.position_x = 0
            self.position_y = 0
        
        elif self.direction == "E":
            self.position_x = 0
            self.position_y = 0
         
        else :
            self.position_x = 0
            self.position_y = 0

    def rouge(self):
        self.couleur = "rouge"
    
    def vert(self):
        self.couleur = "vert"


