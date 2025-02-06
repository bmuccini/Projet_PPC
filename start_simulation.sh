#!/bin/bash

echo "Démarrage de la simulation du carrefour..."

# Exécuter les processus en arrière-plan (& permet de ne pas bloquer le terminal)
python3 display.py &
DISPLAY_PID=$!

sleep 1

python3 lights.py &
LIGHTS_PID=$!

python3 coordinator.py &
COORDINATOR_PID=$!

python3 normal_trafic_gen.py &
NORMAL_PID=$!

python3 priority_trafic_gen.py &
PRIORITY_PID=$!

echo "Tous les processus sont lancés !"

# Attendre que tous les processus se terminent
wait $DISPLAY_PID
wait $LIGHTS_PID
wait $COORDINATOR_PID
wait $NORMAL_PID
wait $PRIORITY_PID

echo "Simulation terminée."



# Commander à écrire dans le terminal

# chmod +x start_simulation.sh   # Donne les permissions d’exécution
# ./start_simulation.sh   # Lance le script
