import numpy as np
import matplotlib.pyplot as plt
from main import *

# Example usage

energies = np.logspace(-2, 3, 200)  # 0.01 MeV to 1 TeV
altitudes = np.linspace(300, 600, 5)  # 300–600 km

plt.figure(figsize=(12, 7))
for alt in altitudes:
    flux = cosmic_ray_flux(energies, alt)
    detectable = detector.detect(energies)
    plt.loglog(energies[detectable], flux[detectable], label=f"{alt:.0f} km")

plt.xlabel("Energy [MeV]"); plt.ylabel("Flux [particles/cm²/s/MeV]")
plt.title("Realistic Cosmic Ray Flux (Protons) with Detector Thresholds")
plt.legend(); plt.grid(); plt.show()
plt.savefig('01_flux_vs_altitude.png')