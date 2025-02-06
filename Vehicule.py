class Vehicule:

    def __init__(self, depart, arrivee, prioritaire = False):
        self.depart = depart
        self.arrivee = arrivee
        self.prioritaire = prioritaire
        
        if prioritaire :
            self.vitesse = 80
        else :
            self.vitesse = 50
        
        self.positionnement_vehicule()
        self.prochain_virage()

    def __repr__(self):
        return f"Véhicule({self.depart}->{self.arrivee}, prioritaire={self.prioritaire}), coords=({self.position_x}, {self.position_y})"


    def positionnement_vehicule(self):
        
        if self.depart == "N":
            self.orientation = "S"
            self.position_x = 550
            self.position_y = 10

        elif self.depart == "S":
            self.orientation = "N"
            self.position_x = 650
            self.position_y = 790
        
        elif self.depart == "E":
            self.orientation = "W"
            self.position_x = 1190
            self.position_y = 350
        
        else :
            self.orientation = "E"
            self.position_x = 10
            self.position_y = 450

    def avancer(self):

        if self.orientation == "N":
            self.position_y -= self.vitesse 
        
        if self.orientation == "S":
            self.position_y += self.vitesse 
        
        if self.orientation == "E":
            self.position_x += self.vitesse 
        
        if self.orientation == "W":
            self.position_x -= self.vitesse 

    
    def arreter(self):
        pass

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
    
    def prochain_virage (self):

        if (self.depart == "S" and self.arrivee == "N") or (self.depart == "N" and self.arrivee == "S") or (self.depart == "E" and self.arrivee == "W") or (self.depart == "W" and self.arrivee == "E"):
            self.virage = "face"

        if (self.depart == "S" and self.arrivee == "E") or (self.depart == "N" and self.arrivee == "W") or (self.depart == "E" and self.arrivee == "N") or (self.depart == "W" and self.arrivee == "S"):
            self.virage = "droite"

        if (self.depart == "S" and self.arrivee == "W") or (self.depart == "N" and self.arrivee == "E") or (self.depart == "E" and self.arrivee == "S") or (self.depart == "W" and self.arrivee == "N"):
            self.virage = "gauche"

    def avant_feu(self):
        if self.depart == "N":
            return 200 < self.position_y < 270
        if self.depart == "S":
            return 510 < self.position_y < 580
        if self.depart == "E":
            return 710 < self.position_x < 780
        if self.depart == "W":
            return 400 < self.position_x < 470
    
    def doit_arreter_derriere(self, vehicule):
        if self.depart != vehicule.depart:
            return False
        
        if self.depart == "N":
            distance = vehicule.position_y - self.position_y
            return 0 < distance <= self.vitesse + 10
        if self.depart == "S":
            distance = self.position_y - vehicule.position_y
            return 0 < distance <= self.vitesse + 10
        if self.depart == "E":
            distance = self.position_x - vehicule.position_x
            return 0 < distance <= self.vitesse + 10
        if self.depart == "W":
            distance = vehicule.position_x - self.position_x
            return 0 < distance <= self.vitesse + 10
        
