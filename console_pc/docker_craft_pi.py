import paramiko, socket
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

def start_container(container_name, ssh):
    command = f"docker start {container_name}"
    stdin, stdout, stderr = ssh.exec_command(command)
    if stderr.read().decode():
        messagebox.showerror("Error", f"Failed to start {container_name}")
    else:
        messagebox.showinfo("Success", f"Container {container_name} started")
    #refresh_containers()

def stop_container(container_name, ssh):
    command = f"docker stop {container_name}"
    stdin, stdout, stderr = ssh.exec_command(command)
    if stderr.read().decode():
        messagebox.showerror("Error", f"Failed to stop {container_name}")
    else:
        messagebox.showinfo("Success", f"Container {container_name} stopped")
    #refresh_containers()

def on_double_click(event, tree, ssh):
    region = tree.identify("region", event.x, event.y)
    if region == "cell":
        col_id = tree.identify_column(event.x)
        row_id = tree.identify_row(event.y)
        item = tree.item(row_id)
        container_name = item['values'][0]  # Nom du conteneur
        if col_id == '#3':  # Colonne 'Start'
            start_container(container_name, ssh)
        elif col_id == '#4':  # Colonne 'Stop'
            stop_container(container_name, ssh)

def get_docker_containers(ssh_client):
    try:
        # Exécution de la commande pour obtenir les noms et statuts de tous les conteneurs
        stdin, stdout, stderr = ssh_client.exec_command('docker ps -a --format "{{.Names}} {{.Status}}"')
        # Lecture de la sortie de la commande
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if error:
            print("Erreur :", error)
            return None

        # Initialisation du dictionnaire pour stocker les données des conteneurs
        containers = {}
        # Découpage de chaque ligne de la sortie pour extraire les informations
        for line in output.splitlines():
            parts = line.split(None, 1)  # On divise la ligne en deux parties au premier espace
            if len(parts) == 2:  # S'assurer que la ligne est correctement divisée en deux parties
                name, status = parts
                containers[name] = status

        return containers
    except Exception as e:
        print("Erreur lors de l'exécution de la commande SSH :", e)
        return None

class SSHConnectionDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Host IP:").grid(row=0)
        tk.Label(master, text="SSH Port:").grid(row=1)
        tk.Label(master, text="Username:").grid(row=2)
        tk.Label(master, text="Password:").grid(row=3)

        self.ip_entry = tk.Entry(master)
        self.port_entry = tk.Entry(master)
        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show="*")

        self.ip_entry.grid(row=0, column=1)
        self.port_entry.grid(row=1, column=1)
        self.username_entry.grid(row=2, column=1)
        self.password_entry.grid(row=3, column=1)

        self.port_entry.insert(0, '22')
        self.username_entry.insert(0, 'pi')
        self.password_entry.insert(0, 'raspberry')

        # Bind the Enter key to the same function as the OK button
        self.bind("<Return>", self.apply)  # Bind Enter key to apply method


        return self.ip_entry  # initial focus

    def apply(self):
        self.result = (self.ip_entry.get(), int(self.port_entry.get()), self.username_entry.get(), self.password_entry.get())

    def cancel(self, event=None):
        print("User has cancelled the dialog.")
        root.deiconify()
        super().cancel()


def connect_ssh(root):
    dialog = SSHConnectionDialog(root, title="Connect to SSH")
    if dialog.result:
        host, port, username, password = dialog.result
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=host, port=port, username=username, password=password)
            messagebox.showinfo("Connection Info", "SSH Connection Successful")
            return ssh_client
        except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.SSHException, socket.timeout) as e:
            messagebox.showerror("Connection Error", f"Failed to connect to {host}:{port}. {str(e)}")
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
    return None

def main_app(ssh):
    def refresh_containers():
        """Fetch and display Docker containers."""
        containers_dict = get_docker_containers(ssh)
        for i in tree.get_children():
            tree.delete(i)  # Clear existing entries in the treeview
        if containers_dict:
            for name, status in containers_dict.items():
                # Insert data with a button placeholder
                tree.insert('', 'end', values=(name, status, 'Start', 'Stop'))
    #root.deiconify()
    root.title("Docker Management")
    root.geometry('600x400')

    # Setup Treeview
    columns = ('name', 'status', 'start', 'stop')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.heading('name', text='Name')
    tree.heading('status', text='Status')
    tree.heading('start', text='Start')
    tree.heading('stop', text='Stop')
    tree.column('name', width=150)
    tree.column('status', width=100)
    tree.column('start', width=100)
    tree.column('stop', width=100)
    tree.pack(expand=True, fill='both')

    # Bind the double-click event to handle Start/Stop commands
    tree.bind('<Double-1>', lambda event: on_double_click(event, tree, ssh))

    # Add a button to refresh the container list
    refresh_button = tk.Button(root, text="Refresh Containers", command=refresh_containers)
    refresh_button.pack()

    refresh_containers()  # Initial refresh of container data


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Docker Craft Pi")
    root.withdraw()


    ssh_client = connect_ssh(root)
    if ssh_client:
        main_app(ssh_client)

    root.mainloop()