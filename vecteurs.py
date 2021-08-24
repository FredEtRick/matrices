# TODO : créer classe Vecteur
# TODO : modifier autres fichiers pour utiliser vecteurs à la place de représentation temporaire
# TODO : rajouter de nouvelles manipulations des vecteurs dans les autres fichiers

# class vecteur

import random
import copy
import math
import logging

logging.basicConfig(level=logging.WARNING)

from matrices import *

class Vecteur() :

    # création vecteur : init, saisie, hasard
    # représentation textuelle : repr, normaliserLargeur
    # propriétés vecteur : estUnitaire
    # vecteurs particuliers : nul, unitaire
    # opérations sur le vecteur : scalaire, castMatrice
    # opérations entre vecteurs : dot, cross

    # =========== CREATION DU VECTEUR (constructeur et méthodes qu'il appel) ===========

    """constructeur
    Args : 
        saisie (bool) : True si l'utilisateur doit saisir manuellement chaque composante du vecteur
        hasard (bool) : True si chaque composante du vecteur doit être tirée au sort
        nul (bool) : True si l'utilisateur souhaite créer un vecteur nul
        composantes (tuple[float]) : composantes du vecteur,
        dim (int) : nombre de dimensions de l'espace auquel appartient le vecteur (nombre de composantes)
    """
    def __init__(self, saisie=False, hasard=False, nul=False, composantes=[], dim=0, minVals=-25, maxVals=25) :
        if saisie :
            dim, composantes = self.saisie()
        elif hasard :
            dim, composantes = self.hasard(dim, minVals, maxVals)
        elif nul :
            dim, composantes = self.nul(dim)
        self.dim = dim
        self.composantes = composantes
    
    """ saisie manuelle du vecteur pour le constructeur, composante par composante
    Return :
        int : nombre de dimensions de l'espace contenant le vecteur
        tuple[float] : composantes du vecteur
    """
    def saisie(self) :
        print()
        print("Saisie du vecteur :")
        dim = int(input("Nombre de dimensions : "))
        composantes = []
        for i in range(dim) :
            composante = int(input(f"composante {i} : "))
            composantes.append(composante)
        composantes = tuple(composantes)
        return dim, composantes

    """ remplissage du vecteur au hasard, pour le constructeur, avec limites éventuellement indiquées manuellement
    Args :
        dim (int) : nombre de dimensions de l'espace auquel le vecteur appartient
    Return :
        dim (int)
        tuple[float] : composantes du vecteur
    """
    def hasard(self, dim, minVals, maxVals) :
        composantes = []
        for i in range(dim) :
            composante = random.randint(minVals, maxVals)
            composantes.append(composante)
        composantes = tuple(composantes)
        return dim, composantes
    
    # =========== REPRESENTATION TEXTUELLE ===========
    
    """ cré une représentation de la matrice sous forme de string, et la renvoie
    Args :
        espace (int) : espace prit par une composante dans le vecteur, en terme de nombres de caractères, pour éviter décalages d'un vecteur sur l'autre, dans le cas où on en affiche plusieurs à la fois
    Return :
        str : représentation textuelle de la matrice
    """
    def __repr__(self, espace=6) :
        if self.dim > 0 :
            repr = "( "
            for i in range(len(self.composantes)) :
                composante = self.composantes[i]
                compTexte = self.normaliserLargeur(composante, espace, 3)
                repr += compTexte
                if i < len(self.composantes) - 1 :
                    repr += ", "
                else :
                    repr += " "
            repr += ")"
            return repr
        else :
            return "O"
    
    """ créé une représentation normalisée d'un nombre. En vue de l'affichage du vecteur, pour éviter d'avoir des vecteurs décallés en fonction des valeurs présentes. Permet d'indiquer une précision pour le float, et la largeur souhaitée d'une colonne.
    Args :
        n (float) : composante à afficher
        largeur (int) : largeur d'affichage prévu pour une composante
        precision (int) : précision de la valeur, pour l'affichage
    Return :
        str : texte à afficher pour représenter la composante du vecteur
    """
    def normaliserLargeur(self, n, largeur, precision) :
        chaine = str(round(n, precision))
        while len(chaine) < largeur :
            chaine += " "
        return chaine
    
    # =========== PROPRIETES VECTEUR ===========

    # =========== VALEURS PARTICULIERES ===========

    """ retourne un vecteur nul, de même dimension que le vecteur self
    Return :
        Vecteur : vecteur nul, de même dimension que le vecteur self
    """
    def nul(self, dim) :
        composantes = []
        for i in range(dim) :
            composantes.append(0)
        composantes = tuple(composantes)
        return dim, composantes

    # =========== OPERATIONS SUR LE VECTEUR ===========

    """ transforme le vecteur en matrice, en vue par exemple de faciliter une opération entre vecteurs et matrices (produit etc)
    Args :
        verticale (bool) : True si le vecteur doit être transformé en matrice verticale, False pour une matrice horizontale
    Return :
        Matrice : matrice d'une seule ligne ou colonne (en fonction de l'argument "verticale") avec les composantes de self
    """
    def castMatrice(self, verticale=False) :
        matrice = None
        if verticale :
            m = []
            for composante in self.composantes :
                ligne = []
                ligne.append(composante)
                m.append(ligne)
            matrice = Matrice(matrice=m, nbl=self.dim, nbc=1)
        else :
            m = []
            ligne = []
            for composante in self.composantes :
                ligne.append(composante)
            m.append(ligne)
            matrice = Matrice(matrice=m, nbl=1, nbc=self.dim)
        return matrice