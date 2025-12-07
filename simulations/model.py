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
    
    # Combined Plot (User Request)
    plt.figure(figsize=(12, 5))

    # Plot 1: Mapa de Polos e Zeros
    plt.subplot(1, 2, 1)
    poles, zeros = ct.pzmap(sys, plot=False)
    plt.scatter(np.real(poles), np.imag(poles), marker='x', s=100, color='r', label='Polos')
    plt.title(f'Mapa de Polos\n(Dominante em {poles[1]:.1f})')
    plt.xlabel('Real')
    plt.ylabel('Imaginário')
    plt.grid(True)
    plt.legend()

    # Plot 2: Resposta ao Degrau
    plt.subplot(1, 2, 2)
    t, y = ct.step_response(sys)
    plt.plot(t, y, linewidth=2)
    plt.title('Resposta ao Degrau (Malha Aberta)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'validation_combined.png'))
    plt.close()

if __name__ == "__main__":
    print("Iniciando modelagem do sistema...")
    sys = define_system()
    analyze_open_loop(sys)
    print("Gráficos gerados em assets/images/")
