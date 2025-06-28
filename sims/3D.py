import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Detector:
    def __init__(self):
        self.energy_min = 0.05  # MeV (50 keV)
        self.energy_max = 100   # MeV

    def detect(self, energy):
        """Check if energy is within detectable range."""
        return (energy >= self.energy_min) & (energy <= self.energy_max)

def cosmic_ray_flux(energy, altitude):
    """Improved flux model with:
       - Power-law spectrum
       - Atmospheric attenuation (scale height)
       - Geomagnetic cutoff (simplified)
    """
    base_flux = 1.2e4 * energy**(-2.7)  # Base GCR flux
    attenuation = np.exp(-(altitude - 100) / 8.5)  # Atmospheric shielding
    geomag_factor = 1 / (1 + (0.5 / energy)**3)  # Approx. cutoff at 0.5 GeV
    return base_flux * attenuation * geomag_factor

# Generate data
energies = np.logspace(-1, 2, 100)  # 0.1 MeV to 100 MeV
altitudes = np.linspace(300, 600, 50)  # 300–600 km
E_grid, H_grid = np.meshgrid(energies, altitudes)
flux_grid = cosmic_ray_flux(E_grid, H_grid)

# Apply detector constraints
detector = Detector()
flux_grid[~detector.detect(E_grid)] = np.nan  # Mask undetectable particles

# Plot
fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(
    np.log10(E_grid), H_grid, np.log10(flux_grid),
    cmap='viridis', edgecolor='none', alpha=0.8
)

# Labels and formatting
ax.set_xlabel('log10(Energy [MeV])', fontsize=12)
ax.set_ylabel('Altitude [km]', fontsize=12)
ax.set_zlabel('log10(Flux [particles/cm²/s/MeV])', fontsize=12)
ax.set_title('Realistic Cosmic Ray Flux (3D)', fontsize=14)

# Colorbar
cbar = fig.colorbar(surf, pad=0.1)
cbar.set_label('log10(Flux)', fontsize=12)

# Adjust view angle
ax.view_init(elev=30, azim=45)

plt.tight_layout()
plt.savefig('realistic_flux_3d.png', dpi=300)
plt.show()