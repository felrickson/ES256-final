import numpy as np
import matplotlib.pyplot as plt
import control as ct
import os

# Create assets directory if it doesn't exist
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '../assets/images')
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

def define_system():
    """
    Define the State Space matrices based on Gabriel's PDF.
    Parameters:
    Km = 1.1 (Motor Gain)
    am = 13.2 (Mechanical Pole)
    ae = 950.0 (Electrical Pole)
    K_sys = 772 (System Constant)
    
    Transfer Function: G(s) = (Km * K_sys) / (s * (s + am) * (s + ae))
    """
    Km = 1.1
    am = 13.2
    ae = 950.0
    K_sys = 772
    
    # Coefficients for denominator: s^3 + a2*s^2 + a1*s + a0
    # den = s(s^2 + (am+ae)s + am*ae) = s^3 + (am+ae)s^2 + (am*ae)s
    a2 = am + ae       # 963.2
    a1 = am * ae       # 12540
    a0 = 0
    
    # Numerator coefficient
    b0 = Km * K_sys    # 849.2
    
    # State Space in Controllable Canonical Form (as per PDF)
    # x_dot = A x + B u
    # y = C x
    
    A = np.array([
        [0, 1, 0],
        [0, 0, 1],
        [-a0, -a1, -a2]
    ])
    
    B = np.array([[0], [0], [1]])
    
    C = np.array([[b0, 0, 0]])
    
    D = np.array([[0]])
    
    sys = ct.ss(A, B, C, D)
    return sys

def analyze_open_loop(sys):
    """
    Analyze open loop stability, poles, and zeros.
    """
    print("Polos do sistema:", ct.poles(sys))
    print("Zeros do sistema:", ct.zeros(sys))
    
    # Configure Dark Mode Style
    plt.rcParams.update({
        "figure.facecolor":  (0.0, 0.0, 0.0, 0.0),  # Transparent
        "axes.facecolor":    (0.0, 0.0, 0.0, 0.0),  # Transparent
        "savefig.facecolor": (0.0, 0.0, 0.0, 0.0),  # Transparent
        "axes.edgecolor":    "white",
        "axes.labelcolor":   "white",
        "xtick.color":       "white",
        "ytick.color":       "white",
        "text.color":        "white",
        "grid.color":        "white",
        "grid.alpha":        0.2,
        "legend.facecolor":  (0.0, 0.0, 0.0, 0.5),
        "legend.edgecolor":  "white"
    })

    # Plot 1: Pole-Zero Map (Dark)
    plt.figure(figsize=(6, 5))
    poles, zeros = ct.pzmap(sys, plot=False)
    plt.scatter(np.real(poles), np.imag(poles), marker='x', s=100, color='#f59e0b', label='Polos') # Orange
    plt.title('Mapa de Polos', color='white')
    plt.xlabel('Real')
    plt.ylabel('Imaginário')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'pzmap_dark.png'))
    plt.close()

    # Plot 2: Step Response (Dark)
    plt.figure(figsize=(8, 5))
    t, y = ct.step_response(sys)
    plt.plot(t, y, linewidth=2, color='#3b82f6') # Blue
    plt.title('Resposta ao Degrau (Malha Aberta)', color='white')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'step_openloop_dark.png'))
    plt.close()

if __name__ == "__main__":
    print("Iniciando modelagem do sistema...")
    sys = define_system()
    analyze_open_loop(sys)
    print("Gráficos gerados em assets/images/")
