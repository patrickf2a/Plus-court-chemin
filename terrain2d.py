import tkinter as tk
import numpy as np
from math import *
from heapq import heappush as enfiler
from heapq import heappop as defiler
from tkinter import Canvas, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

######################### Fenetre ##############################################
# fenetre principal
root = tk.Tk()
root.geometry("900x950")  # taille
root.title("Projet Infographie 2D ")  # titre
root.resizable(width=False, height=False)

height = 900  # longueur
width = 900  # hauteur

######################## Variables globales #####################################

depart_chemin, arrivee_chemin = None, None
dimension_grille = 30
dim_carre = height // dimension_grille
coutmax = 15
ligne = 30
colonne = 30

######################### Label ################################################

# label associé à une variable
variable = tk.StringVar()
variable.set("Bienvenue !")
aff_cout = tk.Label(root, textvariable=variable)
aff_cout.pack(side="top")


variable_deux = tk.StringVar()
aff_cout_deux = tk.Label(root, textvariable=variable_deux)
aff_cout_deux.pack(side="bottom")


###################### Canvas ##################################################
# Canvas
moncanvas = tk.Canvas(root, height=height, width=height)
moncanvas.pack(side="top", expand=True, fill="both")

#################################### Bezier ####################################
def calcul_barycentre(A, B, t):
    x = (1 - t) * A[0] + t * B[0]
    y = (1 - t) * A[1] + t * B[1]
    return (x, y)


def liste_barycentre(L, t):
    liste_bary = []
    for i in range(len(L) - 1):
        liste_bary += [calcul_barycentre(L[i], L[i + 1], t)]
    return liste_bary


def point_control_bezier(points, t):
    n = len(points)
    # On calcule les barycentre jusqu'à obtenir qu'un seul point
    while n > 1:
        points = liste_barycentre(points, t)
        n = len(points)
    return points[0]


def courbe_Bezier(points):
    n = len(points)
    u = 1.0 / 100
    t = u
    liste_point = [points[0]]
    while t < 1.0:
        liste_point += [point_control_bezier(points, t)]
        t += u
    return liste_point


################################### Generation de matrice ######################


def indice_voisin(x, coords):
    """ Fonctions qui prend en coordonnées d'un elément de la matrice et elle génère
    un itérateur qui donne le couple (valeur,(coordonnées)) pour chacun de ses voisins
    """
    r, c = coords
    for rc, val in np.ndenumerate(
        M[
            max(0, r - 1) : min(r + 2, M.shape[0]),
            max(0, c - 1) : min(c + 2, M.shape[1]),
        ]
    ):
        lig, col = rc
        lig += max(r - 1, 0)
        col += max(c - 1, 0)
        yield (val, (lig, col))


def dist(l1, l2):
    # distance euclidienne
    return isqrt(sum((b - a) ** 2 for a, b in zip(l1, l2)))


def filtre_median(mat):
    """ Fonction qui applique le filtre de Tukey sur une matrice
    """
    l = np.empty(shape=mat.shape, dtype=int)
    for coords in np.ndindex(l.shape) :
        l[coords] = np.median(
            np.take(
                mat,
                mat[
                    coords[0] - 1 if coords[0] > 0 else 0 : coords[0] + 2,
                    coords[1] - 1 if coords[1] > 0 else 0 : coords[1] + 2,
                ],
                mode="clip",
            )
        )
    return l


def gen_matrice(l, c):
    """Fonction qui genere une matrice aleatoire et lui applique un filtre
    median afin d'obtenir la mediane"""
    data = np.random.randint(1, 10, size=(l, c))
    dataf = filtre_median(data)
    return dataf

############################# PLUS COURT CHEMIN ################################

def dijkstra(G, depart, arrivee):
    """Fonction de plus court chemin Dijkstra avec ;
    G= matrice generer
    depart=indice de depart au moment du clic
    arrivee = indice de depart au moment du deuxieme clic
    """

    sommets_possibles = []
    enfiler(sommets_possibles, (0, depart, None))
    dict_predecesseur = {}
    while sommets_possibles:
        distance, sommet, predecesseur = defiler(sommets_possibles)

        if sommet in dict_predecesseur:
            continue
        dict_predecesseur[sommet] = predecesseur
        if sommet == arrivee:
            chemin = []
            while sommet:
                chemin.append(sommet)
                sommet = dict_predecesseur[sommet]
            return chemin
        for distance_candidat, candidat in indice_voisin(G, sommet):
            if candidat in dict_predecesseur:
                continue
            # print(candidat)
            enfiler(sommets_possibles, (distance + distance_candidat, candidat, sommet))
    return []


