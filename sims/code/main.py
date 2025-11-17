import numpy as np

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


class cosmic_ray:
    def __init__(self):
        self.H = 7.5  # scale height in km
        self.X0 = 1030.0  # column depth at sea level (g/cm^2)
        self.Lambda = {
            'proton': 140.0,  # proton attenuation length (g/cm^2)
            'alpha': 80.0  # alpha attenuation length (g/cm^2)
        }
        self.prop = {'proton': 1.0, 'alpha': 0.1}  # distribution of protons and alphas

    def atmospheric_attenuation(self, altitude, particle="proton"):
        """Calculate atmospheric attenuation factor exp(-X(h)/Lambda)."""

        # --- Atmospheric column depth X(h) (g/cm^2) ---
        X_h = self.X0 * np.exp(- altitude / self.H)

        # --- Attenuation factor: exp(-X(h)/Lambda) ---
        attenuation = np.exp(- X_h / self.Lambda[particle])

        return attenuation

    def flux(self, energy, altitude, particle="proton"):
        """
            Simple Flux model for protons/alpha. Increases logarithmically with altitude using an atmosphere depth model.
            energy: MeV
            altitude: km above sea level
            particle: "proton" or "alpha"
            Returns flux in particles/cm²/s/MeV
            """

        # --- Base (top-of-atmosphere) energy spectrum ---
        base_flux = 1.2e4 * energy ** (-2.7 + 0.2)  # top-of-atmosphere flux proxy

        # --- Geomagnetic cutoff (simple placeholder, keep yours or refine) ---
        cutoff_energy = 0.5  # GeV, example
        geomag_factor = 1.0 / (1.0 + (cutoff_energy / energy) ** 3)

        # Final flux
        flux = self.prop[particle] * base_flux * self.atmospheric_attenuation(altitude, particle=particle) * geomag_factor
        return flux

detector = Detector()
cosmic_ray = cosmic_ray()