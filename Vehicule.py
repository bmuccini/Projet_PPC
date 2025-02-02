class Vehicule:

    def __init__(self, depart, arrivee, prioritaire = False):
        self.depart = depart
        self.arrivee = arrivee
        self.prioritaire = prioritaire

        #self.positionnement_voiture()

    def __repr__(self):
        return f"Véhicule({self.depart}->{self.arrivee}, prioritaire={self.prioritaire})"


"""    def positionnement_voiture(self):
        
        if self.depart == "N":
            self.orientation = "S"
            self.position_x = 0
            self.position_y = 0

        elif self.depart == "S":
            self.orientation = "N"
            self.position_x = 0
            self.position_y = 0
        
        elif self.depart == "E":
            self.orientation = "W"
            self.position_x = 0
            self.position_y = 0
        
        else :
            self.orientation = "E"
            self.position_x = 0
            self.position_y = 0

    def affichage_vehicule(self):
        #affichage du vehicule 
        print("hello")

    def avancer(self):

        if self.orientation == "N":
            self.position_y += 5
        
        if self.orientation == "S":
            self.position_y -= 5
        
        if self.orientation == "E":
            self.position_x += 5
        
        if self.orientation == "W":
            self.position_x -= 5

    
    def arreter(self):
        print("hello")

    def tourner_gauche (self):

        if self.orientation == "N":
            self.orientation = "W"
        
        if self.orientation == "S":
            self.orientation = "E"
        
        if self.orientation == "E":
            self.orientation = "N"
        
        if self.orientation == "W":
            self.orientation = "S"


    def tourner_droite (self):

        if self.orientation == "N":
            self.orientation = "E"
        
        if self.orientation == "S":
            self.orientation = "W"
        
        if self.orientation == "E":
            self.orientation = "S"
        
        if self.orientation == "W":
            self.orientation = "N"
    """