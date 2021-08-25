# fonctions utilisées par tous les fichiers placées ici pour éviter d'avoir à importer tous les fichiers dans tous les fichiers, et éviter les erreurs d'import circulaires

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