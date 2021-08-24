# TODO : créer classe Vecteur
# TODO : modifier autres fichiers pour utiliser vecteurs à la place de représentation temporaire
# TODO : rajouter de nouvelles manipulations des vecteurs dans les autres fichiers

# class vecteur

import random
import copy
import math
import logging
import fractions

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
        minVals (int) : valeur minimale de chaque composant du vecteur
        maxVals (int) : valeur minimale de chaque composant du vecteur
        maxDen (int) : valeur minimale du dénominateur de chaque composant du vecteur
    """
    def __init__(self, saisie=False, hasard=False, nul=False, composantes=[], dim=0, minVals=-25, maxVals=25, maxDen=4) :
        if saisie :
            dim, composantes = self.saisie()
        elif hasard :
            dim, composantes = self.hasard(dim, minVals, maxVals, maxDen)
        elif nul :
            dim, composantes = self.nul(dim)
        self.dim = dim
        self.composantes = composantes
    
    """ saisie manuelle du vecteur pour le constructeur, composante par composante
    Return :
        int : nombre de dimensions de l'espace contenant le vecteur
        tuple[Fraction] : composantes du vecteur
    """
    def saisie(self) :
        print()
        print("Saisie du vecteur :")
        dim = int(input("Nombre de dimensions : "))
        composantes = []
        for i in range(dim) :
            num = int(input(f"composante {i}, numérateur : "))
            den = int(input(f"composante {i}, dénominateur : "))
            frac = fractions.Fraction(numerator=num, denominator=den)
            composantes.append(frac)
        composantes = tuple(composantes)
        return dim, composantes

    """ remplissage du vecteur au hasard, pour le constructeur, avec limites éventuellement indiquées manuellement
    Args :
        dim (int) : nombre de dimensions de l'espace auquel le vecteur appartient
        minVals (int) : valeur minimale de chaque composant du vecteur
        maxVals (int) : valeur minimale de chaque composant du vecteur
        maxDen (int) : valeur minimale du dénominateur de chaque composant du vecteur
    Return :
        dim (int)
        tuple[Fraction] : composantes du vecteur
    """
    def hasard(self, dim, minVals, maxVals, maxDen) :
        composantes = []
        for i in range(dim) :
            den = random.randint(1, maxDen)
            num = random.randint(minVals*den, maxVals*den)
            frac = fractions.Fraction(numerator=num, denominator=den)
            composantes.append(frac)
        composantes = tuple(composantes)
        return dim, composantes
    
    # =========== REPRESENTATION TEXTUELLE ===========
    
    """ cré une représentation de la matrice sous forme de string, et la renvoie
    Args :
        espace (int) : espace prit par une composante dans le vecteur, en terme de nombres de caractères, pour éviter décalages d'un vecteur sur l'autre, dans le cas où on en affiche plusieurs à la fois
    Return :
        str : représentation textuelle de la matrice
    """
    def __repr__(self, espace=10) :
        if self.dim > 0 :
            repr = "( "
            for i in range(len(self.composantes)) :
                composante = self.composantes[i]
                compTexte = self.normaliserLargeur(composante, espace)
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
    Return :
        str : texte à afficher pour représenter la composante du vecteur
    """
    def normaliserLargeur(self, n, largeur=10) :
        chaine = str(fractions.Fraction(n))
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