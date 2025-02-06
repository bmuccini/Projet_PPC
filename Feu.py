class Feu:

    def __init__(self, direction):
        self.direction= direction

        self.couleur = "rouge" #On l'initialise  à rouge pour la sécurité

        self.positionnement_feu ()

    def positionnement_feu (self):
        if self.direction == "N":
            self.position_x = 520
            self.position_y = 270

        elif self.direction == "S":
            self.position_x = 680
            self.position_y = 510
        
        elif self.direction == "E":
            self.position_x = 710
            self.position_y = 320
         
        else :
            self.position_x = 470
            self.position_y = 480

    def rouge(self):
        self.couleur = "rouge"
    
    def vert(self):
        self.couleur = "vert"


