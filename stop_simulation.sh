#!/bin/bash

echo "🛑 Arrêt de la simulation..."

# Trouver et tuer tous les processus Python liés à la simulation
pkill -f programme_feu.py
pkill -f normal_trafic_gen.py
pkill -f priority_trafic_gen.py
pkill -f coordinator.py

echo "✅ Tous les processus ont été arrêtés."



# Commandes à écrire dans le terminal

# chmod +x stop_simulation.sh   # Donne les permissions d’exécution
# ./stop_simulation.sh   # Lance le script pour arrêter tout
