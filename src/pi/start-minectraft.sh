#!/bin/bash

# Obtenir la mémoire totale en gigaoctets
MEM_TOTAL_GB=$(awk '/MemTotal/ {print int($2/1024/1024)}' /proc/meminfo)
echo "MemTotal=$MEM_TOTAL_GB"

# Définir les paramètres de la JVM en fonction de la mémoire disponible
if [ "$MEM_TOTAL_GB" -ge "7" ]; then
    numbs=6
    tot=8
    JVM_OPTS="-Xms6G -Xmx6G"
elif [ "$MEM_TOTAL_GB" -ge "3" ]; then
    numbs=3
    tot=4
    JVM_OPTS="-Xms3G -Xmx3G"
else
    numbs=1
    tot=$MEM_TOTAL_GB
    JVM_OPTS="-Xms1G -Xmx1G"  # Fallback pour moins de 4 Go
fi

echo "Le serveur minecraft va démarrer avec $numbs de vos $tot Gb de RAM"
# Démarrer le serveur Minecraft dans une session screen nommée "minecraft"
screen -dmS minecraft java $JVM_OPTS -jar papermc.jar --nogui &
echo "Use: 'screen -r minecraft' to access the minecraft server teminal"

tail -f /dev/null
