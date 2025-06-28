import numpy as np
import matplotlib.pyplot as plt

class Detector:
    def __init__(self):
        self.energy_min = 0.05  # MeV (50 keV)
        self.energy_max = 100    # MeV
        self.area = 2.25         # cm² (1.5 cm × 1.5 cm)

    def detect(self, energy):
        """Mask energies outside the detector's range."""
        return (energy >= self.energy_min) & (energy <= self.energy_max)

def cosmic_ray_flux(energy, altitude, particle="proton"):
    """
    Flux model for protons/alphas. Flux inscreases logarithmically with altitude.
    """
    base_flux = 1.2e4 * energy ** (-2.7)
    scale_height = 0.5 # km (Earth's atmosphere)
    attenuation = np.exp(-(altitude - 100) / scale_height)
    geomag_factor = 1 / (1 + (0.5 / energy) ** 3)
    prop = {'proton':1.0,'alpha':0.1} # distribution of protons and alphas
    return prop * base_flux * attenuation * geomag_factor

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
plt.savefig("log_counts_vs_altitude.png", dpi=300)
plt.show()