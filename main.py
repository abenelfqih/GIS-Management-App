# -*- coding: utf-8 -*-


from tkinter import ttk
import Tkinter as tk
import tkMessageBox
import arcpy
import arcApp as app

def quitter():
    root.quit()


# Création de la fenêtre principale
root = tk.Tk()
root.title("Interface de gestion")

liste_frame = tk.Frame(root)
liste_frame.pack(side=tk.LEFT, padx=10, pady=10)

global liste
liste = tk.Listbox(liste_frame)
for couche in app.GetCouche():
    liste.insert('end', couche)
liste.pack()


def Erreur(liste):
    if liste.curselection():
        pass
    else:
        tkMessageBox.showerror("Erreur", "Aucune couche selectionnee")


def Afficher_liste():
    liste.delete(0, tk.END)
    for couche in app.GetCouche():
        liste.insert('end', couche)
    liste.pack()


# Bouton Actualiser
bouton_actualiser = tk.Button(liste_frame, text="Actualiser", command=Afficher_liste)
bouton_actualiser.pack()


def afficher_couche():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    # Obtenir les noms des attributs de la couche
    attributs = [field.name for field in arcpy.ListFields(couche_selectionnee)]
    # Obtenir les valeurs des attributs pour chaque enregistrement
    valeurs_attributs = []
    with arcpy.da.SearchCursor(couche_selectionnee, '*') as curseur:
        for row in curseur:
            valeurs_attributs.append(row)

    # Créer la fenêtre Tkinter
    fenetre = tk.Tk()
    fenetre.title("La Couche " + str(couche_selectionnee).upper())

    # Créer le tableau
    tableau = ttk.Treeview(fenetre, columns=attributs, show="headings")

    # Ajouter les colonnes au tableau
    for attribut in attributs:
        tableau.heading(attribut, text=attribut)
        tableau.column(attribut, width=100)

    # Ajouter les enregistrements au tableau
    for valeur_attribut in valeurs_attributs:
        tableau.insert("", tk.END, values=valeur_attribut)

    # Afficher le tableau
    tableau.pack()

    # Exécuter la boucle principale Tkinter
    fenetre.mainloop()


