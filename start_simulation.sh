#!/bin/bash

echo "Démarrage de la simulation du carrefour..."


python clear_queues.py
python shared_memory.py

sleep 1
# Exécuter les processus en arrière-plan (& permet de ne pas bloquer le terminal)

python3 display.py &
DISPLAY_PID=$!

sleep 3

python3 lights.py &
LIGHTS_PID=$!

python3 priority_trafic_gen.py &
PRIORITY_PID=$!

python3 normal_trafic_gen.py &
NORMAL_PID=$!

python3 coordinator.py &
COORDINATOR_PID=$!

echo "Tous les processus sont lancés !"

# Attendre que tous les processus se terminent
wait $DISPLAY_PID
wait $LIGHTS_PID
wait $PRIORITY_PID
wait $NORMAL_PID
wait $COORDINATOR_PID

echo "Simulation terminée."



# Commander à écrire dans le terminal

# chmod +x start_simulation.sh   # Donne les permissions d’exécution
# ./start_simulation.sh   # Lance le script
