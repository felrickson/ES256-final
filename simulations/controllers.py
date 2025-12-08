import numpy as np
import matplotlib.pyplot as plt
import control as ct
from model import define_system
import os

# Configure Dark Mode (Global for this script)
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
    "legend.edgecolor":  "white"
})

# Create assets directory if it doesn't exist
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, '../assets/images')
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

def design_p_controller(sys, Kp):
    """
    Design and simulate a Proportional Controller.
    """
    # Root Locus
    plt.figure(figsize=(10, 6))
    ct.rlocus(sys, plot=True, grid=True)
    plt.title(f'Lugar das Raízes (Kp={Kp})')
    # Use explicit path
    plt.savefig(os.path.join(assets_dir, 'felipe_rlocus.png'))
    plt.close()
    
    # Step Response
    sys_cl = ct.feedback(Kp * sys, 1)
    t, y = ct.step_response(sys_cl)
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, y, linewidth=2, color='#3b82f6') # Blue
    plt.title(f'Resposta ao Degrau (P, Kp={Kp})')
    plt.grid(True)
    plt.savefig(os.path.join(assets_dir, 'step_response_P.png'))
    plt.close()

def design_pid_controller(sys, Kp, Ki, Kd):
    """
    Design and simulate a PID Controller.
    """
    # PID with filtered derivative: Kp + Ki/s + Kd*s/(tau*s + 1)
    # Using tau = 0.01 (pole at -100)
    tau = 0.01
    pid_tf = Kp + ct.tf([Ki], [1, 0]) + ct.tf([Kd, 0], [tau, 1])
    
    sys_cl = ct.feedback(pid_tf * sys, 1)
    
    t, y = ct.step_response(sys_cl)
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, y, linewidth=2, color='#ef4444') # Red
    plt.title(f'Resposta ao Degrau (PID, Kp={Kp}, Ki={Ki}, Kd={Kd})')
    plt.grid(True)
    plt.savefig(os.path.join(assets_dir, 'step_response_PID.png'))
    plt.close()

def design_lead_controller(sys):
    """
    Design and simulate a Lead Compensator (Placeholder).
    """
    # Example Lead Compensator: Gc(s) = K * (s + z) / (s + p) where p > z
    # Placeholder values
    z = 1
    p = 10
    K = 10
    
    ctrl = K * ct.tf([1, z], [1, p])
    sys_cl = ct.feedback(ctrl * sys, 1)
    
    t, y = ct.step_response(sys_cl)
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, y, linewidth=2, color='#f59e0b') # Orange
    plt.title('Resposta ao Degrau (Compensador Lead)')
    plt.grid(True)
    plt.savefig(os.path.join(assets_dir, 'step_response_Lead.png'))
    plt.close()
    
    # Root Locus (Placeholder for one of the plots)
    plt.figure(figsize=(10, 6))
    ct.rlocus(sys, plot=True, grid=True)
    plt.title('Lugar das Raízes (Compensador Lead)')
    plt.savefig(os.path.join(assets_dir, 'root_locus_Lead.png'))
    plt.close()

def design_lag_controller(sys, Kp, z, p):
    """
    Design and simulate a Proportional-Lag Compensator.
    C(s) = Kp * (s + z) / (s + p)
    Target: Increase DC gain by factor z/p while maintaining P-controller transient provided by Kp.
    """
    # Lag Compensator Transfer Function
    lag_tf = ct.tf([1, z], [1, p])
    ctrl = Kp * lag_tf
    
    sys_cl = ct.feedback(ctrl * sys, 1)
    
    t, y = ct.step_response(sys_cl)
    
    # Calculate metrics for title
    y_final = y[-1]
    y_peak = np.max(y)
    Mp = (y_peak - y_final) / y_final * 100 if y_final != 0 else 0
    
    # Find ts
    error = np.abs(y - y_final)
    threshold = 0.02 * np.abs(y_final)
    out_of_bounds = np.where(error > threshold)[0]
    ts = t[out_of_bounds[-1]] if len(out_of_bounds) > 0 else 0
    
    print(f"Lag Design Results -> Mp: {Mp:.2f}%, ts: {ts:.4f}s")

    plt.figure(figsize=(10, 6))
    plt.plot(t, y, linewidth=2, color='#10b981') # Green
    plt.title(f'Resposta ao Degrau (P+Lag)\nKp={Kp}, z={z}, p={p} (Dominant Gain x{z/p:.1f})')
    plt.grid(True)
    plt.text(0.6 * np.max(t), 0.5 * np.max(y), f'Mp = {Mp:.1f}%\nts = {ts:.2f}s', 
             bbox=dict(facecolor='black', alpha=0.5, edgecolor='white'), color='white')
    plt.savefig(os.path.join(assets_dir, 'step_response_Lag.png'))
    plt.close()
    
    return sys_cl

if __name__ == "__main__":
    sys = define_system()
    
    # 1. Proportional Controller Design
    # Found optimal Kp approx 138 for Mp ~ 10% and ts ~ 0.53s
    best_Kp = 138
    print(f"Executing P Controller with Kp={best_Kp}")
    design_p_controller(sys, Kp=best_Kp)
    
    # 2. PID Controller (Optional, keeping previous values or adjusting)
    # design_pid_controller(sys, Kp=10, Ki=5, Kd=2) # Leaving as is or commenting out if not requested
    
    # 3. Lag Compensator Design
    # Requirement: Increase DC gain by 10x to reduce steady state error.
    # Dierson's optimization found: K=151.4, a=0.01, b=0.1
    # This meets all specs including ramp error <= 1%.
    z_lag = 0.1
    p_lag = 0.01
    K_lag = 151.429
    print(f"Executing P+Lag Controller with K={K_lag}, z={z_lag}, p={p_lag}")
    design_lag_controller(sys, Kp=K_lag, z=z_lag, p=p_lag)
    
    print("Simulações de controle concluídas. Gráficos em assets/images/")
