import numpy as np
import matplotlib.pyplot as plt
import control as ct
import os

def get_assets_dir(mode='dark'):
    """
    Returns the target directory based on the mode.
    mode='dark' -> ../assets/images (HTML)
    mode='light' -> ../assets/report_images (PDF Report)
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if mode == 'light':
        target = os.path.join(script_dir, '../assets/report_images')
    else:
        target = os.path.join(script_dir, '../assets/images')
    
    if not os.path.exists(target):
        os.makedirs(target)
    return target

def configure_plot_style(mode='dark'):
    """
    Configures matplotlib params for Dark (HTML) or Light (PDF) mode.
    """
    if mode == 'dark':
        # Dark Mode (Transparent background, white lines)
        plt.rcParams.update({
            "figure.facecolor":  (0.0, 0.0, 0.0, 0.0),
            "axes.facecolor":    (0.0, 0.0, 0.0, 0.0),
            "savefig.facecolor": (0.0, 0.0, 0.0, 0.0),
            "axes.edgecolor":    "white",
            "axes.labelcolor":   "white",
            "xtick.color":       "white",
            "ytick.color":       "white",
            "text.color":        "white",
            "grid.color":        "white",
            "grid.alpha":        0.2,
            "legend.facecolor":  (0.0, 0.0, 0.0, 0.5),
            "legend.edgecolor":  "white",
            "lines.color":       "white",
            "patch.edgecolor":   "white"
        })
        return ['#f59e0b', '#3b82f6', '#10b981', '#ef4444'] # Orange, Blue, Green, Red
    else:
        # Light Mode (White background, black/colored lines)
        plt.rcParams.update({
            "figure.facecolor":  "white",
            "axes.facecolor":    "white",
            "savefig.facecolor": "white",
            "axes.edgecolor":    "black",
            "axes.labelcolor":   "black",
            "xtick.color":       "black",
            "ytick.color":       "black",
            "text.color":        "black",
            "grid.color":        "black",
            "grid.alpha":        0.2,
            "legend.facecolor":  "white",
            "legend.edgecolor":  "black",
            "lines.color":       "black",
            "patch.edgecolor":   "black"
        })
        # Standard academic colors (Blue, Orange, Green, Red) - darker shades for white paper
        return ['#d35400', '#2980b9', '#27ae60', '#c0392b'] 

def define_system():
    """
    Define the State Space matrices based on Gabriel's PDF.
    Parameters:
    Km = 1.2 (Motor Gain - Dierson's value)
    am = 13.2 (Mechanical Pole)
    ae = 950.0 (Electrical Pole)
    K_sys = 1.0 (Removed intrinsic gain 772)
    
    Transfer Function: G(s) = Km / (s * (s + am) * (s + ae))
    """
    Km = 1.2
    am = 13.2
    ae = 950.0
    # K_sys removed (or set to 1) per Dierson's model
    
    # Coefficients for denominator: s^3 + a2*s^2 + a1*s + a0
    # den = s(s^2 + (am+ae)s + am*ae) = s^3 + (am+ae)s^2 + (am*ae)s
    a2 = am + ae       # 963.2
    a1 = am * ae       # 12540
    a0 = 0
    
    # Numerator coefficient
    b0 = Km            # 1.2
    
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

def analyze_open_loop(sys, mode='dark'):
    """
    Analyze open loop stability, poles, and zeros.
    """
    print(f"[{mode.upper()}] Gerando gráficos de malha aberta...")
    colors = configure_plot_style(mode)
    assets_dir = get_assets_dir(mode)
    
    print("Polos do sistema:", ct.poles(sys))
    print("Zeros do sistema:", ct.zeros(sys))
    
    # Plot 1: PZ Map
    # Plot 1: PZ Map (Manual Plot for High Visibility)
    plt.figure(figsize=(8, 6))
    poles = ct.poles(sys)
    zeros = ct.zeros(sys)
    
    # Grid
    grid_color = 'white' if mode == 'dark' else 'black'
    grid_alpha = 0.3
    plt.grid(True, which='both', linestyle='--', color=grid_color, alpha=grid_alpha)
    plt.axhline(0, color=grid_color, linewidth=1, alpha=0.5)
    plt.axvline(0, color=grid_color, linewidth=1, alpha=0.5)

    # Markers
    if mode == 'dark':
        pole_color = '#00ffff' # Cyan
        zero_color = '#ffff00' # Yellow
    else:
        pole_color = 'blue'
        zero_color = 'red'

    plt.scatter(np.real(poles), np.imag(poles), marker='x', s=150, linewidth=3, color=pole_color, label='Polos')
    if len(zeros) > 0:
        plt.scatter(np.real(zeros), np.imag(zeros), marker='o', s=150, linewidth=3, edgecolor=zero_color, facecolor='none', label='Zeros')

    # Annotate Poles
    for p in poles:
        plt.annotate(f"{p.real:.1f}", (np.real(p), np.imag(p)), 
                     textcoords="offset points", xytext=(10,10), ha='center', 
                     color=grid_color, fontsize=10)

    plt.title('Mapa de Polos e Zeros (Malha Aberta)', color='white' if mode=='dark' else 'black')
    plt.xlabel('Eixo Real')
    plt.ylabel('Eixo Imaginário')
    plt.legend()
    
    # Save
    plt.savefig(os.path.join(assets_dir, f'01_pzmap_{mode}.png'))
    plt.close()
    
    # Plot 2: Open Loop Step
    plt.figure(figsize=(10, 6))
    t, y = ct.step_response(sys)
    plt.plot(t, y, linewidth=2, color='#f59e0b' if mode=='dark' else '#d35400')
    plt.title('Resposta ao Degrau em Malha Aberta', color='white' if mode=='dark' else 'black')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both', color='white' if mode=='dark' else 'black', alpha=0.3)
    
    plt.savefig(os.path.join(assets_dir, f'02_step_openloop_{mode}.png'))
    plt.close()

if __name__ == "__main__":
    sys = define_system()
    # Run for both modes to ensure assets are generated
    for mode in ['dark', 'light']:
        analyze_open_loop(sys, mode=mode)
    print("Gráficos de malha aberta gerados.")
