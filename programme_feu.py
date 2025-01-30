import time
from Feu import Feu

"""
C'est de la forme avec Feu qui est l'objet Feu
dico_feu = {"feu_N" : Feu, "feu_S" : Feu, "feu_E" : Feu, "feu_W" : Feu}
"""
def generation_feu():
    dico_feu = {}

    dico_feu["feu_N"] = Feu("N") #ici on donne la position nord 
    dico_feu["feu_S"] = Feu("S")
    dico_feu["feu_E"] = Feu("E")
    dico_feu["feu_W"] = Feu("W")

    return dico_feu


def changement_feu(dico_feu):
    feu_N = dico_feu["feu_N"] 
    feu_S = dico_feu["feu_S"] 
    feu_E = dico_feu["feu_E"] 
    feu_W = dico_feu["feu_W"] 

#Alternance des feux
    while True:
        feu_N.vert()
        feu_S.vert()
        feu_E.rouge()
        feu_W.rouge()
        time.sleep(10) #On prend un temps reglementaire
        feu_N.rouge()
        feu_S.rouge()
        feu_E.vert()
        feu_W.vert()
        time.sleep(10)

def priorite_traffic_feu(dico_feu, position):
    
    for feu in dico_feu.values() :
        
        if feu.position == position :
            feu.vert()
        else :
            feu.rouge()

