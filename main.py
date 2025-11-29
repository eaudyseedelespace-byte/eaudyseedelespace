import matplotlib.pyplot as plt
import math


h = 0.0001# Pas de temps pour l'intégration
v = [0]  # Liste des valeurs de y (commence avec y0)
x = [0]  #liste des valeurs de x ( positino)
g = 9.81  # Accélération due à la gravité (m/s²)     # Masse initiale de la fusée (kg)

Pajouté = 500000  # Pression ajoutée en Pa
Pext = 101325
P0 = Pext + Pajouté
Ae = 0.00005  # surface de la bouche d'éjection m2
Pt = 0  # pression qui change en fonction du temps
dm_dt = 0  # débit massique de l'eau
ve = 0  # equation de bernouilli
Cd = 0.9
rho_eau = 1000
rho_air = 1.225
Afr = (5.81e-3)  # Surface du + grd diamètre de la bouteille (m²)
Aparachute = 0.15 # Surface parachute en m^2
mf = 0.25  # masse fusée
me = [1]  # masse eau

print("avec une pression ajoutée de", Pajouté, "Pa,")

''' Les fonctions différentielles du code '''


def f_x(t, x, v):
    return v  # dérivée de la position est la vitesse


def f_m(t, m, dm_dt):  # la masse en fonction du temps

    return dm_dt  # le débit massique de l'eau dm_dt


def f_v_1(t, dm_dt, ve, mf, me, g, v_courant):
#équation de Tsiolkovski sans parachute, diamètre de la bouteille, force de trainée négative
    thrust = -dm_dt * ve
    Fd = 0.5 * Cd * rho_air * (v_courant ** 2) * Afr
    return ((thrust - (Fd) - (mf + me) * g)) / (mf + me)

def f_v_2(t, dm_dt, ve, mf, me, g, v_courant):
# équation de Tsiolkovski avec parachute, diamètre du parachute, force de trainée positive
    thrust = -dm_dt * ve
    Fd = 0.5 * Cd * rho_air * (v_courant ** 2) * Aparachute
    return ((thrust + (Fd) - (mf + me) * g)) / (mf + me)

'''-------------La Fonction Euler -------------------'''


def euler(t, v, h, dm_dt, ve, mf, me, g, ):
    v = [0]
    x = [0]
    # for i in range(100000):
    while x[-1] >= 0:
    #for i in range(10000):
        sup = (1.5e-3) - (me[0]) / rho_eau  #
        inf = (1.5e-3) - (me[-1]) / rho_eau

    # calcul de la pression en fonction du temps
        Pt = P0 * (sup / inf) ** 1.4
    # temps que la masse d'eau est superieur à 0 et la
        if me[-1] <= 0 or Pt <= Pext:
            dm_dt = 0
            ve = 0
        else:
            ve = math.sqrt((2 * (Pt - Pext) / rho_eau))  # Vitesse d'éjection de l'eau, Bernouilli
            dm_dt = -Ae * math.sqrt(2 * rho_eau * (Pt - Pext))
        dme = f_m(t, me[-1], dm_dt)  # retourne le début massique de l'eau
        dx = f_x(t, x[-1], v[-1])  # retourne la vitesse [-1]
        if v[-1] >=0:
            # La vitesse est positive, le parachute n'est pas deployé
            dv = f_v_1(t, dm_dt, ve, mf, me[-1], g, v[-1])
        else:
            # la vitesse est négative, le parachute est déployé
            dv = f_v_2(t, dm_dt, ve, mf, me[-1], g, v[-1])

    # La masse d'eau suivante c'est celle d'avant + la dérivée * h
        me_next = me[-1] + dme * h
    # La vitesse suivante c'est la vitesse d'avant + la dérivée * h
        v_next = v[-1] + dv * h
    # La position suivante c'est la position d'avant + la dérivée * h
        x_next = x[-1] + dx * h

    # On rajoue la nouvelle valeur à la liste x ( la position de la fusée)
        x.append(x_next)
    # On rajoue la nouvelle valeur à la liste v ( la vitesse de la fusée
        v.append(v_next)
    # On rajoue la nouvelle valeur à la liste me ( la masse d'eau )
        me.append(me_next)


        if x_next < 0:  # si la position est inferieur à 0, on arrête le code
            break
    return x, v, me




