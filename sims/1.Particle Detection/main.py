import numpy as np
import matplotlib.pyplot as plt

class Detector:
    def __init__(self, material="EJ-200", area=1.5, height=1.5):
        self.material = material
        self.area = area  # cm² (cross-section)
        self.height = height  # cm (scintillator thickness)
        self.density = 1.023  # g/cm³ (EJ-200)
        self.photon_yield = 1e4  # photons/MeV (EJ-200)
        
    def energy_deposition(self, energy, particle="proton"):
        """Realistic Bethe-Bloch approximation."""
        if particle == "proton":
            return 1.5 + 0.05 * np.log(energy)  # MeV/cm
        elif particle == "alpha":
            return 6.0 + 0.2 * np.log(energy)
        
    def detect(self, energy, particle="proton"):
        """Apply detector thresholds (50 keV–100 MeV)."""
        return (energy >= 0.05) & (energy <= 100)

def cosmic_ray_flux(energy, altitude, particle="proton"):
    """Improved flux model with:
       - Solar modulation
       - Atmospheric attenuation (scale height)
       - Geomagnetic cutoff (simplified)
    """
    base_flux = 1.2e4 * energy**(-2.7 + 0.2)  # Solar max adjustment
    
    # Atmospheric attenuation (scale height ~8.5 km)
    scale_height = 8.5  # km
    attenuation = np.exp(-(altitude - 100) / scale_height)
    
    # Geomagnetic cutoff (placeholder)
    cutoff_energy = 0.5  # GeV for 50° inclination
    geomag_factor = 1 / (1 + (cutoff_energy / energy)**3)
    
    if particle == "alpha":
        return 0.1 * base_flux * attenuation * geomag_factor
    return base_flux * attenuation * geomag_factor

# Example usage
detector = Detector()
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