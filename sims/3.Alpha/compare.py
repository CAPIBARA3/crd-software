import numpy as np
import matplotlib.pyplot as plt

def cosmic_ray_flux(energy, altitude, particle="proton"):
    """Flux model for protons/alphas."""
    base_flux = 1.2e4 * energy**(-2.7) * np.exp(-(altitude - 100)/8.5)
    geomag_factor = 1 / (1 + (0.5 / energy)**3)
    
    if particle == "alpha":
        return 0.1 * base_flux * geomag_factor  # Alphas = 10% of protons
    return base_flux * geomag_factor

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
plt.savefig("proton_vs_alpha.png", dpi=300)
plt.show()