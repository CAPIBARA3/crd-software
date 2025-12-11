import numpy as np
import matplotlib.pyplot as plt
from main import *

# Generate data
energies = np.logspace(-1, 2, 100)  # 0.1–100 MeV
altitude = 500  # Fixed altitude

plt.figure(figsize=(10, 6))
for particle, color in [("proton", "blue"), ("alpha", "red")]:
    flux = cosmic_ray_flux(energies, altitude, particle)
    plt.loglog(energies, flux, color, label=particle.capitalize(), linewidth=2)

plt.xlabel("Energy [MeV]", fontsize=12)
plt.ylabel("Flux [particles/cm²/s/MeV]", fontsize=12)
plt.title("Proton vs. Alpha Particle Flux at 500 km", fontsize=14)
plt.grid(True, which="both", linestyle="--")
plt.legend(fontsize=12)
plt.savefig("03_proton_vs_alpha.png", dpi=300)
plt.show()