# Redémarrage et extinction à distance
Pour permettre l'extinction et le redémarrage sans mot de passe, il faut changer les droits sur ces actions.  
Sur le raspberry faire:
```bash
sudo visudo
```
Dans le fichier visudo, taper ceci en remplaçant `username` par le nom d'utilisateur utilisé pour les connexions SSH. 
```bash
username ALL=(ALL) NOPASSWD: /sbin/shutdown, /sbin/reboot
```