import numpy as np
import matplotlib.pyplot as plt
from main import *

energies = np.logspace(-2, 3, 200)  # 0.01 MeV to 1 GeV
altitudes = np.linspace(3, 300, 10)  # 300–600 km

plt.figure(figsize=(12, 7))
for alt in altitudes:
    flux = cosmic_ray.flux(energies, alt)
    detectable = detector.detect(energies)
    plt.loglog(energies[detectable], flux[detectable], label=f"{alt:.0f} km")

plt.xlabel("Energy [MeV]"); plt.ylabel("Flux [particles/cm²/s/MeV]")
plt.title("Realistic Cosmic Ray Flux (Protons) with Detector Thresholds")
plt.legend(); plt.grid()
plt.savefig('../figs/01a_flux_vs_altitude.png')
plt.show()