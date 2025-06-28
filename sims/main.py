import numpy as np
import matplotlib.pyplot as plt

class Detector:
    def __init__(self, material="EJ-200", side=1.5, height=1.5):
        self.material = material
        self.area = side**2  # cm² (cross-section)
        self.height = height  # cm (scintillator thickness)
        self.density = 1.023  # g/cm³ (EJ-200)
        self.photon_yield = 1e4  # photons/MeV (EJ-200)
        self.energy_min = 0.05  # MeV (50 keV)
        self.energy_max = 100  # MeV
        
    def energy_deposition(self, energy, particle="proton"):
        """Realistic Bethe-Bloch approximation."""
        if particle == "proton":
            return 1.5 + 0.05 * np.log(energy)  # MeV/cm
        elif particle == "alpha":
            return 6.0 + 0.2 * np.log(energy)

    def detect(self, energy):
        """Mask energies outside the detector's range."""
        return (energy >= self.energy_min) & (energy <= self.energy_max)

def cosmic_ray_flux(energy, altitude, particle="proton"):
    """
    Flux model for protons/alphas. Flux inscreases logarithmically with altitude.
    Improved flux model with:
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
    geomag_factor = 1 / (1 + (cutoff_energy / energy) ** 3)

    prop = {'proton':1.0,'alpha':0.1} # distribution of protons and alphas
    return prop[particle] * base_flux * attenuation * geomag_factor

detector = Detector()