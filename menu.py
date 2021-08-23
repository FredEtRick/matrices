# fichier à exécuter directement
# contient tout ce qui est relatif au menu
# utilisateur fait ses choix, et indique ses demandes

from pprint import pprint
import math
import os
import logging

cheminCourant = os.path.dirname(__file__)
cheminLog = os.path.join(cheminCourant, "logs.txt")
logging.basicConfig(level=logging.WARNING, format="[%(asctime)s - %(levelname)s] %(message)s", filename=cheminLog, filemode="a")

from matrices import *
from vecteurs import *

# =========== VARIABLES ===========

menu = [
    "renseigner une matrice",
    "générer une matrice aléatoirement",
    "voir toutes les matrices en mémoire",
    "effacer les matrices en mémoire",
    "transposer une matrice",
    "calculer la forme échelonnée réduite d'une matrice",
    "connaitre les solutions d'une matrice augmentée",
    "calculer l'inverse d'une matrice",
    "calculer le noyau d'une matrice",
    "effacer une matrice en mémoire",
    "faire la somme de deux matrices",
    "faire le produit de deux matrices"
]

# limites indices questions du menu
# indice 0 à deb[0]-1 = questions toujours posées (min 0 matrices en mémoire)
# deb[0] => deb[1]-1 = questions posées lorsqu'il y a au moins une matrice en mémoire (min 1)
# deb[1] => ... = questions posées lorsqu'il y a au moins 2 matrices en mémoire (min 2)
# dernière case deb = len(menu) : si il y a le max possible de matrices, présenter tout le menu
debuts = [2, 9, len(menu)]
caseMax = len(debuts)-1

nbMatrices = 0 # nombre de matrices 'mémorisées'
listeMatrices = [] # matrices 'mémorisées' le temps de l'exécution

# =========== FONCTIONS DIVERSES ===========

""" présente menu à l'utilisateur, et récolte son choix
Return :
    int : indice (dans 'menu') du choix fait par l'utilisateur
"""
def choixMenu() :
    iPremiereExclue = debuts[min(nbMatrices, caseMax)]
    print("Que désirez vous faire ?")
    for i in range(len(menu[:iPremiereExclue])) :
        print(f"{i+1} : {menu[i]}")
    choix = "non"
    while not choix.isdigit() or int(choix) < 1 or int(choix) > iPremiereExclue :
        choix = input("Tapez le numéro de votre choix, et appuyez sur 'Entrée' : ")
    choix = int(choix)-1
    return choix

""" propose à l'utilisateur de visualiser les matrices, puis demande de choisir une matrice, et renvoie son numéro
Return :
    int : indice (dans 'listeMatrices') de la matrice choisie par l'utilisateur
"""
def choixMatrice() :
    afficher = False
    while afficher != "oui" and afficher != "non" :
        afficher = input("Avez vous besoin de voir les matrices pour connaitre leurs numéros ? (tappez 'oui' ou 'non') : ")
    afficher = True if afficher == "oui" else False
    if afficher :
        appliquerChoix(2)
    num = "non"
    while not num.isdigit() or int(num) < 1 or int(num) > nbMatrices :
        num = input("Tapez le numéro de la matrice choisie, et appuyez sur 'Entrée' : ")
    num = int(num)-1
    return num

""" demande un int plus grand que borneInf à l'utilisateur, en lui affichant le texte passé en paramètres. Reboucle tant que les données ne sont pas valides, puis renvoie l'int
Args :
    texte (str) : demande formulée à l'utilisateur
    borneInf (int) : borne inférieur (incluse)
Return :
    int : nombre entré par l'utilisateur
"""
def intBorneInfWhile(texte, borneInf) :
    n = "non"
    while not n.lstrip("-").isdigit() or int(n) < borneInf :
        n = input(texte)
    n = int(n)
    return n

# =========== APPLICATION DES CHOIX ===========