def ajouter_couche():
    def valider():
        nom_couche = champ_saisie.get()
        type_couche = liste_types.get()

        if nom_couche and type_couche:
            app.Ajouter_Couche(nom_couche, type_couche)
            tkMessageBox.showinfo("Information",
                                  "Nom de la couche : {}\nType de la couche : {}".format(nom_couche, type_couche))
            Afficher_liste()
            fenetre_saisie.destroy()
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Ajouter une couche")

    # Zone de saisie pour le nom de la couche
    label_nom = tk.Label(fenetre_saisie, text="Nom de la couche:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Liste déroulante pour le type de la couche
    label_type = tk.Label(fenetre_saisie, text="Type de la couche:")
    label_type.pack()
    types_couche = ["POINT", "MULTIPOINT", "POLYGON", "POLYLINE", "MULTIPATCH"]  # Exemple de types de couche
    liste_types = ttk.Combobox(fenetre_saisie, values=types_couche, state="readonly")
    liste_types.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()


def modifier_couche():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    def valider():
        nom_couche = champ_saisie.get()
        type_couche = liste_types.get()

        if nom_couche and type_couche:
            pass
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

        resultat = app.Modifier_Couche(couche_selectionnee, nom_couche, type_couche)
        if resultat[0]:
            tkMessageBox.showinfo("Information", resultat[1])
            Afficher_liste()
            fenetre_saisie.destroy()
        else:
            tkMessageBox.showerror("Erreur", resultat[1])

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Modifier une couche")

    # Zone de saisie pour le nom de la couche
    label_nom = tk.Label(fenetre_saisie, text="Nom de la couche:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.insert(0, couche_selectionnee)
    champ_saisie.pack()

    # Liste déroulante pour le type de la couche
    label_type = tk.Label(fenetre_saisie, text="Type de la couche:")
    label_type.pack()
    types_couche = ["POINT", "MULTIPOINT", "POLYGON", "POLYLINE", "MULTIPATCH"]  # Exemple de types de couche
    liste_types = ttk.Combobox(fenetre_saisie, values=types_couche, state="readonly")
    liste_types.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()


def supprimer_couche():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    resultat = app.Supprimer_Couche(couche_selectionnee)

    if resultat[0]:
        tkMessageBox.showinfo("Information", resultat[1])
        Afficher_liste()
    else:
        tkMessageBox.showerror("Erreur", resultat[1])


def ajouter_champe():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    def valider():
        nom_champe = champ_saisie.get()
        type_champe = liste_types.get()

        if nom_champe and type_champe:
            resultat = app.Ajouter_champe(couche_selectionnee,nom_champe,type_champe)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                Afficher_liste()
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Ajouter un champ")

    # Zone de saisie pour le nom du champ
    label_nom = tk.Label(fenetre_saisie, text="Nom du champ:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Liste déroulante pour le type du champ
    label_type = tk.Label(fenetre_saisie, text="Type du champ:")
    label_type.pack()
    types_champs = ["TEXT", "FLOAT", "DOUBLE", "SHORT", "LONG", "DATE"]  # Exemple de types de champ
    liste_types = ttk.Combobox(fenetre_saisie, values=types_champs, state="readonly")
    liste_types.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()




def ajouter_enregistrement_couche_arcgis():
    Erreur(liste)
    selected_index = liste.curselection()
    couche = liste.get(selected_index)

    description = arcpy.Describe(couche)
    champs = [champ for champ in description.fields if not champ.required]

    # Créer une fenêtre Tkinter
    fenetre = tk.Tk()
    fenetre.title("Ajouter un nouvel enregistrement")

    # Créer les champs de saisie pour chaque champ de la couche
    entrees = []
    for champ in champs:
        tk.Label(fenetre, text=champ.name).pack()
        entree = tk.Entry(fenetre)
        entree.pack()
        entrees.append(entree)

    # Fonction pour ajouter l'enregistrement à la couche
    def ajouter():
        valeurs = [entree.get() for entree in entrees]
        try:
            app.ajouter_enregistrement_dans_couche(couche, valeurs)
            tkMessageBox.showinfo("Information", "Enregistrement ajouté avec succès")
            fenetre.destroy()
        except Exception as e:
            tkMessageBox.showerror("Erreur", "Erreur lors de l'ajout de l'enregistrement: {}".format(str(e)))
            fenetre.destroy()

    # Ajouter un bouton pour ajouter l'enregistrement
    bouton = tk.Button(fenetre, text="Ajouter", command=ajouter)
    bouton.pack()

    fenetre.mainloop()


def trouver_maximum_couche():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    def valider():
        nom_champ = champ_saisie.get()

        if nom_champ:
            resultat = app.trouver_maximum(couche_selectionnee, nom_champ)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez entrer le nom du champ.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Trouver le maximum")

    # Zone de saisie pour le nom du champ
    label_nom = tk.Label(fenetre_saisie, text="Nom du champ:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()

def ajouter_champe():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    def valider():
        nom_champe = champ_saisie.get()
        type_champe = liste_types.get()

        if nom_champe and type_champe:
            resultat = app.Ajouter_champe(couche_selectionnee, nom_champe, type_champe)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                Afficher_liste()
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Ajouter un champ")

    # Zone de saisie pour le nom du champ
    label_nom = tk.Label(fenetre_saisie, text="Nom du champ:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Liste déroulante pour le type du champ
    label_type = tk.Label(fenetre_saisie, text="Type du champ:")
    label_type.pack()
    types_champs = ["TEXT", "FLOAT", "DOUBLE", "SHORT", "LONG", "DATE"]
    liste_types = ttk.Combobox(fenetre_saisie, values=types_champs, state="readonly")
    liste_types.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()
def supprimer_champe():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    def valider():
        nom_champe = champ_saisie.get()

        if nom_champe:
            resultat = app.Supprimer_Champe(couche_selectionnee, nom_champe)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                Afficher_liste()
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir le champ.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Supprimer un champ")

    # Zone de saisie pour le nom du champ
    label_nom = tk.Label(fenetre_saisie, text="Nom du champ:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()
def trouver_minimum_couche():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    def valider():
        nom_champ = champ_saisie.get()

        if nom_champ:
            resultat = app.trouver_minimum(couche_selectionnee, nom_champ)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez entrer le nom du champ.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Trouver le minimum")

    # Zone de saisie pour le nom du champ
    label_nom = tk.Label(fenetre_saisie, text="Nom du champ:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()
def trouver_somme_couche():
    Erreur(liste)
    selected_index = liste.curselection()
    couche_selectionnee = liste.get(selected_index)

    def valider():
        nom_champ = champ_saisie.get()

        if nom_champ:
            resultat = app.trouver_somme(couche_selectionnee, nom_champ)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez entrer le nom du champ.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Trouver la somme")

    # Zone de saisie pour le nom du champ
    label_nom = tk.Label(fenetre_saisie, text="Nom du champ:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()
def compter_enregistrements_table():
    def valider():
        nom_table = champ_saisie.get()

        if nom_table:
            resultat = app.compter_enregistrements_table(nom_table)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez entrer le nom de la table.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x100")
    fenetre_saisie.title("Afficher le nombre d'enregistrements")

    # Zone de saisie pour le nom de la table
    label_nom = tk.Label(fenetre_saisie, text="Nom de la table:")
    label_nom.pack()
    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()
def calculer_moyenne_champ():
    def valider():
        nom_table = champ_table.get()
        nom_champ = champ_champ.get()

        if nom_table and nom_champ:
            resultat = app.calculer_moyenne_champ(nom_table, nom_champ)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("300x150")
    fenetre_saisie.title("Calculer et afficher la moyenne d'un champ")

    # Zone de saisie pour le nom de la table
    label_table = tk.Label(fenetre_saisie, text="Nom de la table:")
    label_table.pack()
    champ_table = tk.Entry(fenetre_saisie)
    champ_table.pack()

    # Zone de saisie pour le nom du champ
    label_champ = tk.Label(fenetre_saisie, text="Nom du champ:")
    label_champ.pack()
    champ_champ = tk.Entry(fenetre_saisie)
    champ_champ.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()
def creer_buffer_couche_point():
    def valider():
        nom_couche_entree = champ_couche_entree.get()
        distance = champ_distance.get()
        nom_couche_sortie = champ_couche_sortie.get()

        if nom_couche_entree and distance and nom_couche_sortie:
            resultat = app.creer_buffer_couche_point(nom_couche_entree, distance, nom_couche_sortie)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("400x200")
    fenetre_saisie.title("Créer le buffer d'une couche d'objet point")

    # Zone de saisie pour le nom de la couche d'entrée
    label_couche_entree = tk.Label(fenetre_saisie, text="Nom de la couche d'entrée:")
    label_couche_entree.pack()
    champ_couche_entree = tk.Entry(fenetre_saisie)
    champ_couche_entree.pack()

    # Zone de saisie pour la distance du buffer
    label_distance = tk.Label(fenetre_saisie, text="Distance du buffer:")
    label_distance.pack()
    champ_distance = tk.Entry(fenetre_saisie)
    champ_distance.pack()

    # Zone de saisie pour le nom de la couche de sortie
    label_couche_sortie = tk.Label(fenetre_saisie, text="Nom de la couche de sortie:")
    label_couche_sortie.pack()
    champ_couche_sortie = tk.Entry(fenetre_saisie)
    champ_couche_sortie.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()
def creer_intersection_buffers():
    def valider():
        couches_entree = champ_couches_entree.get().split(",")
        nom_couche_sortie = champ_couche_sortie.get()

        if couches_entree and nom_couche_sortie:
            resultat = app.creer_intersection_buffers(couches_entree, nom_couche_sortie)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("400x200")
    fenetre_saisie.title("Créer l'intersection des buffers")

    # Zone de saisie pour les couches d'entrée (séparées par des virgules)
    label_couches_entree = tk.Label(fenetre_saisie, text="Couches d'entrée (séparées par des virgules):")
    label_couches_entree.pack()
    champ_couches_entree = tk.Entry(fenetre_saisie)
    champ_couches_entree.pack()

    # Zone de saisie pour le nom de la couche de sortie
    label_couche_sortie = tk.Label(fenetre_saisie, text="Nom de la couche de sortie:")
    label_couche_sortie.pack()
    champ_couche_sortie = tk.Entry(fenetre_saisie)
    champ_couche_sortie.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()
def convertir_polygones_vers_lignes():
    def valider():
        couche_polygones = champ_couche_polygones.get()
        nom_couche_lignes = champ_couche_lignes.get()

        if couche_polygones and nom_couche_lignes:
            resultat = app.convertir_polygones_vers_lignes(couche_polygones, nom_couche_lignes)
            if resultat[0]:
                tkMessageBox.showinfo("Information", resultat[1])
                fenetre_saisie.destroy()
            else:
                tkMessageBox.showerror("Erreur", resultat[1])
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("400x200")
    fenetre_saisie.title("Convertir polygones vers lignes")

    # Zone de saisie pour la couche de polygones
    label_couche_polygones = tk.Label(fenetre_saisie, text="Couche de polygones:")
    label_couche_polygones.pack()
    champ_couche_polygones = tk.Entry(fenetre_saisie)
    champ_couche_polygones.pack()

    # Zone de saisie pour le nom de la couche de lignes
    label_couche_lignes = tk.Label(fenetre_saisie, text="Nom de la couche de lignes:")
    label_couche_lignes.pack()
    champ_couche_lignes = tk.Entry(fenetre_saisie)
    champ_couche_lignes.pack()

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()
# Cadre pour les boutons de gestion
gestion_frame = tk.Frame(root)
gestion_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Ajouter les boutons de gestion des couches
ajouter_button = tk.Button(gestion_frame, text="Ajouter Couche", command=ajouter_couche)
ajouter_button.grid(row=0, column=0, padx=5, pady=5)

modifier_button = tk.Button(gestion_frame, text="Modifier Couche", command=modifier_couche)
modifier_button.grid(row=0, column=1, padx=5, pady=5)

supprimer_button = tk.Button(gestion_frame, text="Supprimer Couche", command=supprimer_couche)
supprimer_button.grid(row=0, column=2, padx=5, pady=5)

# Ajouter les boutons de gestion des champs
ajouter_champ_button = tk.Button(gestion_frame, text="Ajouter Champ", command=ajouter_champe)
ajouter_champ_button.grid(row=1, column=0, padx=5, pady=5)

supprimer_champ_button = tk.Button(gestion_frame, text="Supprimer Champ", command=supprimer_champe)
supprimer_champ_button.grid(row=1, column=1, padx=5, pady=5)

# Ajouter les boutons pour les opérations sur les enregistrements et les statistiques
ajouter_enregistrement_button = tk.Button(gestion_frame, text="Ajouter Enregistrement", command=ajouter_enregistrement_couche_arcgis)
ajouter_enregistrement_button.grid(row=2, column=0, padx=5, pady=5)

afficher_nombre_enregistrements_button = tk.Button(gestion_frame, text="Afficher Nombre Enregistrements", command=compter_enregistrements_table)
afficher_nombre_enregistrements_button.grid(row=2, column=1, padx=5, pady=5)

trouver_max_button = tk.Button(gestion_frame, text="Trouver Maximum", command=trouver_maximum_couche)
trouver_max_button.grid(row=2, column=2, padx=5, pady=5)

trouver_min_button = tk.Button(gestion_frame, text="Trouver Minimum", command=trouver_minimum_couche)
trouver_min_button.grid(row=2, column=3, padx=5, pady=5)

trouver_somme_button = tk.Button(gestion_frame, text="Trouver Somme", command=trouver_somme_couche)
trouver_somme_button.grid(row=3, column=0, padx=5, pady=5)

calculer_moyenne_button = tk.Button(gestion_frame, text="Calculer Moyenne Champ", command=calculer_moyenne_champ)
calculer_moyenne_button.grid(row=3, column=1, padx=5, pady=5)

# Bouton pour les opérations spatiales
creer_buffer_button = tk.Button(gestion_frame, text="Créer Buffer Couche Point", command=creer_buffer_couche_point)
creer_buffer_button.grid(row=4, column=0, padx=5, pady=5)

creer_intersection_button = tk.Button(gestion_frame, text="Créer Intersection Buffers", command=creer_intersection_buffers)
creer_intersection_button.grid(row=4, column=1, padx=5, pady=5)

convertir_lignes_button = tk.Button(gestion_frame, text="Convertir Polygones vers Lignes", command=convertir_polygones_vers_lignes)
convertir_lignes_button.grid(row=4, column=2, padx=5, pady=5)

# Bouton Quitter
bouton_quitter = tk.Button(gestion_frame, text="Quitter", command=quitter)
bouton_quitter.grid(row=5, column=0, columnspan=2, pady=10)

# Ajouter le bouton pour afficher les enregistrements de la couche sélectionnée
afficher_button = tk.Button(liste_frame, text="Afficher", command=afficher_couche)
afficher_button.pack(pady=5)

# Lancer la boucle principale
root.mainloop()
