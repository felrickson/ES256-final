import numpy as np
import matplotlib.pyplot as plt
import control as ct
import os

# Create assets directory if it doesn't exist
if not os.path.exists('../assets/images'):
    os.makedirs('../assets/images')

def define_system():
    """
    Define the State Space matrices here based on the project PDF.
    """
    # TODO: Fill with actual values from PDF
    A = np.array([[0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1],
                  [-1, -2, -3, -4]]) # Example values
    
    B = np.array([[0], [0], [0], [1]])
    
    C = np.array([[1, 0, 0, 0]])
    
    D = np.array([[0]])
    
    sys = ct.ss(A, B, C, D)
    return sys

def analyze_open_loop(sys):
    """
    Analyze open loop stability, poles, and zeros.
    """
    print("Polos do sistema:", ct.poles(sys))
    print("Zeros do sistema:", ct.zeros(sys))
    
    # Plot PZ Map
    plt.figure()
    ct.pzmap(sys)
    plt.title('Mapa de Polos e Zeros (Malha Aberta)')
    plt.savefig('../assets/images/pzmap_openloop.png')
    plt.close()

if __name__ == "__main__":
    print("Iniciando modelagem do sistema...")
    sys = define_system()
    analyze_open_loop(sys)
    print("Gráficos gerados em assets/images/")
