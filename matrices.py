# classe Matrice

import random
import copy
import math
import logging

logging.basicConfig(level=logging.WARNING)

class Matrice() :

    # création matrice : init, saisie, hasard
    # représentation textuelle : repr normaliserLargeur
    # propriétés matrice : nullity indicesLibresPivots
    # matrices particulières : identite transposeReturn transposeInplace rref inverse
    # solutions : (dénombrement :) sol0 nbsol (1 sol :) solSi1 (inf sol :) noyau xp solInf (solutions :) sol
    # opérations entre matrices : somme prod

    # =========== CREATION DE LA MATRICE (constructeur et méthodes qu'il appel) ===========

    # constructeur
    def __init__(self, saisie = False, hasard = False, identite=False, nbl = 0, nbc = 0, matrice = [], minNbl = 2, maxNbl = 8, minNbc = 2, maxNbc = 8, minVals = -25, maxVals = 25) :
        if saisie :
            nbl, nbc, matrice = self.saisie()
        elif hasard :
            nbl, nbc, matrice = self.hasard(minNbl, maxNbl, minNbc, maxNbc, minVals, maxVals)
        elif identite :
            nbl, nbc, matrice = self.identite(nbl)
        self.nbl = nbl
        self.nbc = nbc
        self.matrice = matrice
    
    # saisie manuelle de la matrice pour le constructeur, valeur par valeur
    def saisie(self) :
        print()
        print("Saisie de la matrice :")
        nbl = int(input("Nombre de lignes : "))
        nbc = int(input("Nombre de colonnes : "))
        matrice = []
        for i in range(nbl) :
            ligne = []
            for j in range(nbc) :
                valeur = int(input(f"a{i}{j} : "))
                ligne.append(valeur)
            matrice.append(ligne)
        return nbl, nbc, matrice

    # remplissage de la matrice au hasard, pour le constructeur, avec limites éventuellement indiquées manuellement
    # (cf menu.py, appliquerChoix, choix 1)
    def hasard(self, minNbl, maxNbl, minNbc, maxNbc, minVals, maxVals) :
        nbl = random.randint(minNbl, maxNbl)
        nbc = random.randint(minNbc, maxNbc)
        matrice = []
        for i in range(nbl) :
            ligne = []
            for j in range(nbc) :
                valeur = random.randint(minVals, maxVals)
                ligne.append(valeur)
            matrice.append(ligne)
        return nbl, nbc, matrice

    # =========== REPRESENTATION TEXTUELLE ===========
    
    # créé une représentation de la matrice sous forme de string, et la renvoie
    def __repr__(self, espace = 6, decalage = 0) :
        strMat = ""
        for ligne in self.matrice :
            strMat += " " * decalage
            strMat += "[ "
            for valeur in ligne :
                strVal = self.normaliserLargeur(valeur, espace, 3)
                strMat += strVal + " "
            strMat += "]\n"
        return strMat
    
    # créé une représentation normalisée d'un nombre
    # en vue de l'affichage de la matice, pour éviter d'avoir des valeurs décallées en fonction des valeurs présentes
    # permet d'indiquer une précision pour le float, et la largeur souhaitée d'une colonne
    def normaliserLargeur(self, n, largeur, precision) :
        chaine = str(round(n, precision))
        while len(chaine) < largeur :
            chaine += " "
        return chaine

    # =========== PROPRIETES MATRICE ===========

    # renvoie le nombre de variables libres de la matrice
    # note : matrice self considérée comme augmentée
    def nullity(self) :
        mrref = self.rref()
        libres, pivots = self.indicesLibresPivots()
        nullity = len(libres)
        return nullity
    
    # renvoie deux listes, correspondant respectivement aux indices :
    # des variables libres
    # des variables pivots
    def indicesLibresPivots(self) :
        mrref = self.rref()
        libres = []
        pivots = []
        for ligne in range(self.nbl) :
            # trouve le pivot de la ligne
            trouvePivot = False
            col = 0
            if ligne == 0 :
                pivots.append(0)
                trouvePivot = True
                col += 1
            else :
                col = pivots[-1] + 1
                while col in libres :
                    col += 1
            while col <= self.nbc - 2 :
                if not trouvePivot and mrref.matrice[ligne][col] == 1 :
                    pivots.append(col)
                    trouvePivot = True
                elif mrref.matrice[ligne][col] != 0 and col not in libres :
                    libres.append(col)
                col += 1
        return libres, pivots

    # =========== MATRICES PARTICULIERES ===========

    # renvoie une matrice identité, des dimensions demandées
    # TODO : classmethod ?
    def identite(self, n) :
        matrice = []
        for i in range(n) :
            ligne = []
            for j in range(n) :
                if i == j :
                    ligne.append(1)
                else :
                    ligne.append(0)
            matrice.append(ligne)
        return n, n, matrice

    # renvoie une version transposée de la matrice
    def transposeReturn(self) :
        transp = []
        for j in range(self.nbc) :
            ligne = []
            for i in range(self.nbl) :
                ligne.append(self.matrice[i][j])
            transp.append(ligne)
        transp = Matrice(nbl=self.nbc, nbc=self.nbl, matrice=transp)
        return transp
    
    # transpose la matrice elle même directement, ne renvoie rien
    # TODO : pas utilisé pour le moment. Utiliser ? Supprimer ?
    def transposeInplace(self) :
        transp = self.transposeReturn()
        self.nbl, self.nbc, self.matrice = transp.nbl, transp.nbc, transp.matrice

    # renvoie une version échelonnée réduite de la matrice
    def rref(self) :
        pivotCol = 0 # progression sur les colonnes (matrice passée en RREF dans cols d'avant)
        pivotLigne = 0 # dernière position pivot, avant => calculs déjà faits
        parcoursLigne = 0 # pour regarder au delà du pivot quand on tombe que sur des 0 dans la colonne
        copie = copy.deepcopy(self)
        while pivotLigne < self.nbl and pivotCol < self.nbc : # tant qu'on est pas en RREF
            # si 0 en position pivot, échanger avec prochaine ligne sans 0 en pivotCol
            while parcoursLigne < self.nbl and copie.matrice[parcoursLigne][pivotCol] == 0 :
                parcoursLigne += 1
            if parcoursLigne == self.nbl : # si on a parcouru toute la colonne en ne rencontrant que de 0, on passe à la suivante
                pivotCol += 1
                parcoursLigne = pivotLigne
                continue
            if parcoursLigne > pivotLigne :
                copie.matrice[pivotLigne], copie.matrice[parcoursLigne] = copie.matrice[parcoursLigne], copie.matrice[pivotLigne]
            # passe pivot à 1
            diviseur = copie.matrice[pivotLigne][pivotCol]
            for i in range(self.nbc) :
                copie.matrice[pivotLigne][i] /= diviseur
            # annule colonne sauf pivot
            lignesSaufPivot = list(range(self.nbl))
            lignesSaufPivot.pop(pivotLigne)
            for i in lignesSaufPivot :
                facteur = copie.matrice[i][pivotCol]
                for j in range(self.nbc) :
                    copie.matrice[i][j] -= facteur * copie.matrice[pivotLigne][j]
            pivotCol += 1
            pivotLigne += 1
            parcoursLigne = pivotLigne
        return copie
        
    # calcule et renvoie l'inverse de la matrice
    def inverse(self) :
        if self.nbl != self.nbc :
            return "la matrice doit être carré pour posséder un inverse"
        idm = Matrice(identite=True, nbl=self.nbl)
        copie = copy.deepcopy(self)
        for i in range(self.nbl) :
            copie.matrice[i] += idm.matrice[i]
        copie.nbc *= 2
        mrref = copie.rref()
        invValeurs = []
        for i in range(mrref.nbl) :
            invValeurs.append(mrref.matrice[i][self.nbc:])
        inv = Matrice(nbl = self.nbl, nbc = self.nbc, matrice=invValeurs)
        return inv

    # =========== SOLUTIONS ET LEURS NOMBRES ===========
    
    # renvoie un booléen indiquant si la matrice a 0 solutions ou non
    # note : matrice self considérée comme augmentée
    def sol0(self) :
        mrref = self.rref()
        for i in range(self.nbl) :
            if sum([abs(i) for i in mrref.matrice[i][:-1]]) == 0 and mrref.matrice[i][-1] != 0 :
                return True
        return False
    
    # renvoie le nombre de solutions de la matrice
    # note : matrice self considérée comme augmentée
    def nbSol(self) :
        if self.sol0() :
            return 0
        elif self.nullity() > 0 :
            return math.inf
        else :
            return 1
    
    # renvoie la solution, si la matrice n'en a qu'une
    # (à n'utiliser que dans ce cas)
    def solSi1(self) :
        mrref = self.rref()
        sol = []
        for i in mrref.matrice :
            sol.append(i[-1])
        return sol
    
    # renvoie le noyau de la matrice
    # (les vecteurs base du sous espace dont l'image par la matrice est l'origine)
    # TODO : améliorer une fois que j'aurais créé la classe vecteur
    def noyau(self) :
        mrref = self.rref()
        libres, pivots = self.indicesLibresPivots()
        noyau = []
        for colLibre in libres :
            vecteur = []
            cptPivots = 0
            for col in range(mrref.nbc) :
                if col in pivots :
                    logging.debug("cptPivots : " + str(cptPivots))
                    logging.debug("col : " + str(col))
                    vecteur.append(-mrref.matrice[cptPivots][colLibre])
                    cptPivots += 1
                elif col == colLibre :
                    vecteur.append(1)
                else :
                    vecteur.append(0)
            noyau.append(vecteur)
        return noyau
    
    # calcule une solution particulière de la matrice
    # utilisé pour le calcul de la solution générale, quand la matrice a une infinité de solutions
    # considérer la matrice comme étant augmentée
    def xp(self) :
        mrref = self.rref()
        libres, pivots = self.indicesLibresPivots()
        xp = []
        nbPivotsVerifies = 0
        for col in range(mrref.nbc) :
            if col in pivots :
                xp.append(mrref.matrice[nbPivotsVerifies][mrref.nbc-1])
                nbPivotsVerifies += 1
            else :
                xp.append(0)
        return xp
    
    # calcule les solutions et créé un string pour affichage
    # a utiliser si la matrice a une infinité de solutions
    def solInf(self) :
        strSol = ""
        xp = self.xp()
        x0 = self.noyau()
        strSol += "Infinité de solutions. Solution générale X = Xp + c * Xn :\n"
        for col in range(self.nbc - 1) :
            strXp = self.normaliserLargeur(xp[col], 6, 3)
            strSol += "[ " + strXp + " ] "
            if col == self.nbc - 2 :
                strSol += " + c1 [ "
            else :
                strSol += "      [ "
            for vect in range(len(x0)) :
                valX0 = x0[vect][col]
                strX0 = self.normaliserLargeur(valX0, 6, 3)
                strSol += strX0 + "]"
                if vect != len(x0) - 1 :
                    if col == self.nbc - 2 :
                        strSol += " + c" + str(vect+2) + " [ "
                    else :
                        strSol += "      [ "
                elif col != self.nbc - 2 :
                    strSol += "\n"
        return strSol
    
    # renvoie les solutions de la matrice
    # détermine le nombre de solutions, puis appelle les méthodes nécessaires en fonction
    def sol(self) :
        nbSolutions = self.nbSol()
        if nbSolutions == 0 :
            return "aucune"
        elif nbSolutions == math.inf :
            return self.solInf()
        elif nbSolutions == 1 :
            return self.solSi1()
        else :
            return "problème : pour nombre de solutions, ne trouve ni 0, ni 1, ni l'infini"

    # =========== OPERATIONS ENTRE MATRICES ===========
    
    # renvoie la somme de la matrice avec une autre si elles ont même dimensions
    # sinon : prévient que le calcul est impossible + renvoie une matrice vide
    def somme(self, m2) :
        resultat = []
        if self.nbl != m2.nbl or self.nbc != m2.nbc :
            logging.WARNING("les matrices n'ont pas les mêmes dimensions, et ne peuvent être ajoutées.")
        else :
            for i in range(self.nbl) :
                ligne = []
                for j in range(self.nbc) :
                    valeur = self.matrice[i][j] + m2.matrice[i][j]
                    ligne.append(valeur)
                resultat.append(ligne)
        resultat = Matrice(nbl=self.nbl, nbc=self.nbc, matrice=resultat)
        return resultat

    # renvoie le produit de la matrice avec une autre
    def produit(self, m2) :
        resultat = []
        if self.nbc != m2.nbl :
            print("La première matrice doit avoir autant de colonnes que la seconde n'a de lignes")
        else :
            for i in range(self.nbl) :
                ligne = []
                for j in range(m2.nbc) :
                    valeur = 0
                    for k in range(self.nbc) :
                        valeur += self.matrice[i][k] * m2.matrice[k][j]
                    ligne.append(valeur)
                resultat.append(ligne)
        resultat = Matrice(nbl=self.nbl, nbc=m2.nbc, matrice=resultat)
        return resultat