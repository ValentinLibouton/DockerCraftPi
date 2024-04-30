FROM openjdk:17-slim

WORKDIR /minecraft

RUN apt-get update && apt-get upgrade -y && apt-get install -y wget nano python3 python3-pip screen git && apt-get clean && rm -rf /var/lib/apt/lists/*

# Insérer ci-dessous le lien de la version du serveur minecraft que vous désiez
RUN wget https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/464/downloads/paper-1.20.4-464.jar -O papermc.jar

#Plugins à installer (option)
RUN mkdir -p /minecraft/plugins
RUN wget -O /minecraft/plugins/LuckPerms-Bukkit.jar  https://download.luckperms.net/1534/bukkit/loader/LuckPerms-Bukkit-5.4.121.jar

# Accept CLUF Minecraft
RUN echo "eula=true" > eula.txt

# Minecraft server port (si vous voulez ajouter plusieurs serveurs en parralèle, choisissez des ports différents pour chacun (25566, 25567,...)
EXPOSE 25565

COPY start-minecraft.sh /minecraft/
COPY server.properties /minecraft/server.properties

# start-minecraft.sh est le petit programme que Docker va autormatiquement exécuter lors de son démarrage
RUN chmod +x /minecraft/start-minecraft.sh
ENTRYPOINT ["/minecraft/start-minecraft.sh"]
