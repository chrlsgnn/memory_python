# importation des modules necesaires
from tkinter import *
from random import shuffle

def avoir_une_grille_mélangée():
	# création une grille 4x4 mélangée, c'est une liste de 4 listes de 4 entiers:
	# pas d'argument en entrée et doit renvoyer une une liste de 4 listes de 4 entiers 
	# aléatoires entre 1 et 8 (deux de chaque)
	# on remplacera cette valeure par -1 si l'image a retrouvé sa paire 
	liste = list(range(1,9))*2
	shuffle(liste)
	tab = []
	for i in range(4):
		l = []
		for j in liste[i*4:i*4+4]:
			l.append(j)
		tab.append(l)
	return tab

def créer_liste_images():
	# créer une liste nommée lst_images avec dedans les objets image que l'on placera sur le canvas
	# a l'aide d'une grille aléatoire (explications ci dessus):
	lst_noms = ["image_1", "image_2", "image_3", "image_4", "image_5", "image_6", "image_7", "image_8"]
	lst_images =[]
	for i in lst_noms:
		image=PhotoImage(file=i+".png")
		lst_images.append(image)
	return lst_images

def remplire_grille():
	# on place des images aléatoirement comme sur une grille, par pair
	# on les recouvre par le logo de notre entreprise
	# on stocke leur identifiant dans une liste (chaque element placé sur un canvas dispose d'un identifiant)
	liste_id_logos = []
	for i in range(4):
		liste_d_identifiants = []
		for j in range(4):
			numéro=grille[i][j]
			image=lst_images[numéro-1]
			centre=(60+i*110, 60+j*110)
			cnv.create_image(centre, image=image)
			identifiant = cnv.create_image(centre, image=logo)
			liste_d_identifiants.append(identifiant)
		liste_id_logos.append(liste_d_identifiants)
	return liste_id_logos

def clic(event):
	# cliquer sur le canvas, identifier a quelle image et a quel logo le clique correspond
	# (car même si on couvre chaque image par le meme logo, ils on leur a tous attribué un 
	# identifiant unique)
	# faire attention a ce que si on reclique sur une image deja cliquée, on ne re supprime pas le logo et 
	# son identifiant car cela peut créer des bugs
	if etat[1] is not None:
		return # pour sortire de la fonction
	if grille[event.x//110][event.y//110] != -1:
		verifier_clic(event.x//110, event.y//110)

def verifier_clic(ligne, colone):
	# supprime la carte de couverture
	item=liste_id_logos[ligne][colone]
	cnv.delete(item)
	# teste de si on est au premier clic
	if etat[0] is None:
		etat[0]=(ligne, colone)
	# si non on est au deuxième clique
	else:
		# si on reclique sur la meme image, on sort de la fonction avec return
		if etat[0]==(ligne, colone):
			return 
		# on a donc pas besoin de else 
		etat[1]=(ligne, colone)
		i, j=etat[0]
		# si les 2 images cliquées sont les memes, on les laisse "alumées"
		if grille[i][j]==grille[ligne][colone]:
			grille[i][j]=grille[ligne][colone]=-1
			etat[0]=etat[1]=None
		# si non on les re eteint avec la fonction cacher
		# after sers a attendre 1/2 seconde avans de le faire
		else:
			cnv.after(500, cacher, i,j, ligne, colone)

def cacher(i, j, ligne, colone):
	# on remet un cache sur les images si cette fonction est apelée 
	# et on met a jour son identifiant dans la liste
	# on presise ensuite que plus aucune image n'est allumée
	centre=(60+i*110, 60+j*110)
	liste_id_logos[i][j] = cnv.create_image(centre, image=logo)
	centre=(60+ligne*110, 60+colone*110)
	liste_id_logos[ligne][colone] = cnv.create_image(centre, image=logo)
	etat[0], etat[1] = None, None

##############################  programme principale  ##############################
# creation de la fenetre et du canvas
fen=Tk()
cnv=Canvas(fen, width=446, height=446, background='black')
cnv.pack()

# création de l'objet image qui cachera les autres images du jeu, on le nomme logo
logo=PhotoImage(file='./Mem_Dos.png')

# création de la liste d'images
lst_images = créer_liste_images()

# création de la grille aléatoire
grille = avoir_une_grille_mélangée()

# création de la liste avec les id de chaque logo
liste_id_logos = remplire_grille()

# etat de l'avancement des clics (None si pas de clic fait, si un clic a ete fait, on lui ajoute
# un tuple avec les coordonées du clic et donc de l'image retournée, 
#deux tuples si deux images sont cliquées)
etat=[None, None]

# La méthode bind() permet de lier un événement avec une fonction :
# un clic de souris sur la surface provoquera l'appel de la fonction clic()
cnv.bind("<Button>", clic)

# lancement de la fenetre
fen.mainloop() 
