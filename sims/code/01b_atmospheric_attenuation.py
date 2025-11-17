import numpy as np
import matplotlib.pyplot as plt
from main import *

# Energies to check
energies = [10, 100, 1000]  # MeV, example energies
labels = [f"{E} MeV" for E in energies]

# Altitude range: sea level to 600 km
altitudes = np.linspace(0, 600, 200)  # km

plt.figure(figsize=(10, 7))

attenuation = cosmic_ray.atmospheric_attenuation(altitudes)
plt.semilogy(altitudes, attenuation, label='atmospheric attenuation', linewidth=2)

plt.xlabel("Altitude [km]")
plt.ylabel("Atmospheric Attenuation (exp(-X/Λ))")
plt.title("Atmospheric Attenuation vs Altitude for Protons")
plt.grid(True, which="both")
plt.legend()
plt.ylim(1e-3, 1.2)  # show sea level to top-of-atmosphere clearly
plt.savefig("../figs/01b_atmospheric_attenuation.png")
plt.show()