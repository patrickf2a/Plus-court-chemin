# Projet GEOMETRIE ALGORITHMIQUE
# FERNANDES DE FARIA PATRICK
# DOMENGE TOM

#################################### Partie 2D ###################################

######### CONTENUE DOSSIER ###########

-Fichier terrain2d.py : contient l'ensemble des fonctions permettant de :

** Modéliser un terrain.
** Cree des courbes de bezier à partir d'un chemin.
** Le déplacement de deux vers sur leurs chemins respectif.
** La sauvegarde d'un terrain dans un fichier.
** Le chargement d'un terrain à partir d'un fichier.
** La génération d'un terrain grâce à un bouton.
** Quitter l'application à partir d'un bouton.


######## UTILISATION DU PROGRAMME ########

- Exécution du programme : pour ce faire il suffit simplement d'exécuter le programme terrain2d.py,
 il suffit de taper la commande suivante :

 ** python3 terrain2d.py

- Pour ajouter un point de départ, faites un clic gauche sur une case du terrain.

- Pour ajouter un point d'arrivée, faites un clic gauche sur une autre case du terrain.

- Pour sauvegarder un terrain il suffit de cliquer sur "Enregistrer" dans la barre de menu et enregistrer au fichier .npy.

- Pour charger un terrain il suffit de cliquer sur "Ouvrir" dans la barre de menu et ouvrir un terrain déjà sauvegarder.

- Pour générer un terrain il suffit de cliquer sur "Nouveau" dans la barre de menu.


################### PROBLEME RENCONTRER ##########################

- Au niveau du deplacement des deux vers :

  Le déplacement a été implanté avec succès, cependant lors du mouvement du vers
  le milieu du corps et la queue ne suivent pas idéalement comme en temps réel le chemin;
  en effet ils suivent le mouvement de la tête.

- Petite erreur :
  Quand un déplacement est en cours il ne faut pas cliquer sur une autre case du
  terrain car sinon une erreur apparaît.



######################################## Partie 3D #############################

######## UTILISATION DU PROGRAMME ########

- Exécution du programme : pour ce faire il suffit simplement d'exécuter le programme open.py,
 il suffit de taper la commande suivante :

 ** python3 open.py

 - Génère un terrain à partir d'une matrice.

 - Grace au clavier on peut jouer avec la camera grâce aux touches(Z=zoomer;
   S=dezoomer,Q et D permettent de faire des rotations autour de l'axe X)

################### PROBLEME RENCONTRER ##########################

- Lors de la modélisation du terrain, les triangles entres les carre n'ont pas ete cree.
Le probleme est du à la mal compréhension de openGL/3D. :(