def main():
    h_max = float((input("Entrer la hauteur max :")))  # On pose une hauteur max
    hauteur_max_absolue = []  # On créer une liste qui va determiner la hauteur max absolue finale

    ''' Boucle pour déterminer la masse d'eau en fonction de la hauteur qu'on choisis'''

    h_l, dm_t_l, ve_l, mf_l, g_l = h, dm_dt, ve, mf, g
    for i in range(1, 150):  # On prend chaque masse de 0,01 à 150
        x = [0]
        v = [0]
        me = [0.01 * i]
        resultat_x, resultat_v, resultat_m = euler(0, v, h, dm_dt, ve, mf, me, g)
        # On fait une liste avec toutes les hauteurs max pour trouver au final le max des hauteur max
        hauteur_max_absolue.append(max(resultat_x))
        if h_max - 0.3 < max(resultat_x) <= h_max + 0.3:
            print(max(resultat_x))

            print("Masse d'eau initiale pour atteindre " + str(h_max) + " m = " + str(me[0]) + " kg")

            hauteur_max = max(resultat_x)
            vitesse_max = max(resultat_v)

            temps = [i * h for i in range(len(resultat_x))]  # Créer la liste des temps

            # Figure avec 3 sous-graphes
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

            # Graphe 1 : Position x(t)
            ax1.plot(temps, resultat_x, 'b-', linewidth=2, label='Position x(t)')
            ax1.axhline(y=hauteur_max, color='r', linestyle='--', linewidth=1, alpha=0.7)
            ax1.set_xlabel('Temps (s)', fontsize=11)
            ax1.set_ylabel('Hauteur (m)', fontsize=11)
            ax1.set_title(f'Position en fonction du temps - Hauteur max : {hauteur_max:.2f} m', fontsize=12,
                          fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.legend(fontsize=10)
            ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)

            # Graphe 2 : Vitesse v(t)
            ax2.plot(temps, resultat_v, 'g-', linewidth=2, label='Vitesse v(t)')
            ax2.axhline(y=vitesse_max, color='r', linestyle='--', linewidth=1, alpha=0.7)
            ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
            ax2.set_xlabel('Temps (s)', fontsize=11)
            ax2.set_ylabel('Vitesse (m/s)', fontsize=11)
            ax2.set_title(f'Vitesse en fonction du temps - Vitesse max : {vitesse_max:.2f} m/s', fontsize=12,
                          fontweight='bold')
            ax2.grid(True, alpha=0.3)
            ax2.legend(fontsize=10)

            # Graphe 3 : Masse d'eau m(t)
            ax3.plot(temps, resultat_m, 'orange', linewidth=2, label="Masse d'eau m(t)")
            ax3.axhline(y=mf, color='red', linestyle='--', linewidth=1, alpha=0.7, label=f'Masse fusée sèche : {mf} kg')
            ax3.set_xlabel('Temps (s)', fontsize=11)
            ax3.set_ylabel('Masse (kg)', fontsize=11)
            ax3.set_title(f"Masse d'eau en fonction du temps", fontsize=12, fontweight='bold')
            ax3.grid(True, alpha=0.3)
            ax3.legend(fontsize=10)

            plt.tight_layout()
            plt.show()

    # la hauteur max absolue est la plus grande hauteur dans la liste des hauteurs max
    hauteur_max = max(hauteur_max_absolue)
    print("La hauteur absolue est ", hauteur_max)


if __name__ == "__main__":
    main()
    # resultat_x, resultat_v, resultat_m = euler(0, v, h, dm_dt, ve, mf, me, g)
    # print("Hauteur maximale atteinte :", max(resultat_x), "m")

