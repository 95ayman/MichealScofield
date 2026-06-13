# Projet CAO & Eurocode 2 - Dimensionnement d'un Poteau en Béton Armé

## Équipe de Projet
* Ninjbaatar Oyungerel- Responsable GC(GC)
* Loqcman Benyoucef - Responsable architecture Python (INFO)
* Ayman Ghomari - Responsable dessin DXF
* laurent minkoulou - Responsable validation et tests

---

## Description du Projet
Ce programme est un outil intelligent interactif permettant le dimensionnement simplifié d'un poteau en béton armé (section rectangulaire ou circulaire) soumis à la compression, selon les règles de l'Eurocode 2. 

En plus d'automatiser les calculs de ferraillage (choix automatisé des aciers longitudinaux et transversaux), l'outil génère automatiquement un plan d'exécution au format .dxf (vue longitudinale et coupe transversale) directement exploitable sur AutoCAD.

---

## Architecture du Code
Pour rendre le projet lisible et facile à corriger, le code source a été organisé en trois modules distincts :

* main.py : Point d'entrée du programme. Il gère l'interface graphique (Tkinter), la récupération des données de l'utilisateur, l'import/export de fichiers Excel et la communication avec les autres modules.
* calcul_poteau.py : Moteur mathématique du projet. Ce fichier contient toutes les fonctions relatives à l'Eurocode 2 (calcul de l'effort normal ultime, vérification de l'élancement, calcul des sections d'acier nécessaires et adoptées).
* dessin_dxf.py : Moteur graphique. Il transforme les résultats géométriques et le choix des aciers en objets CAO (calques, lignes, cercles, textes) via la bibliothèque externe ezdxf.

---

## Prérequis et Installation
Le programme fonctionne avec Python 3. Avant de le lancer, vous devez installer les deux bibliothèques externes requises pour la manipulation des fichiers Excel et la génération de la CAO.

Ouvrez votre terminal ou l'invite de commande et exécutez :
pip install ezdxf openpyxl

---

## Comment lancer le programme ?
1. Placez les trois fichiers Python (main.py, calcul_poteau.py, dessin_dxf.py) dans le même dossier.
2. Ouvrez un terminal dans ce dossier.
3. Lancez la commande suivante :
python main.py

4. Une interface graphique s'ouvre. Vous avez alors deux options pour utiliser l'outil :
   * Mode Manuel : Remplissez les champs de l'interface avec vos données géométriques, vos charges (NG, NQ) et les propriétés des matériaux, puis cliquez sur "Calculer".
   * Mode par Lot (Excel) : Cliquez sur "Importer Excel", sélectionnez votre fichier de données structuré .xlsx. Le programme traitera tous les poteaux d'un seul coup.

---

## Résultats et Livrables
Une fois le calcul terminé avec succès, le programme génère deux fichiers de sortie dans le même dossier :
* resultats_poteau.xlsx : Un tableau récapitulatif complet des calculs pour chaque section étudiée (incluant les vérifications, la section d'acier requise, les aciers choisis et l'enrobage).
* poteau_BA_rendu.dxf : Le dessin d'exécution (dessiné en millimètres). Vous pouvez l'ouvrir directement dans AutoCAD pour visualiser la géométrie, la répartition des armatures longitudinales et l'espacement des étriers.