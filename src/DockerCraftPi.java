import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class DockerCraftPi {
    private static DefaultTableModel tableModel;

    public static void main(String[] args) {
        JFrame frame = new JFrame("DockerCraftPi");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 400);
        frame.setLayout(new BorderLayout());

        // Création du modèle de tableau
        tableModel = new DefaultTableModel(new Object[]{"Nom du conteneur", "Statut", "Démarrer", "Arrêter"}, 0);
        JTable table = new JTable(tableModel) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return column >= 2; // Rend les cellules des boutons éditables
            }
        };

        // Boutons dans le tableau
        table.getColumn("Démarrer").setCellRenderer(new ButtonRenderer());
        table.getColumn("Démarrer").setCellEditor(new ButtonEditor(new JCheckBox()));
        table.getColumn("Arrêter").setCellRenderer(new ButtonRenderer());
        table.getColumn("Arrêter").setCellEditor(new ButtonEditor(new JCheckBox()));

        // Ajout de la table dans un JScrollPane
        JScrollPane scrollPane = new JScrollPane(table);
        frame.add(scrollPane, BorderLayout.CENTER);

        // Bouton de rafraîchissement
        JButton refreshButton = new JButton("Rafraîchir");
        refreshButton.addActionListener(e -> refreshTable());
        frame.add(refreshButton, BorderLayout.SOUTH);

        frame.setLocationRelativeTo(null);
        frame.setVisible(true);

        // Rafraîchir les données initiales
        refreshTable();
    }

    // Méthode pour rafraîchir la table
    private static void refreshTable() {
        try {
            Process process = new ProcessBuilder("docker", "ps", "--format", "{{.Names}} {{.Status}}").start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                String[] data = line.split(" ");
                tableModel.addRow(new Object[]{data[0], data[1], "Démarrer", "Arrêter"});
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}
