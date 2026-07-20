import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def box_muller(I,sigma=1.0):
    """Génère une matrice de bruit gaussien adaptée aux dimensions d'une image.

    Cette fonction calcule une matrice de bruit B dont chaque élément suit une
    loi normale centrée N(0, sigma^2) via la méthode de Box-Muller. La taille
    de B est calquée sur la forme (Hauteur, Largeur, Canaux) de la matrice I.

    Args:
        I (np.darray): mtrice de l'image d'origine (I)
            de forme (H, W, 3).
        sigma (float, optional): L'écart-type de la loi normale, contrôlant
            l'intensité du bruit. Par défaut à 1.0.

    Returns:
        numpy.ndarray: La matrice de bruit (B) de mêmes dimensions et même
            forme que l'image d'origine, contenant les variables gaussiennes.
        numpy.ndarray: Un vecteur contenant les variables aléatoires de lois N(0,sigma^2)
            que l'on comparera à la courbe théorique de la loi N(0,sigma^2).
    """
    H = I.shape[0]
    W = I.shape[1]
    n_target = H * W * 3
    n_total = n_target

    rng = np.random.default_rng()
    B = rng.uniform(low=1e-15, high=1.0, size=(H, W, 3))

    flat_unif = B.ravel()

    # Ajout d'une variable uniforme pour rendre le total pair car Box Muller prend 2 entrées pour 2 sorties
    if n_total % 2 != 0:
        u_extra = rng.uniform(low=1e-15, high=1.0, size=1)
        flat_unif = np.concatenate([flat_unif, u_extra])
        n_total += 1

    # Box-Muller
    u1 = flat_unif[::2]
    u2 = flat_unif[1::2]

    r = np.sqrt(-2 * np.log(u1))
    theta = 2 * np.pi * u2

    z0 = sigma * r * np.cos(theta)
    z1 = sigma * r * np.sin(theta)

    flat_normal = np.empty(n_total)
    flat_normal[::2] = z0
    flat_normal[1::2] = z1

    B = flat_normal[:n_target].reshape(H, W, 3)
    return B


def valider_bruit_gaussien(B,sigma_th):
    """Affiche une analyse graphique de la matrice de bruit.

        Cette fonction permet de valider empiriquement le générateur de Box-Muller
        en comparant l'histogramme des valeurs générées avec la courbe théorique
        de la loi normale N(0, sigma^2).

        Args:
            matrice_bruit (numpy.ndarray): La matrice de bruit générée à analyser.
            sigma_theorique (float): L'écart-type théorique utilisé lors de la génération.

        Returns:
            None: La fonction affiche un graphique Matplotlib et des prints textuels.
    """
    Var = B.flatten()
    #Histogramme empirique
    plt.hist(Var, bins=30, density=True, alpha=0.6, color="g", label="Empirique")

    #Courbe théorique
    x = np.linspace(Var.min(), Var.max(), 200)
    pdf_theorique = norm.pdf(x, loc=0, scale=sigma_th)
    plt.plot(x, pdf_theorique, "r-", lw=2, label="Théorique")

    plt.title("Comparaison Histogramme vs Densité Théorique")
    plt.xlabel("Valeurs")
    plt.ylabel("Densité")
    plt.legend()
    plt.show()
    return None

def generer_bruit_gaussien(I,sigma):
    """Génère une version bruitée d'une image et renvoie l'image bruitée ainsi que le bruit appliqué.

        Cette fonction génère une matrice de bruit gaussien centrée à l'aide de la
        méthode de Box-Muller, l'ajoute à l'image d'origine (normalisée entre 0.0 et 1.0),
        puis re-quantifie le résultat dans l'intervalle [0, 255] au format uint8.

        Args:
            I (numpy.ndarray): Image d'entrée sous forme de matrice (généralement uint8).
            sigma (float): Écart-type du bruit gaussien à générer.

        Returns:
            tuple[numpy.ndarray, numpy.ndarray]:
            - I_bruite (numpy.ndarray): L'image finale bruitée au format uint8 (valeurs entre 0 et 255).
            - B (numpy.ndarray): La matrice du bruit gaussien généré par Box-Muller.
        """
    B = box_muller(I,sigma)
    # Conversion et normalisation entre 0.0 et 1.0 (en float32 pour économiser la mémoire)
    I = I.astype(np.float32)/255
    I_bruite = I + B 
    I_bruite = np.clip(I_bruite,0,1)
    I_bruite = (I_bruite*255).astype(np.uint8)
    return I_bruite,B