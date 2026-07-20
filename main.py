import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import fonctions

nom = str(input("Entrez le nom (avec l'extension (png/jpg/jpeg)) : "))
img = Image.open(nom).convert("RGB")

# Conversion en array Numpy de taille (H,W,3)

img_array = np.array(img)
img.close()
continuer = True
while continuer :
    sigma = float(input("Entrez une valeur de sigma (positif (ou négatif pour sortir du programme)) pour régler l'intensité du bruit : "))
    if sigma < 0 :
        continuer = False
    else :
        img_bruite,bruit = fonctions.generer_bruit_gaussien(img_array,sigma)
        fonctions.valider_bruit_gaussien(bruit, sigma)
        img_bruite = Image.fromarray(img_bruite)
        img_bruite.show()
        img_bruite.save("img_bruite.jpeg")