import numpy as np
import matplotlib.pyplot as plt
from main import *

def calculate_counts(flux, energy_bins, detector_area):
    """Integrate flux over energy bins (counts/cm²/s)."""
    return np.trapz(flux, energy_bins) * detector_area

# Generate energy/altitude grid
energies = np.logspace(-1, 2, 100)  # 0.1–100 MeV
altitudes = np.linspace(300, 600, 5)  # 300–600 km
detector = Detector()

# Calculate counts/sec at each altitude (logarithmic scale)
counts = []
for alt in altitudes:
    flux = cosmic_ray_flux(energies, alt)
    detectable = detector.detect(energies)
    counts.append(calculate_counts(flux[detectable], energies[detectable], detector.area))

# Plot (logarithmic y-axis)
plt.figure(figsize=(10, 5))
plt.semilogy(altitudes, counts, 'bo-', markersize=8, linewidth=2)  # Log y-axis
plt.xlabel("Altitude [km]", fontsize=12)
plt.ylabel("Detected Counts per Second (log scale)", fontsize=12)
plt.title("CAPIBARA Count Rate vs. Altitude (Logarithmic Scale)", fontsize=14)
plt.grid(True, which="both", linestyle='--')  # Grid for log scale
plt.savefig("../figs/02_log_counts_vs_altitude.png", dpi=300)
plt.show()