def A_star(G, depart, arrivee):
    """Fonction de plus court chemin A* avec :
    G= matrice generer
    depart = indice de depart au moment du clic
    arrivee = indice d'arrivee' au moment du deuxieme clic
    """

    sommets_possibles = []
    enfiler(sommets_possibles, (0, depart, None))
    dict_predecesseur = {}
    while sommets_possibles:
        distance, sommet, predecesseur = defiler(sommets_possibles)
        if sommet in dict_predecesseur:
            continue
        dict_predecesseur[sommet] = predecesseur
        if sommet == arrivee:
            chemin = []
            while sommet:
                chemin.append(sommet)
                sommet = dict_predecesseur[sommet]
            return chemin
        for distance_candidat, candidat in indice_voisin(G, sommet):
            if candidat in dict_predecesseur:
                continue
            enfiler(
                sommets_possibles,
                (
                    distance + distance_candidat + int(dist(candidat, arrivee)),
                    candidat,
                    sommet,
                ),
            )
    return []


################################### TERRAIN ####################################
def moyenne(liste): # pas utile dans notre cas
    """
    Fait la moyenne d'une liste
    """

    sum = 0
    for i in liste:
        sum += i
    return sum / len(liste)


def codecouleur(rgb):
    """Fonction qui retourne la valeur rgb en hexa"""
    r, g, b = rgb
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def gen_terrain(mat):
    """Fonction qui génère un terrain selon la matrice generer.
    mat=matrice generer aleatoirement """

    dim_carre = height // dimension_grille
    for i in range(dimension_grille):
        for j in range(dimension_grille):
            x = i * dim_carre
            y = j * dim_carre
            le_cout = mat[i][j]
            # print(le_cout)
            # if (i==0 or j==0 or i== dimension_grille-1 or j==dimension_grille-1):
            #   le_cout=0
            couleur = (le_cout * 256 // coutmax)
            rgb = codecouleur((couleur, couleur, couleur))
            moncanvas.create_rectangle(
                x, y, x + dim_carre, y + dim_carre, fill=rgb, activefill="red", width=0
            )
            # moncanvas.create_text(x+12,y+12,text=(le_cout)) #affiche le cout
    return None

################################## AFFICHAGE DU CHEMIN ET DU DEPLACEMENT #########################
def affiche_chemin(event=None):
    """Fonction qui affiche le plus chemin entre deux point selectionné"""
    global depart_chemin, arrivee_chemin, courbe, courbe_deux, chemin_astar, chemin_dijkstra

    ## Pour creation des serpent et selection point d'arriver de depart
    coords = moncanvas.coords("current")
    x = int(coords[0])
    y = int(coords[1])
    res = (
        int(coords[1]) // dimension_grille,
        int(coords[0]) // dimension_grille,
    )  # recuperation des tags
    Ver_un = [[x - 3, y - 3], [x + 5, y + 5], [x + 10, y + 10], [0, 0]]
    Ver_deux = [[x - 3, y - 3], [x + 5, y + 5], [x + 10, y + 10], [0, 0]]

    if depart_chemin is None:
        # On rentre dans la boucle quand on clique n'importe ou sur le terrrain
        depart_chemin = res
        # moncanvas.update()
        moncanvas.create_oval(
            x, y, x + dim_carre, y + dim_carre, fill="blue", tag="current"
        )  # point de depart

        moncanvas.delete("point","point1")
        #### Creation des trois sphere pour le ver un
        verun = moncanvas.create_oval(
            Ver_un[0][0],
            Ver_un[0][1],
            Ver_un[0][0] + 18,
            Ver_un[0][1] + 18,
            outline="black",
            fill="orange",
            tag="point",
        )

        verun = moncanvas.create_oval(
            Ver_un[1][0],
            Ver_un[1][1],
            Ver_un[1][0] + 15,
            Ver_un[1][1] + 15,
            outline="black",
            fill="orange",
            tag="point",
        )

        verun = moncanvas.create_oval(
            Ver_un[2][0],
            Ver_un[2][1],
            Ver_un[2][0] + 10,
            Ver_un[2][1] + 10,
            outline="black",
            fill="orange",
            tag="point",
        )

        #### Creation des trois sphere pour le ver deux
        verdeux = moncanvas.create_oval(
            Ver_deux[0][0],
            Ver_deux[0][1],
            Ver_deux[0][0] + 20,
            Ver_deux[0][1] + 18,
            outline="black",
            fill="yellow",
            tag="point1",
        )

        verdeux = moncanvas.create_oval(
            Ver_deux[1][0],
            Ver_deux[1][1],
            Ver_deux[1][0] + 15,
            Ver_deux[1][1] + 15,
            outline="black",
            fill="yellow",
            tag="point1",
        )

        verdeux = moncanvas.create_oval(
            Ver_deux[2][0],
            Ver_deux[2][1],
            Ver_deux[2][0] + 10,
            Ver_deux[2][1] + 10,
            outline="black",
            fill="yellow",
            tag="point1",
        )

    else:
        # On rentre dans la boucles ou un deuxieme endroit à été cliqué
        arrivee_chemin = res
        moncanvas.create_oval(
            x, y, x + dim_carre, y + dim_carre, fill="green", tag="current"
        )  # point d'arrivee
        # On execute les deux focntions du plus court chemin
        chemin_dijkstra = dijkstra(M, depart_chemin, arrivee_chemin)
        chemin_astar = A_star(M, depart_chemin, arrivee_chemin)

        # On créé les courbes de bezier selon les deux chemins
        courbe = courbe_Bezier(chemin_dijkstra)
        courbe_deux = courbe_Bezier(chemin_astar)

        # Affiche une bar d'etat expliquant les differentes courbes
        variable.set(
            "Courbe de bezier pour Dijkstra en rouge | Courbe de bezier pour A Star en jaune "
        )
        moncanvas.after(20, None)  # attente voulu pour que ce sois plus agreables
        cout_dijkstra = 0
        ###### On fait Dijkstra en premier
        for i in chemin_dijkstra[1:-1]:
            # On garde ses ligne en commentaire car elle peuvent servir pour savoir
            # qu'elle est le chemin selon les indices des cases
            # x,y=i
            # id_carre=moncanvas.find_closest((y*dimension_grille),x*dimension_grille)
            # moncanvas.itemconfigure(id_carre,fill="green")
            for ligne in courbe:
                x = ligne[1]
                y = ligne[0]
                # deplacement(obj,courbe)
                moncanvas.update()
                moncanvas.create_line(
                    x * dim_carre + dim_carre / 2 + 1,
                    y * dim_carre + dim_carre / 2,
                    x * dim_carre + dim_carre / 2,
                    y * dim_carre + dim_carre / 2,
                    fill="red",
                    width=3,
                )

            cout_dijkstra += M[i]  # lecout

        # print(f"cout Dijkstra: {s}, longeur : {len(S)}")

        cout_Astar = 0
        moncanvas.after(20, None)  # attente voulu pour que ce sois plus agreables
        ###### On fait A_star en second
        for i in chemin_astar[1:-1]:
            # Afiche le chemin selon les indices des cases
            # x,y=i
            # moncanvas.find_closest(y*dimension_grille,x*dimension_grille)
            # moncanvas.itemconfigure(id_carre,fill="yellow")#type:ignore
            for ligne_deux in courbe_deux:
                x = ligne_deux[1]
                y = ligne_deux[0]
                moncanvas.update()
                moncanvas.create_line(
                    x * dim_carre + dim_carre / 2 + 1,
                    y * dim_carre + dim_carre / 2,
                    x * dim_carre + dim_carre / 2,
                    y * dim_carre + dim_carre / 2,
                    fill="yellow",
                    width=3,
                )

            cout_Astar += M[i]
            depart_chemin,arrivee_chemin=None,None
        variable_deux.set(
            f"cout Dijkstra: {cout_dijkstra}, longeur : {len(chemin_dijkstra)} | "
            f"cout A* : {cout_Astar}, longeur : {len(chemin_astar)}"
        )

        ############# Je compare le chemin optimal et chaque ver le prend ##########

        if len(chemin_astar) > len(chemin_dijkstra):
            """
            Si la longeur de astar est plus grande que dijkstra alors les deux
            vers vont prend le chemin de dijkstra
            """
            moncanvas.after(20, None)
            deplacement_ver("point", courbe)

            moncanvas.after(20, None)
            deplacement_ver("point1", courbe)

        elif len(chemin_astar) == len(chemin_dijkstra):
            """
            Si les deux chemins sont égaux alors chaque vers prend un chemin differentes
            """

            moncanvas.after(20, None)
            deplacement_ver("point", courbe)

            moncanvas.after(20, None)
            deplacement_ver("point1", courbe_deux)

        else:
            """
            Sinon les deux vers vont prendre le chemin de A_star
            """
            moncanvas.after(20, None)
            deplacement_ver("point", courbe_deux)

            moncanvas.after(20, None)
            deplacement_ver("point1", courbe_deux)

    return None


# Je bind le bouton pour afficher l'animation
moncanvas.bind("<1>", affiche_chemin)

# Il va au point souhaite
def deplacement_ver(ver, chemin):
    """
    Fonction qui realise le deplacement d'un objet selon un chemin donnee
    """
    for i in range(len(chemin) - 1):
        if i < len(chemin) - 1 :
            moncanvas.update()
            moncanvas.move(
                ver,
                (chemin[i][1] - chemin[i - 1][1]) * dim_carre,
                (chemin[i][0] - chemin[i - 1][0]) * dim_carre,
            )
            moncanvas.after(30, None)
        i += 1

########################### MENU ###############################################
def MenuBar():
    barremenu = tk.Menu(root, bg="gray25", fg="white", bd=0)

    # Menu Fichier
    fichier = tk.Menu(barremenu, tearoff=0, bg="gray25", fg="white")
    barremenu.add_cascade(label="Fichier", menu=fichier)
    fichier.add_command(label="Nouveau", command=nouveau)
    fichier.add_command(label="Ouvrir", command=ouvrir)
    fichier.add_command(label="Enregistrer", command=enregistrer)
    fichier.add_separator()
    fichier.add_command(label="Quitter", command=quitter)

    # Menu Aide
    aide = tk.Menu(barremenu, tearoff=0, bg="gray25", fg="white")
    barremenu.add_cascade(label="Aide", menu=aide)
    aide.add_command(label="Fonctionnement", command=maide)
    aide.add_command(label="A propos", command=apropos)

    root.config(menu=barremenu)


def ouvrir():
    """Fonction qui charge une scene"""
    filename = askopenfilename(
        title="Ouvrir un fichier",
        filetypes=[("Données", ".npy"), ("Tous les fichiers", ".*")],
    )
    if filename:
        moncanvas.delete("all")
        # Je load la matrice du terrrain
        m = np.load(filename, allow_pickle=True)
        # Je genere le terrain
        gen_terrain(m)


# ENREGISTRER UN FICHIER
def enregistrer():
    """Fonction qui enregistre une scene"""
    filename = asksaveasfilename(
        title="Enregistrer sous ...",
        filetypes=[("Fichier ", ".npy")],
        defaultextension=".npy",
    )
    # Je save dans le fichier la matrice M
    if filename:
        np.save(filename, M)


# QUITTER L'APPLICATION
def quitter():
    """Fonction pour quitter l'application"""
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
        root.destroy()


def nouveau():
    """Fonction pour tout effacer et reaffiche la grille"""
    global depart_chemin, arrivee_chemin
    moncanvas.delete("all")  # on efface tout le contenu du canvas
    gen_terrain(gen_matrice(30, 30))  # je genere un nouveau terrrain
    depart_chemin, arrivee_chemin = None, None


# MENU AIDE
def apropos():
    messagebox.showinfo("Application ", "FERNANDES DE FARIA Patrick \n DOMENGE TOM")


def maide():
    messagebox.showinfo("Fonctionnement","Fonctionnement de l'application: \n  - On peut selectionner un point de départ nimporte ou sur le terrain. \n - On peut selectionner un point d'arrivée nimporte ou sur le terrain. \n - On peut generer un nouveau terrain. \n - On peut enregistrer un terrain dans un fichier. \n - On peut crée un terrain a partir d'un fichier. \n - On peut quitter l'application. \n - On peut aussi prendre du plaisir a utiliser cette aplication.  ")


##################################### MAIN #####################################
MenuBar()
M = gen_matrice(ligne, colonne)
gen_terrain(M)
root.protocol("WM_DELETE_WINDOW", quitter)

try:
    root.mainloop()
except tk.TclError:
    """Erreur qui peut se produire si l'on ferme la fenêtre alors que l'animation est encore en cours
    (si le canvas est détruit)"""
    pass
