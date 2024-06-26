# -*- coding: utf-8 -*-

import arcpy

path = "" #Add path to your geo data

def GetCouche():
    if not arcpy.Exists(path):
        print("La géodatabase spécifiée n'existe pas.")
        return []

    arcpy.env.workspace = path
    layer_list = []

    for layer in arcpy.ListFeatureClasses():
        layer_list.append(layer)

    for data in arcpy.ListDatasets():
        for layer in arcpy.ListFeatureClasses("", "", data):
            layer_list.append(layer)

    return layer_list if layer_list else ["Aucune couche n'a été trouvée dans le dataset."]

def Ajouter_Couche(nom_couche, type_couche):
    if arcpy.Exists(path + "\\" + nom_couche):
        return (0, "La couche existe déjà.")
    else:
        arcpy.CreateFeatureclass_management(path, nom_couche, type_couche)
        return (1, "La couche a été ajoutée avec succès.")

def Modifier_Couche(nom_couche, nouveau_nom, nouveau_type):
    arcpy.env.workspace = path
    arcpy.env.overwriteOutput = True

    if arcpy.Exists(nom_couche):
        couche = arcpy.Describe(nom_couche)
        chemin_couche = couche.catalogPath
        arcpy.Rename_management(chemin_couche, nouveau_nom)
        arcpy.CopyFeatures_management(nouveau_nom, nouveau_type)
        return (1, "La couche a été modifiée avec succès.")
    else:
        return (0, "La couche spécifiée n'existe pas dans la géodatabase.")

def Supprimer_Couche(nom_couche):
    try:
        arcpy.env.workspace = path
        arcpy.Delete_management(nom_couche)
        return (1, "La couche {} a été supprimée avec succès.".format(nom_couche))
    except arcpy.ExecuteError:
        return (0, arcpy.GetMessages())

def Ajouter_champe(nom_couche, nom_champ, type_champ):
    try:
        if arcpy.Exists(path + "\\" + nom_couche):
            arcpy.AddField_management(path + "\\" + nom_couche, nom_champ, type_champ)
            return (1, "Le champ a été ajouté avec succès à la couche.")
        else:
            return (0, "La couche spécifiée n'existe pas.")
    except arcpy.ExecuteError:
        return (0, arcpy.GetMessages())

def Supprimer_Champe(nom_couche, nom_champ):
    try:
        if arcpy.Exists(path + "\\" + nom_couche):
            arcpy.DeleteField_management(path + "\\" + nom_couche, nom_champ)
            return (1, "Le champ a été supprimé avec succès de la couche.")
        else:
            return (0, "La couche spécifiée n'existe pas.")
    except arcpy.ExecuteError:
        return (0, arcpy.GetMessages())

def ajouter_enregistrement_dans_couche(couche, values):
    try:
        chemin_couche = path + "\\" + couche
        couche_temp = arcpy.management.MakeFeatureLayer(chemin_couche, "couche_temp").getOutput(0)
        description = arcpy.Describe(couche_temp)
        champs = [champ for champ in description.fields if champ.name not in ["OBJECTID", "SHAPE", "Shape"]]

        if len(values) != len(champs):
            raise ValueError("Le nombre de valeurs ne correspond pas au nombre de champs.")

        valeurs_converties = []
        for i in range(len(values)):
            valeur = values[i]
            champ = champs[i]
            if champ.type == 'String':
                valeur_convertie = str(valeur)
            elif champ.type == 'Double':
                valeur_convertie = float(valeur)
            elif champ.type == 'Integer':
                valeur_convertie = int(valeur)
            elif champ.type == 'Date':
                valeur_convertie = arcpy.ParseDateTime(valeur)
            else:
                valeur_convertie = valeur
            valeurs_converties.append(valeur_convertie)

        with arcpy.da.InsertCursor(couche_temp, [champ.name for champ in champs if not champ.required]) as curseur:
            curseur.insertRow(valeurs_converties)

        print("Enregistrement ajouté avec succès.")
    except Exception as e:
        print("Erreur lors de l'ajout de l'enregistrement: {}".format(str(e)))
        raise
    finally:
        if arcpy.Exists("couche_temp"):
            arcpy.management.Delete("couche_temp")

