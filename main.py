"""
Programme de résolution d'équations différentielles par la méthode d'Euler.
Résout l'équation différentielle : dy/dt = f(t, y)
"""

# Paramètres initiaux
import matplotlib.pyplot as plt
import math

h =0.0001    # Pas de temps pour l'intégration
v = [0]      # Liste des valeurs de y (commence avec y0)
x =[0]
g = 9.81     # Accélération due à la gravité (m/s²)     # Masse initiale de la fusée (kg)

# Pressions
Peau = 1000 # masse volumique de l'eau kg/m3
Pint = 400000
Pext = 101325
Ae = 0.00005 # surface de la bouche d'éjection m2
ve = math.sqrt(2*(Pint-Pext)/Peau) #Vitesse d'éjection de l'eau
dm_dt = -Peau*Ae*ve

mf = 0.3 # masse fusée
me = 0.4 # masse eau
m = [mf + me] # masse totale initiale



def f_x(t, x, v):

    return v  # dérivée de la position est la vitesse

def f_m(t,m,dm_dt): # la masse en fonction du temps

    return dm_dt  # le débit massique de l'eau dm_dt

def f_v(t, dm_dt, ve, m, g):

    thrust = -dm_dt * ve  # Poussée (positive)
    return (thrust - m * g) / m
    
def euler(t, v, h, dm_dt, ve, m, g):
        
    for i in range(100000):

        if m[-1] <= mf:
            dm_dt = 0
            ve = 0
       
            

        dm = f_m(t, m[-1], dm_dt)
        dx = f_x(t, x[-1], v[-1])
        dv = f_v(t, dm_dt, ve, m[-1], g)

        m_next = m[-1] + dm*h
        v_next = v[-1] + dv*h
        x_next = x[-1] + dx*h

        if x_next >= 0:
            x.append(x_next)
            v.append(v_next)
            m.append(m_next)

        t += h

    return  x,v,m

# Exécution de la méthode d'Euler
resultat_x, resultat_v, resultat_m = euler(0, v, h, dm_dt, ve, m, g)
#resultat_x, resultat_v, resultat_m = euler(0, dm_dt, ve, g)
print(resultat_x)
# Affichage des résultats
hauteur_max = max(resultat_x)
vitesse_max = max(resultat_v)

print(f"\n🚀 FUSÉE À EAU - RÉSULTATS")
print(f"=" * 50)
print(f"✓ Hauteur maximale : {hauteur_max:.2f} m")
print(f"✓ Vitesse maximale : {vitesse_max:.2f} m/s")
print(f"✓ Masse finale : {resultat_m[-1]:.3f} kg")
print(f"=" * 50 + "\n")

# Tracer les graphes
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