import matplotlib.pyplot as plt
import math

print("hello")

h =0.0001    # Pas de temps pour l'intégration
v = [0]      # Liste des valeurs de y (commence avec y0)
x =[0]
g = 9.81     # Accélération due à la gravité (m/s²)     # Masse initiale de la fusée (kg)

# Pressions

Pajouté = 150000 # Pression ajoutée en Pa
Pext = 101325      # masse volumique de l'eau kg/m3
P0 = Pext + Pajouté
Ae = 0.00005       # surface de la bouche d'éjection m2
pt = 0
dm_dt = 0    
ve = 0
Cd  =  0.9
rho_eau = 1000
rho_air = 1.225
Afr = (5.81e-3)  # Surface de la sortie fusée (m²)

mf = 0.25      # masse fusée
me = [0.6]       # masse eau
#m = mf + me   # masse totale initiale

# Pression dans la bouteille d'eau


def f_x(t, x, v):

    return v            # dérivée de la position est la vitesse

def f_m(t,m,dm_dt):     # la masse en fonction du temps

    return dm_dt        # le débit massique de l'eau dm_dt

def f_v(t, dm_dt, ve, mf, me, g,v_courant):

    thrust = -dm_dt * ve 
    #Fp = 2*Pt -Pext * Ae  # Poussée (positive)
    Fd = 0.5 * Cd * rho_air * (v_courant ** 2) * Afr
    return ((thrust -(Fd) - (mf + me) * g)) / (mf + me)   # dérivée de la vitesse (accélération)




def euler(t, v, h, dm_dt, ve, mf, me, g,):

    v = [0]
    x = [0]


    for i in range(100000):


        

        Pt = P0*(((1.5*10**-3)-(me[0]*10**-3)/rho_eau)/((1.5*10**-3)-(me[-1]*10**-3)/rho_eau))**1.4 # La pression qui diminue en fonction du temps

        ve = math.sqrt(2*(Pt-Pext)/rho_eau)      #Vitesse d'éjection de l'eau
        
        dm_dt = -Ae*math.sqrt(2*rho_eau*(Pt-Pext))


        #if m[-1] <= mf:
        if me[-1] <= 0:
            dm_dt = 0
            ve = 0

        dme = f_m(t, me[-1], dm_dt)
        dx = f_x(t, x[-1], v[-1])
        dv = f_v(t, dm_dt, ve, mf, me[-1], g, v[-1])

        me_next = me[-1] + dme*h
        v_next = v[-1] + dv*h
        x_next = x[-1] + dx*h

        #if x_next >= 0:
        x.append(x_next)
        v.append(v_next)
        me.append(me_next)
            
        if x_next < 0:
            break

            
        #if h_max-1 < x_next <= h_max +1 :

            #print(me[0])
    t = t + h
    return  x,v,me

for i in range(1,151):
    x = [0]
    v = [0]
    me = [0.01*i]
    h_max = 15

    resultat_x, resultat_v, resultat_m = euler(0, v, h, dm_dt, ve, mf, me, g)


    if h_max - 0.1< max(resultat_x) <= h_max + 0.1:
        print(max(resultat_x))
        print("Masse d'eau initiale pour atteindre {} m : {:.2f} kg".format(h_max, me[0]))

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
        ax1.set_title(f'Position en fonction du temps - Hauteur max : {hauteur_max:.2f} m', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=10)
        ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)

        # Graphe 2 : Vitesse v(t)
        ax2.plot(temps, resultat_v, 'g-', linewidth=2, label='Vitesse v(t)')
        ax2.axhline(y=vitesse_max, color='r', linestyle='--', linewidth=1, alpha=0.7)
        ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax2.set_xlabel('Temps (s)', fontsize=11)
        ax2.set_ylabel('Vitesse (m/s)', fontsize=11)
        ax2.set_title(f'Vitesse en fonction du temps - Vitesse max : {vitesse_max:.2f} m/s', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=10)

        # Graphe 3 : Masse m(t)
        ax3.plot(temps, resultat_m, 'orange', linewidth=2, label='Masse m(t)')
        ax3.axhline(y=mf, color='red', linestyle='--', linewidth=1, alpha=0.7, label=f'Masse fusée sèche : {mf} kg')
        ax3.set_xlabel('Temps (s)', fontsize=11)
        ax3.set_ylabel('Masse (kg)', fontsize=11)
        ax3.set_title(f'Masse en fonction du temps', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.legend(fontsize=10)

        plt.tight_layout()
        plt.show()
