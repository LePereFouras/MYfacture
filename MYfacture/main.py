import customtkinter as ctk
import tkinter as tk # Keep tkinter for some specific functionalities if needed, but we'll primarily use ctk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
from fpdf import FPDF
import webbrowser
import time

# Change FacturationApp to inherit from ctk.CTk
class FacturationApp(ctk.CTk):
    PROFILE_FILE = "profil_entreprise.json"

    def __init__(self):
        super().__init__()
        self.title("MYfacture - Logiciel de Facturation")
        self.geometry("900x650")
        # ctk handles appearance mode and color themes differently
        ctk.set_appearance_mode("light")  # Modes: "system" (default), "light", "dark"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

        # Define a new pastel color palette for Soft UI/Glassmorphism
        # CustomTkinter uses its own theming, but we can still define colors for custom elements
        self.colors = {
            "primary": "#a2d2ff",  # Light Blue
            "secondary": "#bde0fe", # Lighter Blue
            "accent": "#ffc8dd",   # Pink
            "text": "#4a4e69",     # Dark Blue-Grey
            "light_bg": "#f8f8f8", # Very light grey for frames
            "white": "#ffffff",   # White
            "shadow": "#dcdcdc"   # Light grey for subtle shadows
        }
        
        # With CustomTkinter, we don't configure ttk.Style in the same way for ctk widgets.
        # We will use ctk's built-in theming and widget properties for styling.
        # Remove or comment out the old ttk.Style configurations:
        # self.style = ttk.Style(self)
        # self.style.theme_use('clam')
        # self.style.configure("TFrame", ...)
        # ... (all other self.style.configure and self.style.map lines)

        # Create a main frame using ctk.CTkFrame
        main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=self.colors["light_bg"], border_color=self.colors["shadow"], border_width=1)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Logo and title using ctk.CTkLabel
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent") # Transparent background for header
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ctk.CTkLabel(header_frame, text="MYfacture", 
                                font=ctk.CTkFont(size=28, weight="bold"), 
                                text_color=self.colors["primary"])
        title_label.pack(side='top', pady=10)
        
        subtitle_label = ctk.CTkLabel(header_frame, text="Solution de facturation professionnelle", 
                                  font=ctk.CTkFont(size=14), 
                                  text_color=self.colors["text"])
        subtitle_label.pack(side='top')

        # Notebook with tabs - CustomTkinter does not have a direct CTkNotebook equivalent.
        # We will simulate it using CTkSegmentedButton and CTkFrames.
        self.tab_names = ["Profil Société", "Nouvelle Facture", "Historique"]
        self.tab_frames = {}

        self.segmented_button = ctk.CTkSegmentedButton(main_frame, values=self.tab_names,
                                                        command=self.change_tab,
                                                        font=ctk.CTkFont(size=12, weight="bold"),
                                                        selected_color=self.colors["primary"],
                                                        selected_hover_color=self.colors["secondary"],
                                                        unselected_color=self.colors["light_bg"],
                                                        unselected_hover_color=self.colors["shadow"],
                                                        text_color=self.colors["text"])
        self.segmented_button.pack(fill='x', pady=(10, 20))

        # Container for tab content frames
        self.tab_content_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.tab_content_container.pack(fill='both', expand=True)

        for tab_name in self.tab_names:
            frame = ctk.CTkFrame(self.tab_content_container, corner_radius=10, fg_color=self.colors["white"], border_color=self.colors["shadow"], border_width=1)
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            self.tab_frames[tab_name] = frame

        # Initial tab display
        self.segmented_button.set(self.tab_names[0])
        self.change_tab(self.tab_names[0])

        # Pied de page using ctk.CTkLabel
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(fill='x', pady=(20, 0))
        
        footer_label = ctk.CTkLabel(footer_frame, text="© 2023 MYfacture - Tous droits réservés", 
                                font=ctk.CTkFont(size=9), 
                                text_color=self.colors["text"])
        footer_label.pack(side='right')

        # Call the form creation methods, passing the correct frame
        self.create_profil_form(self.tab_frames["Profil Société"])
        self.create_facture_form(self.tab_frames["Nouvelle Facture"])
        self.create_historique_view(self.tab_frames["Historique"])

    def change_tab(self, selected_tab):
        # Hide all tab frames
        for tab_name in self.tab_names:
            self.tab_frames[tab_name].pack_forget()
        # Show the selected tab frame
        self.tab_frames[selected_tab].pack(fill='both', expand=True)

    # Modify create_profil_form to accept a frame argument
    def create_profil_form(self, parent_frame):
        frame = parent_frame
        
        # Titre de la section
        title_label = ctk.CTkLabel(frame, text="Informations de votre entreprise", 
                               font=ctk.CTkFont(size=16, weight="bold"), 
                               text_color=self.colors["primary"])
        title_label.grid(row=0, column=0, columnspan=3, sticky='w', padx=10, pady=(0, 20))

        labels = ["Nom de la société", "Adresse", "Téléphone", "E-mail", "Numéro SIRET", "Logo"]
        self.entries = {}

        # Créer un cadre pour les champs de formulaire
        form_frame = ctk.CTkFrame(frame, fg_color="transparent") # Transparent background for form frame
        form_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        for i, label_text in enumerate(labels[:-1]):
            label = ctk.CTkLabel(form_frame, text=label_text, font=ctk.CTkFont(size=10))
            label.grid(row=i, column=0, sticky='w', padx=10, pady=10)
            
            entry = ctk.CTkEntry(form_frame, width=300) # Use CTkEntry
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.entries[label_text] = entry

    # You will need to modify create_facture_form and create_historique_view similarly
    # to accept a parent_frame argument and use ctk widgets.
    # I will provide those modifications in the next steps.

    def create_profil_form(self):
        frame = self.profil_frame
        
        # Titre de la section
        title_label = ttk.Label(frame, text="Informations de votre entreprise", 
                               font=("Segoe UI", 16, "bold"), 
                               foreground=self.colors["primary"])
        title_label.grid(row=0, column=0, columnspan=3, sticky='w', padx=10, pady=(0, 20))

        labels = ["Nom de la société", "Adresse", "Téléphone", "E-mail", "Numéro SIRET", "Logo"]
        self.entries = {}

        # Créer un cadre pour les champs de formulaire
        form_frame = ttk.Frame(frame)
        form_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        for i, label_text in enumerate(labels[:-1]):
            label = ttk.Label(form_frame, text=label_text, font=("Segoe UI", 10))
            label.grid(row=i, column=0, sticky='w', padx=10, pady=10)
            
            entry = ttk.Entry(form_frame, width=50)
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.entries[label_text] = entry

        # Logo upload avec un style amélioré
        logo_label = ttk.Label(form_frame, text="Logo", font=("Segoe UI", 10))
        logo_label.grid(row=len(labels)-1, column=0, sticky='w', padx=10, pady=10)
        
        logo_frame = ttk.Frame(form_frame)
        logo_frame.grid(row=len(labels)-1, column=1, sticky='w', padx=10, pady=10)
        
        self.logo_path_var = tk.StringVar()
        logo_entry = ttk.Entry(logo_frame, textvariable=self.logo_path_var, width=40, state='readonly')
        logo_entry.pack(side='left', padx=(0, 10))
        
        logo_button = ttk.Button(logo_frame, text="Parcourir...", command=self.load_logo)
        logo_button.pack(side='left')

        # Cadre pour le bouton de sauvegarde
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky='e', padx=10, pady=20)
        
        save_button = ttk.Button(button_frame, text="Sauvegarder le profil", command=self.save_profile)
        save_button.pack(padx=5)

        # Prévisualisation du logo
        self.logo_preview_label = ttk.Label(frame, text="Aperçu du logo", font=("Segoe UI", 10))
        self.logo_preview_label.grid(row=1, column=1, sticky='n', padx=10, pady=10)
        
        self.logo_preview = ttk.Label(frame)
        self.logo_preview.grid(row=1, column=1, sticky='n', padx=10, pady=40)

        # Charger le profil existant
        self.load_profile()
        
        # Configurer l'expansion des lignes et colonnes
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(1, weight=1)

    def load_logo(self):
        file_path = filedialog.askopenfilename(title="Choisir un logo", filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            self.logo_path_var.set(file_path)
            
            # Prévisualisation du logo
            try:
                from PIL import Image, ImageTk
                
                # Ouvrir et redimensionner l'image
                img = Image.open(file_path)
                img = img.resize((150, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Mettre à jour la prévisualisation
                self.logo_preview.configure(image=photo)
                self.logo_preview.image = photo  # Garder une référence
            except ImportError:
                self.logo_preview.configure(text="Prévisualisation non disponible\n(PIL non installé)")
            except Exception as e:
                self.logo_preview.configure(text=f"Erreur: {e}")

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
        
        # Titre de la section
        title_label = ttk.Label(frame, text="Création d'une nouvelle facture", 
                               font=("Segoe UI", 16, "bold"), 
                               foreground=self.colors["primary"])
        title_label.grid(row=0, column=0, columnspan=6, sticky='w', padx=10, pady=(0, 20))
        
        # Section client
        client_frame = ttk.Frame(frame, padding=10)
        client_frame.grid(row=1, column=0, columnspan=6, sticky='ew', padx=10, pady=5)
        
        client_title = ttk.Label(client_frame, text="Informations client", 
                                font=("Segoe UI", 12, "bold"), 
                                foreground=self.colors["secondary"])
        client_title.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))
        
        # Add client info fields
        client_labels = ["Nom du client", "Adresse client", "Téléphone client", "E-mail client", "N° TVA client"]
        self.client_vars = {}
        
        for i, label_text in enumerate(client_labels):
            ttk.Label(client_frame, text=label_text).grid(row=i+1, column=0, sticky='w', padx=10, pady=5)
            var = tk.StringVar()
            entry = ttk.Entry(client_frame, textvariable=var, width=50)
            entry.grid(row=i+1, column=1, sticky='w', padx=10, pady=5)
            self.client_vars[label_text] = var
        
        # Section produits
        products_frame = ttk.Frame(frame, padding=10)
        products_frame.grid(row=2, column=0, columnspan=6, sticky='nsew', padx=10, pady=10)
        
        products_title = ttk.Label(products_frame, text="Détails des produits/services", 
                                  font=("Segoe UI", 12, "bold"), 
                                  foreground=self.colors["secondary"])
        products_title.grid(row=0, column=0, columnspan=6, sticky='w', pady=(0, 10))
        
        # Tableau des produits
        columns = ("Produit", "Prix Unitaire HT", "Quantité", "TVA (%)", "Remise (%)", "Total HT")
        self.tree = ttk.Treeview(products_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            self.tree.heading(col, text=col)
            width = 100 if col != "Produit" else 200
            self.tree.column(col, width=width)
        
        self.tree.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky='nsew')
        
        # Scrollbar pour le tableau
        scrollbar = ttk.Scrollbar(products_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=6, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Champs pour ajouter un produit
        entry_frame = ttk.Frame(products_frame)
        entry_frame.grid(row=2, column=0, columnspan=6, sticky='ew', padx=5, pady=10)
        
        labels = ["Produit", "Prix Unitaire HT", "Quantité", "TVA (%)", "Remise (%)"]
        self.entry_vars = {}
        
        for i, label_text in enumerate(labels):
            ttk.Label(entry_frame, text=label_text).grid(row=0, column=i, padx=5, pady=5)
            var = tk.StringVar()
            width = 15 if label_text != "Produit" else 30
            entry = ttk.Entry(entry_frame, textvariable=var, width=width)
            entry.grid(row=1, column=i, padx=5, pady=5)
            self.entry_vars[label_text] = var
        
        # Boutons d'action pour les produits
        button_frame = ttk.Frame(products_frame)
        button_frame.grid(row=3, column=0, columnspan=6, sticky='e', padx=5, pady=5)
        
        add_button = ttk.Button(button_frame, text="Ajouter ligne", command=self.add_product_line)
        add_button.pack(side='left', padx=5)
        
        delete_button = ttk.Button(button_frame, text="Supprimer ligne", command=self.delete_product_line)
        delete_button.pack(side='left', padx=5)
        
        # Section totaux
        totals_frame = ttk.Frame(frame, padding=10)
        totals_frame.grid(row=3, column=0, columnspan=6, sticky='ew', padx=10, pady=5)
        
        self.total_ht_var = tk.StringVar(value="0.00")
        self.total_tva_var = tk.StringVar(value="0.00")
        self.total_remise_var = tk.StringVar(value="0.00")
        self.total_ttc_var = tk.StringVar(value="0.00")
        
        # Style pour les labels de totaux
        total_label_style = {"font": ("Segoe UI", 10), "padding": 5}
        total_value_style = {"font": ("Segoe UI", 10, "bold"), "foreground": self.colors["secondary"], "padding": 5}
        
        ttk.Label(totals_frame, text="Total HT :", **total_label_style).grid(row=0, column=4, sticky='e')
        ttk.Label(totals_frame, textvariable=self.total_ht_var, **total_value_style).grid(row=0, column=5, sticky='w')
        
        ttk.Label(totals_frame, text="Total Remise :", **total_label_style).grid(row=1, column=4, sticky='e')
        ttk.Label(totals_frame, textvariable=self.total_remise_var, **total_value_style).grid(row=1, column=5, sticky='w')
        
        ttk.Label(totals_frame, text="Total TVA :", **total_label_style).grid(row=2, column=4, sticky='e')
        ttk.Label(totals_frame, textvariable=self.total_tva_var, **total_value_style).grid(row=2, column=5, sticky='w')
        
        ttk.Label(totals_frame, text="Total TTC :", **total_label_style).grid(row=3, column=4, sticky='e')
        ttk.Label(totals_frame, textvariable=self.total_ttc_var, **total_value_style).grid(row=3, column=5, sticky='w')
        
        # Bouton pour générer le PDF
        action_frame = ttk.Frame(frame)
        action_frame.grid(row=4, column=0, columnspan=6, sticky='e', padx=10, pady=20)
        
        pdf_button = ttk.Button(action_frame, text="Générer PDF", command=self.generate_pdf)
        pdf_button.pack()
        
        # Configurer l'expansion des lignes et colonnes
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)

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
        pdf.cell(0, 8, f"N° TVA: {self.client_vars.get('N° TVA client').get()}", ln=True)

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

    def create_historique_view(self):
        frame = self.historique_frame
        
        # Titre de la section
        title_label = ttk.Label(frame, text="Historique des factures", 
                               font=("Segoe UI", 16, "bold"), 
                               foreground=self.colors["primary"])
        title_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=(0, 20))
        
        # Créer un Treeview pour afficher l'historique des factures
        columns = ("Date", "Numéro", "Client", "Total HT", "Total TTC")
        self.history_tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for i, col in enumerate(columns):
            self.history_tree.heading(col, text=col)
            width = 150 if i < 2 else 120
            self.history_tree.column(col, width=width)
            
        self.history_tree.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        
        # Scrollbar pour l'historique
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.history_tree.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Cadre pour les boutons d'action
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky='e', padx=10, pady=20)
        
        refresh_button = ttk.Button(button_frame, text="Actualiser", 
                                   command=self.load_invoice_history)
        refresh_button.pack(side='left', padx=5)
        
        open_button = ttk.Button(button_frame, text="Ouvrir la facture", 
                                command=self.open_invoice)
        open_button.pack(side='left', padx=5)
        
        # Double-clic pour ouvrir une facture
        self.history_tree.bind("<Double-1>", lambda event: self.open_invoice())
        
        # Configurer l'expansion des lignes et colonnes
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        
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