class Vehicule:

    def __init__(self, depart, arrivee, prioritaire):
        self.depart = depart
        self.arrivee = arrivee
        self.prioritaire = prioritaire

        self.positionnement_voiture()


    def positionnement_voiture(self):
        
        if self.depart == "N":
            self.orientation = "S"
            self.position_x 
            self.position_y

        elif self.depart == "S":
            self.orientation = "N"
            self.position_x
            self.position_y
        
        elif self.depart == "E":
            self.orientation = "W"
            self.position_x
            self.position_y
        
        else :
            self.orientation = "E"
            self.position_x
            self.position_y

    def affichage_vehicule(self):
        #affichage du vehicule 
        print("hello")

    def avancer(self):
        print("hello")
    
    def arreter(self):
        print("hello")

    def tourner_gauche (self):
        print("hello")

    def tourner_droite (self):
        print("hello")