from multiprocessing import Manager

def create_shared_memory():
    """Crée un dictionnaire partagé pour stocker l'état des feux"""
    manager = Manager()
    shared_lights = manager.dict({  # multiprocessing.Manager().dict() permet de stocker plusieurs valeurs (feux N, S, E, W), mieux que Value() ou Array()
        "N": "rouge",
        "S": "rouge",
        "E": "vert",
        "W": "vert"
    })
    return shared_lights