""" fait ce que l'utilisateur a demandé, en appelant les méthodes nécessaires
Args :
    choix (int) : choix fait par l'utilisateur
"""
def appliquerChoix(choix) :
    global listeMatrices
    global nbMatrices
    if choix == 0 : # renseigner une matrice
        m = Matrice(saisie=True)
        listeMatrices.append(m)
        nbMatrices += 1
        print(m)
    if choix == 1 : # générer une matrice aléatoirement
        preciser = ""
        m = None
        while preciser != "oui" and preciser != "non" :
            preciser = input("Voulez vous préciser les limites du nombre de colonnes, lignes, et des valeurs de la matrice ? (tappez 'oui' ou 'non') : ")
        preciser = True if preciser == "oui" else False
        if preciser :
            minNbl = intBorneInfWhile("Nombre minimal de lignes : ", 1)
            maxNbl = intBorneInfWhile("Nombre maximal de lignes : ", minNbl)
            minNbc = intBorneInfWhile("Nombre minimal de colonnes : ", 1)
            maxNbc = intBorneInfWhile("Nombre maximal de colonnes : ", minNbc)
            minVals = intBorneInfWhile("Valeur minimale autorisée : ", -math.inf)
            maxVals = intBorneInfWhile("Valeur maximale autorisée : ", minVals)
            m = Matrice(hasard=True, minNbl=minNbl, maxNbl=maxNbl, minNbc=minNbc, maxNbc=maxNbc, minVals=minVals, maxVals=maxVals)
            listeMatrices.append(m)
        else :
            m = Matrice(hasard=True)
            listeMatrices.append(m)
        print(m)
        nbMatrices += 1
    if choix == 2 : # voir toutes les matrices en mémoire
        for i in range(len(listeMatrices)) :
            print(f"=== MATRICE {i+1} ===")
            print(listeMatrices[i])
    if choix == 3 : # effacer les matrices en mémoire
        sur = False
        while sur != "oui" and sur != "non" :
            sur = input("Etes vous sur de vouloir effacer toutes les matrices ? (tappez 'oui' ou 'non') : ")
        sur = True if sur == "oui" else False
        if sur :
            listeMatrices = []
            nbMatrices = 0
            print("matrices effacées.")
        else :
            print("annulé, matrices non effacées.")
    if choix == 4 : # transposer une matrice
        num = choixMatrice()
        transp = listeMatrices[num].transposeReturn()
        print(transp)
        listeMatrices.append(transp)
        nbMatrices += 1
        print("Le transposé de la matrice a été sauvé.")
    if choix == 5 : # calculer la forme échelonnée réduite d'une matrice
        num = choixMatrice()
        mrref = listeMatrices[num].rref()
        print(mrref)
        listeMatrices.append(mrref)
        nbMatrices += 1
    if choix == 6 : # connaitre les solutions d'une matrice augmentée
        num = choixMatrice()
        solutions = listeMatrices[num].sol()
        print(solutions)
    if choix == 7 : # calculer l'inverse d'une matrice
        num = choixMatrice()
        inv = listeMatrices[num].inverse()
        print(inv)
        listeMatrices.append(inv)
        nbMatrices += 1
    if choix == 8 : # calculer le noyau d'une matrice
        num = choixMatrice()
        noyau = listeMatrices[num].noyau()
        pprint(noyau) # TODO : améliorer une fois que j'aurais créé la classe vecteur
    if choix == 9 : # effacer une matrice en mémoire
        num = choixMatrice()
        supprimee = listeMatrices.pop(num)
        nbMatrices -= 1
        print("la matrice suivante a été supprimée :")
        print(supprimee)
    if choix == 10 : # faire la somme de deux matrices
        print("=== PREMIERE MATRICE ===")
        num1 = choixMatrice()
        print("=== SECONDE MATRICE ===")
        num2 = choixMatrice()
        resultat = listeMatrices[num1].somme(listeMatrices[num2])
        print("=== RESULTAT ===")
        print(resultat)
        listeMatrices.append(resultat)
        nbMatrices += 1
    if choix == 11 : # faire le produit de deux matrices
        print("=== PREMIERE MATRICE ===")
        num1 = choixMatrice()
        print("=== SECONDE MATRICE ===")
        num2 = choixMatrice()
        resultat = listeMatrices[num1].produit(listeMatrices[num2])
        print("=== RESULTAT ===")
        print(resultat)
        listeMatrices.append(resultat)
        nbMatrices += 1

# =========== GESTION, APPEL DES FONCTIONS, BOUCLE ===========

# début du programme
# demande appelle fonctions précédemment définies
# boucle tant que l'utilisateur souhaite continuer
continuer = True
while continuer :
    choix = choixMenu()
    appliquerChoix(choix)
    while continuer != "oui" and continuer != "non" :
        continuer = input("Voulez continuer ? (tappez 'oui' ou 'non') : ")
    continuer = True if continuer == "oui" else False
