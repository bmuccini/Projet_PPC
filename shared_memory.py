from multiprocessing import Manager

def create_shared_memory():
    """Fonction qui crée une mémoire partagée sous forme de dictionnaire géré par Manager().dict() pour stocker l'état des feux"""
    manager = Manager()
    shared_lights = manager.dict({  # multiprocessing.Manager().dict() permet de stocker plusieurs valeurs (feux N, S, E, W), mieux que Value() ou Array()
        "N": "rouge",
        "S": "rouge",  # C’est juste la valeur de départ au lancement du programme, ne signifie pas que le feu du sud restera toujours rouge
        "E": "vert",
        "W": "vert"
    })
    return shared_lights