def supprimer_enregistrement_dans_arcgis(nom_couche, objectid):
    try:
        chemin_couche = path + "\\" + nom_couche
        couche = arcpy.management.MakeFeatureLayer(chemin_couche, "couche_temp").getOutput(0)

        with arcpy.da.UpdateCursor(couche, "*") as curseur:
            for row in curseur:
                if row[0] == objectid:
                    curseur.deleteRow()
                    return (1, "Enregistrement supprimé avec succès.")
        return (0, "Aucun enregistrement correspondant à l'OBJECTID spécifié n'a été trouvé.")
    except arcpy.ExecuteError:
        return (0, arcpy.GetMessages())

def trouver_maximum(nom_couche, nom_champ):
    chemin_couche = path + "\\" + nom_couche

    try:
        with arcpy.da.SearchCursor(chemin_couche, [nom_champ]) as curseur:
            max_valeur = None
            for row in curseur:
                valeur = row[0]
                if max_valeur is None or valeur > max_valeur:
                    max_valeur = valeur
        return (1, "La valeur maximale du champ {} est : {}".format(nom_champ, max_valeur))
    except Exception as e:
        return (0, "Erreur lors de la recherche de la valeur maximale: {}".format(str(e)))
def trouver_minimum(nom_couche, nom_champ):
    try:
        with arcpy.da.SearchCursor(nom_couche, nom_champ) as cursor:
            min_value = min(row[0] for row in cursor)
        return (True, "La valeur minimale du champ {} est : {}".format(nom_champ, min_value))
    except Exception as e:
        return (False, "Erreur lors de la recherche du minimum : {}".format(str(e)))
def trouver_somme(nom_couche, nom_champ):
    try:
        with arcpy.da.SearchCursor(nom_couche, nom_champ) as cursor:
            sum_value = sum(row[0] for row in cursor)
        return (True, "La somme du champ {} est : {}".format(nom_champ, sum_value))
    except Exception as e:
        return (False, "Erreur lors du calcul de la somme : {}".format(str(e)))
def compter_enregistrements_table(nom_table):
    try:
        count = int(arcpy.GetCount_management(nom_table).getOutput(0))
        return (True, "Nombre total d'enregistrements dans {} : {}".format(nom_table, count))
    except Exception as e:
        return (False, "Erreur lors du comptage des enregistrements : {}".format(str(e)))
def calculer_moyenne_champ(nom_table, nom_champ):
    try:
        moyenne = 0.0
        total = 0.0
        count = 0
        with arcpy.da.SearchCursor(nom_table, [nom_champ]) as cursor:
            for row in cursor:
                total += float(row[0])
                count += 1
        if count > 0:
            moyenne = total / count
        return (True, "La moyenne du champ {} dans la table {} est : {:.2f}".format(nom_champ, nom_table, moyenne))
    except Exception as e:
        return (False, "Erreur lors du calcul de la moyenne : {}".format(str(e)))
def creer_buffer_couche_point(nom_couche_entree, distance, nom_couche_sortie):
    try:
        arcpy.Buffer_analysis(nom_couche_entree, nom_couche_sortie, distance)
        return (True, "Buffer créé avec succès pour la couche {} avec une distance de {}".format(nom_couche_entree, distance))
    except Exception as e:
        return (False, "Erreur lors de la création du buffer : {}".format(str(e)))
def creer_intersection_buffers(couches_entree, nom_couche_sortie):
    try:
        arcpy.Intersect_analysis(couches_entree, nom_couche_sortie)
        return (True, "Intersection des buffers créée avec succès dans la couche {}".format(nom_couche_sortie))
    except Exception as e:
        return (False, "Erreur lors de la création de l'intersection des buffers : {}".format(str(e)))
def convertir_polygones_vers_lignes(couche_polygones, nom_couche_lignes):
    try:
        arcpy.FeatureToLine_management(couche_polygones, nom_couche_lignes)
        return (True, "Couche de lignes créée avec succès : {}".format(nom_couche_lignes))
    except Exception as e:
        return (False, "Erreur lors de la conversion en lignes : {}".format(str(e)))