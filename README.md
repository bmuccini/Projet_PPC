## Projet_PPC : Simulation d'un Carrefour routier

## Description
Ce projet est une simulation multi-processus d'un carrefour routier géré par des feux de signalisation.  
Il modélise le passage des véhicules normaux et prioritaires.

## Fonctionnalités
- **Gestion des feux de signalisation** : alternance des feux et priorité aux véhicules d’urgence.  
- **Génération dynamique du trafic** : véhicules normaux et prioritaires apparaissent aléatoirement.  
- **Coordination des véhicules** : gestion des files d’attente et des priorités.  
- **Affichage en temps réel** : simulation graphique avec **Pygame**.  

## Architecture
Le projet repose sur plusieurs **processus indépendants** communiquant via **files de messages, mémoire partagée et sockets** :  
- `normal_trafic_gen.py` : génère le trafic normal.  
- `priority_trafic_gen.py` : génère le trafic prioritaire et envoie un signal aux feux.  
- `coordinator.py` : contrôle le passage des véhicules et met à jour l’affichage.  
- `lights.py` : gère les cycles des feux de signalisation.  
- `display.py` : affiche la simulation avec Pygame.  
- `shared_memory.py` : initialise et gère la mémoire partagée.  
- `clear_queues.py` : vide les files de messages.  

## Installation
### Prérequis
- Python 3  
- Bibliothèques : `pygame`, `sysv_ipc`, `pickle`  

Installez les dépendances avec :  
```bash  
pip install pygame  
pip install sysv_ipc  
```

## Exécution
Lancez le projet avec le script Bash:
```Bash
chmod +x start_simulation.sh  
./start_simulation.sh  
```

Arretez le programme avec le script suivant :  
```Bash
chmod +x stop_simulation.sh  
./stop_simulation.sh  
```

## Auteurs
Duran Rémi  
Muccini Bianca