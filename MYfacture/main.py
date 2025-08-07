import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
from fpdf import FPDF
import webbrowser

class FacturationApp(tk.Tk):
    PROFILE_FILE = "profil_entreprise.json"

    def __init__(self):
        super().__init__()
        self.title("Logiciel de Facturation")
        self.geometry("800x600")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.profil_frame = ttk.Frame(self.notebook)
        self.facture_frame = ttk.Frame(self.notebook)
        self.historique_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.profil_frame, text="Profil Société")
        self.notebook.add(self.facture_frame, text="Nouvelle Facture")
        self.notebook.add(self.historique_frame, text="Historique")

        self.create_profil_form()
        self.create_facture_form()
        self.create_historique_view()

    def create_profil_form(self):
        frame = self.profil_frame

        labels = ["Nom de la société", "Adresse", "Téléphone", "E-mail", "Numéro SIRET", "Logo"]
        self.entries = {}

        for i, label_text in enumerate(labels[:-1]):
            label = ttk.Label(frame, text=label_text)
            label.grid(row=i, column=0, sticky='w', padx=10, pady=5)
            entry = ttk.Entry(frame, width=50)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label_text] = entry

        # Logo upload
        logo_label = ttk.Label(frame, text="Logo")
        logo_label.grid(row=len(labels)-1, column=0, sticky='w', padx=10, pady=5)
        self.logo_path_var = tk.StringVar()
        logo_entry = ttk.Entry(frame, textvariable=self.logo_path_var, width=50, state='readonly')
        logo_entry.grid(row=len(labels)-1, column=1, padx=10, pady=5)
        logo_button = ttk.Button(frame, text="Charger logo", command=self.load_logo)
        logo_button.grid(row=len(labels)-1, column=2, padx=10, pady=5)

        # Save button
        save_button = ttk.Button(frame, text="Sauvegarder", command=self.save_profile)
        save_button.grid(row=len(labels), column=1, pady=20)

        self.load_profile()

    def load_logo(self):
        file_path = filedialog.askopenfilename(title="Choisir un logo", filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            self.logo_path_var.set(file_path)

    def save_profile(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        data["Logo"] = self.logo_path_var.get()
        try:
            with open(self.PROFILE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Succès", "Profil sauvegardé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {e}")

    def load_profile(self):
        if os.path.exists(self.PROFILE_FILE):
            try:
                with open(self.PROFILE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for key, entry in self.entries.items():
                    entry.delete(0, tk.END)
                    entry.insert(0, data.get(key, ""))
                self.logo_path_var.set(data.get("Logo", ""))
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement du profil : {e}")

    def create_facture_form(self):
        frame = self.facture_frame
        
        # Add client info fields above the product list
        client_labels = ["Nom du client", "Adresse client", "Téléphone client", "E-mail client"]
        self.client_vars = {}
        for i, label_text in enumerate(client_labels):
            ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky='w', padx=10, pady=2)
            var = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=var, width=50)
            entry.grid(row=i, column=1, columnspan=4, sticky='w', padx=10, pady=2)
            self.client_vars[label_text] = var

        # Adjust the starting row for product list to be after client info
        product_start_row = len(client_labels) + 1

        columns = ("Produit", "Prix Unitaire HT", "Quantité", "TVA (%)", "Remise (%)", "Total HT")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=product_start_row, column=0, columnspan=8, padx=10, pady=10, sticky='nsew')

        labels = ["Produit", "Prix Unitaire HT", "Quantité", "TVA (%)", "Remise (%)"]
        self.entry_vars = {}
        for i, label_text in enumerate(labels):
            ttk.Label(frame, text=label_text).grid(row=product_start_row+1, column=i, padx=5, pady=5)
            var = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=var, width=15)
            entry.grid(row=product_start_row+2, column=i, padx=5, pady=5)
            self.entry_vars[label_text] = var

        add_button = ttk.Button(frame, text="Ajouter ligne", command=self.add_product_line)
        add_button.grid(row=product_start_row+2, column=len(labels), padx=5, pady=5)

        delete_button = ttk.Button(frame, text="Supprimer ligne", command=self.delete_product_line)
        delete_button.grid(row=product_start_row+2, column=len(labels)+1, padx=5, pady=5)

        pdf_button = ttk.Button(frame, text="Générer PDF", command=self.generate_pdf)
        pdf_button.grid(row=product_start_row+3, column=0, padx=10, pady=10, sticky='w')

        self.total_ht_var = tk.StringVar(value="0.00")
        self.total_tva_var = tk.StringVar(value="0.00")
        self.total_remise_var = tk.StringVar(value="0.00")
        self.total_ttc_var = tk.StringVar(value="0.00")

        ttk.Label(frame, text="Total HT :").grid(row=product_start_row+3, column=3, sticky='e')
        ttk.Label(frame, textvariable=self.total_ht_var).grid(row=product_start_row+3, column=4, sticky='w')
        ttk.Label(frame, text="Total TVA :").grid(row=product_start_row+4, column=3, sticky='e')
        ttk.Label(frame, textvariable=self.total_tva_var).grid(row=product_start_row+4, column=4, sticky='w')
        ttk.Label(frame, text="Total Remise :").grid(row=product_start_row+5, column=3, sticky='e')
        ttk.Label(frame, textvariable=self.total_remise_var).grid(row=product_start_row+5, column=4, sticky='w')
        ttk.Label(frame, text="Total TTC :").grid(row=product_start_row+6, column=3, sticky='e')
        ttk.Label(frame, textvariable=self.total_ttc_var).grid(row=product_start_row+6, column=4, sticky='w')

    def delete_product_line(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner une ligne à supprimer.")
            return
        for item in selected_item:
            self.tree.delete(item)
        self.update_totals()

    def generate_pdf(self):
        from datetime import datetime
        profil = {}
        if os.path.exists(self.PROFILE_FILE):
            with open(self.PROFILE_FILE, 'r', encoding='utf-8') as f:
                profil = json.load(f)

        factures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'factures')
        if not os.path.exists(factures_dir):
            os.makedirs(factures_dir)
            
        # Demander le nom du fichier PDF
        default_filename = f"facture_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        custom_filename = tk.simpledialog.askstring(
            "Nom du fichier", 
            "Entrez un nom pour votre facture (sans l'extension .pdf) :",
            initialvalue=default_filename
        )
        
        # Si l'utilisateur annule, utiliser le nom par défaut
        if custom_filename is None or custom_filename.strip() == "":
            custom_filename = default_filename
        
        # Nettoyer le nom de fichier pour éviter les caractères invalides
        import re
        custom_filename = re.sub(r'[\\/*?:"<>|]', "_", custom_filename)
        
        # Chemin complet du fichier
        filename = os.path.join(factures_dir, f"{custom_filename}.pdf")

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font('Arial', 'B', 16)

        logo_path = profil.get("Logo", "")
        if logo_path and os.path.exists(logo_path):
            pdf.image(logo_path, 10, 8, 33)

        pdf.cell(0, 10, profil.get("Nom de la société", ""), ln=True, align='C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, profil.get("Adresse", ""), ln=True, align='C')
        pdf.cell(0, 10, f"Téléphone: {profil.get('Téléphone', '')} - E-mail: {profil.get('E-mail', '')}", ln=True, align='C')
        pdf.cell(0, 10, f"SIRET: {profil.get('Numéro SIRET', '')}", ln=True, align='C')

        pdf.ln(10)

        # Add client information section
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "Informations Client", ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, f"Nom: {self.client_vars.get('Nom du client').get()}", ln=True)
        pdf.cell(0, 8, f"Adresse: {self.client_vars.get('Adresse client').get()}", ln=True)
        pdf.cell(0, 8, f"Téléphone: {self.client_vars.get('Téléphone client').get()}", ln=True)
        pdf.cell(0, 8, f"E-mail: {self.client_vars.get('E-mail client').get()}", ln=True)

        pdf.ln(10)

        pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d/%m/%Y')}", ln=True)

        headers = ["Produit", "Prix Unitaire HT", "Quantité", "TVA (%)", "Remise (%)", "Total HT"]
        col_widths = [50, 30, 20, 20, 20, 30]

        pdf.set_font('Arial', 'B', 12)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1, align='C')
        pdf.ln()

        pdf.set_font('Arial', '', 12)
        for child in self.tree.get_children():
            vals = self.tree.item(child)['values']
            for i, val in enumerate(vals):
                pdf.cell(col_widths[i], 10, str(val), border=1)
            pdf.ln()

        pdf.ln(5)

        euro = chr(128)
        pdf.cell(0, 10, f"Total HT: {self.total_ht_var.get()} {euro}", ln=True, align='R')
        pdf.cell(0, 10, f"Total Remise: {self.total_remise_var.get()} {euro}", ln=True, align='R')
        pdf.cell(0, 10, f"Total TVA: {self.total_tva_var.get()} {euro}", ln=True, align='R')
        pdf.cell(0, 10, f"Total TTC: {self.total_ttc_var.get()} {euro}", ln=True, align='R')

        pdf.output(filename)

        messagebox.showinfo("Succès", f"Facture générée et sauvegardée sous {filename}")

        self.load_invoice_history()

    def add_product_line(self):
        try:
            produit = self.entry_vars["Produit"].get()
            prix_ht = float(self.entry_vars["Prix Unitaire HT"].get())
            quantite = int(self.entry_vars["Quantité"].get())
            tva = float(self.entry_vars["TVA (%)"].get())
            remise = float(self.entry_vars["Remise (%)"].get() or 0)

            total_ht = prix_ht * quantite * (1 - remise / 100)

            self.tree.insert('', 'end', values=(produit, f"{prix_ht:.2f}", quantite, f"{tva:.2f}", f"{remise:.2f}", f"{total_ht:.2f}"))

            self.update_totals()

            for var in self.entry_vars.values():
                var.set("")

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour le prix, la quantité, la TVA et la remise.")

    def update_totals(self):
        total_ht = 0.0
        total_tva = 0.0
        total_remise = 0.0

        for child in self.tree.get_children():
            vals = self.tree.item(child)['values']
            prix_ht = float(vals[1])
            quantite = int(vals[2])
            tva = float(vals[3])
            remise = float(vals[4])

            line_ht = prix_ht * quantite
            line_remise = line_ht * remise / 100
            line_tva = (line_ht - line_remise) * tva / 100

            total_ht += line_ht
            total_remise += line_remise
            total_tva += line_tva

        total_ttc = total_ht - total_remise + total_tva

        self.total_ht_var.set(f"{total_ht:.2f}")
        self.total_remise_var.set(f"{total_remise:.2f}")
        self.total_tva_var.set(f"{total_tva:.2f}")
        self.total_ttc_var.set(f"{total_ttc:.2f}")

    # Ajoutez cette méthode après update_totals et avant le bloc if __name__ == "__main__"
    def create_historique_view(self):
        frame = self.historique_frame
        
        # Créer un Treeview pour afficher l'historique des factures
        columns = ("Date", "Numéro", "Client", "Total HT", "Total TTC")
        self.history_tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
            
        self.history_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Ajouter un bouton pour ouvrir la facture sélectionnée
        open_button = ttk.Button(frame, text="Ouvrir la facture", command=self.open_invoice)
        open_button.pack(pady=10)
        
        # Double-clic pour ouvrir une facture
        self.history_tree.bind("<Double-1>", lambda event: self.open_invoice())
        
        # Charger l'historique des factures
        self.load_invoice_history()
    
    def load_invoice_history(self):
        # Effacer l'historique actuel
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Obtenir le chemin absolu du dossier factures
        factures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'factures')
            
        # Vérifier si le dossier factures existe
        if not os.path.exists(factures_dir):
            return
            
        # Lister tous les fichiers PDF dans le dossier factures
        for filename in os.listdir(factures_dir):
            if filename.endswith('.pdf'):
                # Obtenir la date de création du fichier
                filepath = os.path.join(factures_dir, filename)
                from datetime import datetime
                import time
                
                # Obtenir la date de création du fichier
                creation_time = os.path.getctime(filepath)
                date_obj = datetime.fromtimestamp(creation_time)
                date_formatted = date_obj.strftime('%d/%m/%Y %H:%M')
                
                # Extraire le nom du client si possible (pour les nouveaux fichiers)
                client_name = "--"
                
                # Insérer dans l'historique
                self.history_tree.insert('', 'end', values=(date_formatted, filename, client_name, "--", "--"), tags=(filename,))
    
    def open_invoice(self):
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une facture à ouvrir.")
            return
            
        item = selected[0]
        filename = self.history_tree.item(item, 'values')[1]  # Le nom du fichier est dans la deuxième colonne
        factures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'factures')
        filepath = os.path.join(factures_dir, filename)
        
        if os.path.exists(filepath):
            webbrowser.open(filepath)
        else:
            messagebox.showerror("Erreur", f"Le fichier {filepath} n'existe pas.")

if __name__ == "__main__":
    app = FacturationApp()
    app.mainloop()