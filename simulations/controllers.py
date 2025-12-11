import numpy as np
import matplotlib.pyplot as plt
import control as ct
from model import define_system, configure_plot_style, get_assets_dir, analyze_open_loop
import os

def generate_comparative_plots(sys_input, Kp_p, ctrl_lag_input, mode='dark'):
    """
    Generates detailed comparative plots based on Dierson Silva's specifications.
    Parameters from request:
    km = 1.2, am = 13.2, ae = 950
    kcp = 77000
    aLag = 0.01, bLag = 0.1
    """
    colors = configure_plot_style(mode)
    assets_dir = get_assets_dir(mode)
    grid_color = 'black' if mode == 'light' else 'white'
    grid_alpha = 0.3
    
    # --- Redefining System exactly as requested for Comparison ---
    s = ct.TransferFunction.s
    km = 1.2
    am = 13.2
    ae = 950
    
    # Plant G(s)
    Gs = km/(s*(s+am)*(s+ae))
    
    # Compensator Parameters
    kcp = 77000
    aLag = 0.01
    bLag = 10.0 * aLag # bLag = 0.1
    
    # Lag Compensator C(s) without Gain (Gain is applied in loop)
    # The snippet implies Lkc = kcp * CLag * Gs, where CLag is just the pole/zero
    CLag = (s + bLag)/(s + aLag)

    # --- Loop Definitions (Dierson's Logic) ---
    # Lk = kcp * Gs
    # Lkc = kcp * CLag * Gs
    # Gf = feedback(Gs, 1)      -> Uncompensated
    # Gkf = feedback(Lk, 1)     -> Proportional
    # Gkcf = feedback(Lkc, 1)   -> P + Lag
    
    Lk = kcp * Gs
    Lkc = kcp * CLag * Gs
    
    Gf = ct.feedback(Gs, 1)
    Gkf = ct.feedback(Lk, 1)
    Gkcf = ct.feedback(Lkc, 1)

    # --- Resposta ao Degrau (Snippet implementation) ---
    plt.figure(figsize=(10, 6))
    t1 = np.linspace(0, 3, 1000)
    
    t1, y1 = ct.step_response(Gf, T=t1)
    t1, y2 = ct.step_response(Gkf, T=t1)
    t1, y3 = ct.step_response(Gkcf, T=t1)
    
    plt.plot(t1, y1, linewidth=2, label='G(s)', color=colors[1])
    plt.plot(t1, y2, linewidth=2, label='k*G(s)', color=colors[0])
    plt.plot(t1, y3, linewidth=2, label='k*G(s)*C(s)', color=colors[2])
    
    plt.title('Resposta ao degrau do sistema em malha fechada', color='white' if mode=='dark' else 'black')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.savefig(os.path.join(assets_dir, '07_compare_step.png'))
    plt.close()

    # --- Resposta à Rampa (Snippet implementation) ---
    plt.figure(figsize=(10, 6))
    t = np.linspace(0, 3, 1000)
    rampa = t  # r(t) = t
    
    t_out, y1_r = ct.forced_response(Gf, T=t, U=rampa)
    t_out, y2_r = ct.forced_response(Gkf, T=t, U=rampa)
    t_out, y3_r = ct.forced_response(Gkcf, T=t, U=rampa)
    
    plt.plot(t_out, y1_r, linewidth=2, label="Saída G(s)", color=colors[1])
    plt.plot(t_out, y2_r, linewidth=2, label="Saída k*G(s)", color=colors[0])
    plt.plot(t_out, y3_r, linewidth=2, label="Saída k*G(s)*C(s)", color=colors[2])
    plt.plot(t_out, rampa, '--', linewidth=2, label="Entrada rampa", color=colors[3])
    
    plt.title("Resposta à Rampa do sistema em malha fechada", color='white' if mode=='dark' else 'black')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.legend()
    plt.savefig(os.path.join(assets_dir, '08_compare_ramp.png'))
    plt.close()
    
    # --- Bode (Standardized) ---
    # Recalculating Bode for consistency with new parameters
    plt.figure(figsize=(10, 8))
    omega = np.logspace(-3, 3, 1000)
    
    # Open Loops
    sys_ol_uncomp = Gs
    sys_ol_p = Lk
    sys_ol_lag = Lkc
    
    mag_u, phase_u, _ = ct.frequency_response(sys_ol_uncomp, omega)
    mag_p, phase_p, _ = ct.frequency_response(sys_ol_p, omega)
    mag_l, phase_l, _ = ct.frequency_response(sys_ol_lag, omega)
    
    mag_u_db = 20 * np.log10(mag_u)
    mag_p_db = 20 * np.log10(mag_p)
    mag_l_db = 20 * np.log10(mag_l)
    
    phase_u_deg = np.degrees(np.unwrap(phase_u))
    phase_p_deg = np.degrees(np.unwrap(phase_p))
    phase_l_deg = np.degrees(np.unwrap(phase_l))
    
    ax1 = plt.subplot(2, 1, 1)
    plt.semilogx(omega, mag_u_db, linewidth=2, label='G(s)', color=colors[1])
    plt.semilogx(omega, mag_p_db, linewidth=2, label='k*G(s)', color=colors[0])
    plt.semilogx(omega, mag_l_db, linewidth=2, label='k*G(s)*C(s)', color=colors[2])
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.ylabel('Magnitude (dB)')
    plt.title('Diagrama de Bode Comparativo', color='white' if mode=='dark' else 'black')
    plt.legend()
    
    ax2 = plt.subplot(2, 1, 2)
    plt.semilogx(omega, phase_u_deg, linewidth=2, label='G(s)', color=colors[1])
    plt.semilogx(omega, phase_p_deg, linewidth=2, label='k*G(s)', color=colors[0])
    plt.semilogx(omega, phase_l_deg, linewidth=2, label='k*G(s)*C(s)', color=colors[2])
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.ylabel('Fase (graus)')
    plt.xlabel('Frequência (rad/s)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, '05_compare_bode.png'))
    plt.close()

def design_p_controller(sys, mode='dark'):
    """
    Design and simulate a Proportional Controller.
    Updated Kp to 77000 as per discussion.
    """
    Kp = 77000
    
    colors = configure_plot_style(mode)
    assets_dir = get_assets_dir(mode)
    grid_color = 'black' if mode == 'light' else 'white'
    grid_alpha = 0.3

    # Root Locus
    plt.figure(figsize=(10, 10))
    rlist, klist = ct.rlocus(sys, plot=True, grid=True)
    
    # Enhanced visibility for poles and zeros
    poles, zeros = ct.pzmap(sys, plot=False)
    plt.plot(np.real(poles), np.imag(poles), 'x', markersize=12, markeredgewidth=3, color='orange', label='Open Loop Poles')
    plt.plot(np.real(zeros), np.imag(zeros), 'o', markersize=12, markeredgewidth=3, markerfacecolor='none', color='orange', label='Open Loop Zeros')
    
    plt.title(f'Lugar das Raízes (Kp={Kp})', color='white' if mode=='dark' else 'black')
    plt.xlabel('Eixo Real')
    plt.ylabel('Eixo Imaginário')
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    # plt.xlim([-2, 2]) # Auto-scale requested
    plt.legend()
    plt.savefig(os.path.join(assets_dir, '03_rlocus_P.png'))
    plt.close()
    
    # Step Response
    sys_cl = ct.feedback(Kp * sys, 1)
    t = np.linspace(0, 1.5, 1000)
    t, y = ct.step_response(sys_cl, T=t)
    
    info = ct.step_info(sys_cl)
    Mp = info['Overshoot']
    ts = info['SettlingTime']
    
    print(f"[{mode.upper()}] P Result (Kp={Kp}): Mp={Mp:.3f}%, ts={ts:.4f}s")
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, y, linewidth=2, color=colors[1])
    plt.title(f'Resposta ao Degrau (P, Kp={Kp})', color='white' if mode=='dark' else 'black')
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    
    text_color = 'white' if mode=='dark' else 'black'
    bg_color = 'black' if mode=='dark' else 'white'
    plt.text(0.6 * np.max(t), 0.5 * np.max(y), f'Mp = {Mp:.2f}%\nts = {ts:.3f}s', 
             bbox=dict(facecolor=bg_color, alpha=0.5, edgecolor=text_color), color=text_color)
             
    plt.savefig(os.path.join(assets_dir, '04_step_response_P.png'))
    plt.close()
    return Kp

def design_lag_controller(sys, mode='dark'):
    """
    Design and simulate a Proportional-Lag Compensator.
    Updated Parameters: Kp=77000, z=0.1 (bLag), p=0.01 (aLag)
    """
    colors = configure_plot_style(mode)
    assets_dir = get_assets_dir(mode)
    grid_color = 'black' if mode == 'light' else 'white'
    grid_alpha = 0.3

    # Dierson Parameters
    Kp = 77000
    z = 0.1   # bLag
    p = 0.01  # aLag

    print(f"[{mode.upper()}] Lag Design (Dierson): Kp={Kp}, z={z}, p={p}")

    # Lag Compensator Transfer Function (without gain Kp, Kp applied to loop)
    lag_tf = ct.tf([1, z], [1, p])
    
    # Total Open Loop = Kp * Lag * Sys
    ctrl = Kp * lag_tf
    
    sys_cl = ct.feedback(ctrl * sys, 1)
    
    t = np.linspace(0, 3, 1000) # Increased to 3s per request
    t, y = ct.step_response(sys_cl, T=t)
    
    y_final = y[-1]
    y_peak = np.max(y)
    Mp = (y_peak - y_final) / y_final * 100 if y_final != 0 else 0
    
    error = np.abs(y - y_final)
    threshold = 0.02 * np.abs(y_final)
    out_of_bounds = np.where(error > threshold)[0]
    ts = t[out_of_bounds[-1]] if len(out_of_bounds) > 0 else 0
    
    print(f"[{mode.upper()}] Lag Design Results -> Mp: {Mp:.2f}%, ts: {ts:.4f}s")

    plt.figure(figsize=(10, 6))
    plt.plot(t, y, linewidth=2, color=colors[2])
    plt.title(f'Resposta ao Degrau (P+Lag)\nKp={Kp}, z={z}, p={p}', color='white' if mode=='dark' else 'black')
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    
    text_color = 'white' if mode=='dark' else 'black'
    bg_color = 'black' if mode=='dark' else 'white'
    
    plt.text(0.6 * np.max(t), 0.5 * np.max(y), f'Mp = {Mp:.1f}%\nts = {ts:.2f}s', 
             bbox=dict(facecolor=bg_color, alpha=0.5, edgecolor=text_color), color=text_color)
    plt.savefig(os.path.join(assets_dir, '06b_step_response_Lag.png'))
    plt.close()

    # Root Locus (Lag)
    plt.figure(figsize=(10, 10))
    # Standard RL of the Lag*Sys
    sys_open_lag = lag_tf * sys
    ct.rlocus(sys_open_lag, plot=True, grid=True)
    
    # Enhanced visibility
    poles, zeros = ct.pzmap(sys_open_lag, plot=False)
    plt.plot(np.real(poles), np.imag(poles), 'x', markersize=12, markeredgewidth=3, color='orange')
    plt.plot(np.real(zeros), np.imag(zeros), 'o', markersize=12, markeredgewidth=3, markerfacecolor='none', color='orange')

    plt.title(f'Lugar das Raízes (Compensador Lag) - Zero: {z}, Polo: {p}', color='white' if mode=='dark' else 'black')
    plt.savefig(os.path.join(assets_dir, '06a_rlocus_Lag.png'))
    plt.close()
    
    # Root Locus Detail (Dipole)
    plt.figure(figsize=(10, 10))
    ct.rlocus(sys_open_lag, plot=True, grid=True)
    
    # Enhanced visibility
    plt.plot(np.real(poles), np.imag(poles), 'x', markersize=12, markeredgewidth=3, color='orange')
    plt.plot(np.real(zeros), np.imag(zeros), 'o', markersize=12, markeredgewidth=3, markerfacecolor='none', color='orange')

    plt.xlim([-0.5, 0.5]) 
    plt.ylim([-0.5, 0.5])
    plt.title(f'Lugar das Raízes (Detalhe do Dipolo)\nZero={z}, Polo={p}', color='white' if mode=='dark' else 'black')
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.savefig(os.path.join(assets_dir, '06_rlocus_lag_detail.png'))
    plt.close()

    return ctrl

def design_lead_controller(sys, mode='dark'):
    """
    Design and simulate a Lead Compensator.
    """
    colors = configure_plot_style(mode)
    assets_dir = get_assets_dir(mode)
    grid_color = 'black' if mode == 'light' else 'white'
    grid_alpha = 0.3
    
    z = 13.2 
    p = 150  
    K = 700 
    
    ctrl = K * ct.tf([1, z], [1, p])
    sys_cl = ct.feedback(ctrl * sys, 1)
    
    t = np.linspace(0, 1, 1000)
    t, y = ct.step_response(sys_cl, T=t)
    
    y_final = y[-1]
    y_peak = np.max(y)
    Mp = (y_peak - y_final) / y_final * 100 if y_final != 0 else 0
    
    error = np.abs(y - y_final)
    threshold = 0.02 * np.abs(y_final)
    out_of_bounds = np.where(error > threshold)[0]
    ts = t[out_of_bounds[-1]] if len(out_of_bounds) > 0 else 0
    
    print(f"[{mode.upper()}] Lead Design Results -> Mp: {Mp:.2f}%, ts: {ts:.4f}s")
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, y, linewidth=2, color=colors[0])
    plt.title(f'Resposta ao Degrau (Lead): z={z}, p={p}, K={K}', color='white' if mode=='dark' else 'black')
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.text(0.6 * np.max(t), 0.5 * np.max(y), f'Mp = {Mp:.1f}%\nts = {ts:.3f}s', 
             bbox=dict(facecolor='black', alpha=0.5, edgecolor=colors[1]), color='white')
    plt.savefig(os.path.join(assets_dir, '12_step_response_Lead.png'))
    plt.close()
    
    plt.figure(figsize=(10, 10))
    ct.rlocus(ctrl*sys, plot=True, grid=True)
    
    # Enhanced visibility
    poles, zeros = ct.pzmap(ctrl*sys, plot=False)
    plt.plot(np.real(poles), np.imag(poles), 'x', markersize=12, markeredgewidth=3, color='orange')
    plt.plot(np.real(zeros), np.imag(zeros), 'o', markersize=12, markeredgewidth=3, markerfacecolor='none', color='orange')

    # plt.xlim([-200, 50]) # Auto-scale
    # plt.ylim([-150, 150])
    plt.title(f'Lugar das Raízes (Lead)', color='white' if mode=='dark' else 'black')
    plt.savefig(os.path.join(assets_dir, '09_root_locus_Lead.png'))
    plt.close()

    plt.figure(figsize=(10, 10))
    ct.rlocus(ctrl*sys, plot=True, grid=True)
    
    # Enhanced visibility
    plt.plot(np.real(poles), np.imag(poles), 'x', markersize=12, markeredgewidth=3, color='orange')
    plt.plot(np.real(zeros), np.imag(zeros), 'o', markersize=12, markeredgewidth=3, markerfacecolor='none', color='orange')

    plt.xlim([-20.0, 5.0])
    plt.ylim([-10.0, 10.0])
    plt.title(f'Detalhe do Cancelamento Polo-Zero (Lead)', color='white' if mode=='dark' else 'black')
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.savefig(os.path.join(assets_dir, '10_rlocus_lead_detail.png'))
    plt.close()
    
    plt.figure(figsize=(10, 8))
    omega = np.logspace(-2, 4, 1000)
    mag, phase, omega = ct.frequency_response(ctrl*sys, omega)
    mag_db = 20 * np.log10(mag)
    phase_deg = np.degrees(np.unwrap(phase))
    
    plt.subplot(2, 1, 1)
    plt.semilogx(omega, mag_db, linewidth=2, color=colors[0])
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.ylabel('Magnitude (dB)')
    plt.title('Diagrama de Bode (Lead)', color='white' if mode=='dark' else 'black')
    
    plt.subplot(2, 1, 2)
    plt.semilogx(omega, phase_deg, linewidth=2, color=colors[0])
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.ylabel('Fase (graus)')
    plt.xlabel('Frequência (rad/s)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, '11_bode_Lead.png'))
    plt.close()
    
    return ctrl

def design_lead_lag_controller(sys, mode='dark'):
    """
    Design and simulate an Integrated Lead-Lag Compensator.
    """
    colors = configure_plot_style(mode)
    assets_dir = get_assets_dir(mode)
    grid_color = 'black' if mode == 'light' else 'white'
    grid_alpha = 0.3
    
    s = ct.TransferFunction.s
    
    # Lag Part
    z_lag = 0.1
    p_lag = 0.01
    C_lag = ct.tf([1, z_lag], [1, p_lag])
    
    # Lead Part
    z_lead = 20
    p_lead = 100
    C_lead = ct.tf([1, z_lead], [1, p_lead])
    
    K = 1000
    
    ctrl = K * C_lag * C_lead
    sys_cl = ct.feedback(ctrl * sys, 1)
    
    t = np.linspace(0, 1, 2000)
    t, y = ct.step_response(sys_cl, T=t)
    
    y_final = y[-1]
    y_peak = np.max(y)
    Mp = (y_peak - y_final) / y_final * 100 if y_final != 0 else 0
    
    error = np.abs(y - y_final)
    threshold = 0.02 * np.abs(y_final)
    out_of_bounds = np.where(error > threshold)[0]
    ts = t[out_of_bounds[-1]] if len(out_of_bounds) > 0 else 0
    
    print(f"[{mode.upper()}] Integrated Lead-Lag Design Results -> Mp: {Mp:.2f}%, ts: {ts:.4f}s")
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, y, linewidth=2, color=colors[3])
    plt.title(f'Resposta Final (Lead-Lag Integrado)', color='white' if mode=='dark' else 'black')
    plt.grid(True)
    plt.text(0.6 * np.max(t), 0.5 * np.max(y), f'Mp = {Mp:.1f}%\nts = {ts:.3f}s', 
             bbox=dict(facecolor='black', alpha=0.5, edgecolor=colors[1]), color='white')
    plt.savefig(os.path.join(assets_dir, '13_step_response_LeadLag.png'))
    plt.close()
    
    plt.figure(figsize=(10, 10))
    ct.rlocus(ctrl*sys, plot=True, grid=True)
    
    # Enhanced visibility
    poles, zeros = ct.pzmap(ctrl*sys, plot=False)
    plt.plot(np.real(poles), np.imag(poles), 'x', markersize=12, markeredgewidth=3, color='orange')
    plt.plot(np.real(zeros), np.imag(zeros), 'o', markersize=12, markeredgewidth=3, markerfacecolor='none', color='orange')
    
    plt.title(f'Lugar das Raízes (Lead-Lag)', color='white' if mode=='dark' else 'black')
    plt.savefig(os.path.join(assets_dir, '14a_rlocus_LeadLag.png')) # Renamed to avoid collision
    plt.close()
    
    plt.figure(figsize=(10, 8))
    omega = np.logspace(-3, 3, 1000)
    mag, phase, omega = ct.frequency_response(ctrl*sys, omega)
    mag_db = 20 * np.log10(mag)
    phase_deg = np.degrees(np.unwrap(phase))
    
    plt.subplot(2, 1, 1)
    plt.semilogx(omega, mag_db, linewidth=2, color=colors[3])
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.ylabel('Magnitude (dB)')
    plt.title('Diagrama de Bode (Lead-Lag)', color='white' if mode=='dark' else 'black')
    
    plt.subplot(2, 1, 2)
    plt.semilogx(omega, phase_deg, linewidth=2, color=colors[3])
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.ylabel('Fase (graus)')
    plt.xlabel('Frequência (rad/s)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, '14_bode_LeadLag.png'))
    plt.close()
    
    return ctrl

def design_pid_controller(sys, mode='dark'):
    """
    Design and simulate a PID Controller (Ziegler-Nichols).
    """
    colors = configure_plot_style(mode)
    assets_dir = get_assets_dir(mode)
    grid_color = 'black' if mode == 'light' else 'white'
    grid_alpha = 0.3
    
    Kp_pid = 60000
    Ki_pid = 5000
    Kd_pid = 1000
    
    # Filter for derivative
    tau = 0.001
    
    pid_tf = ct.tf([Kd_pid, Kp_pid, Ki_pid], [tau, 1, 0])
    sys_cl = ct.feedback(pid_tf * sys, 1)
    
    t = np.linspace(0, 1.5, 1000)
    t, y = ct.step_response(sys_cl, T=t)
    
    y_final = y[-1]
    y_peak = np.max(y)
    Mp = (y_peak - y_final) / y_final * 100 if y_final != 0 else 0
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, y, linewidth=2, color=colors[3])
    plt.title(f'Resposta ao Degrau (PID Ziegler-Nichols)', color='white' if mode=='dark' else 'black')
    plt.grid(True, which='both', color=grid_color, alpha=grid_alpha)
    plt.text(0.6 * np.max(t), 0.5 * np.max(y), f'Mp = {Mp:.1f}%', 
             bbox=dict(facecolor='black', alpha=0.5, edgecolor=colors[1]), color='white')
    plt.savefig(os.path.join(assets_dir, '15_step_response_PID.png'))
    plt.close()
    
    return pid_tf

def create_plant_variation(Km, am, ae):
    """
    Cria variação da planta para análise de robustez (Nicolas).
    Nominal: Km=1.1, am=13.2, ae=950 -> K_sys=772 fixo.
    Using user parameters for K_sys check.
    """
    # Note: user defined K_sys implicitly via 1.2 * 772? 
    # Original code had K_sys=772. Let's keep the robustness logic consistent 
    # but acknowledge the new nominal plant is slightly different.
    K_sys = 772
    num = [Km * K_sys]
    den = [1, (am + ae), (am * ae), 0]
    return ct.tf(num, den)

def analyze_robustness(controllers_dict, mode='dark'):
    """
    Análise de Robustez baseada nos cenários do Nicolas.
    """
    scenarios = {
        "Nominal":   {"Km": 1.1, "am": 13.2, "ae": 950,  "style": "-", "color_dark": "#00ff00", "color_light": "green"},
        "Pesado":    {"Km": 0.8, "am": 15.0, "ae": 1100, "style": "--", "color_dark": "#00bfff", "color_light": "blue"},
        "Agressivo": {"Km": 1.2, "am": 10.0, "ae": 800,  "style": "-.", "color_dark": "#ff4500", "color_light": "red"}
    }
    
    colors = configure_plot_style(mode)
    assets_dir = get_assets_dir(mode)
    
    if mode == 'light':
        text_color = 'black'
        grid_color = 'black'
        face_color = 'white'
        grid_alpha = 0.3
    else:
        text_color = 'white'
        grid_color = 'white'
        face_color = 'black'
        grid_alpha = 0.3
    
    for ctrl_name, ctrl in controllers_dict.items():
        plt.figure(figsize=(10, 6))
        print(f"[{mode.upper()}] Analisando Robustez: {ctrl_name}")
        
        for name, params in scenarios.items():
            G_var = create_plant_variation(params["Km"], params["am"], params["ae"])
            sys_cl = ct.feedback(ctrl * G_var, 1)
            
            t, y = ct.step_response(sys_cl, T=np.linspace(0, 2.0, 1000))
            
            color = params["color_dark"] if mode == 'dark' else params["color_light"]
            
            y_peak_abs = np.max(np.abs(y))
            
            if y_peak_abs > 50:
                label_text = f"{name} (Instável)"
                # Clip data to prevent visual artifacts (vertical lines filling the plot)
                y_plot = np.clip(y, -5.0, 5.0)
            else:
                y_peak = np.max(y)
                mp = (y_peak - 1) * 100
                label_text = f"{name} (Mp={mp:.1f}%)"
                y_plot = y
            
            plt.plot(t, y_plot, linestyle=params["style"], linewidth=2, label=label_text, color=color)
            
        plt.axhline(1.0, color=text_color, linestyle=':', linewidth=0.8, alpha=0.5)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color=grid_color, alpha=grid_alpha)
        
        plt.title(f'Análise de Robustez - {ctrl_name}', color=text_color, fontsize=14)
        plt.xlabel('Tempo (s)', color=text_color, fontsize=12)
        plt.ylabel('Amplitude', color=text_color, fontsize=12)
        plt.ylim(-0.2, 2.0)
        
        legend = plt.legend(facecolor=face_color, edgecolor=text_color)
        for text in legend.get_texts():
            text.set_color(text_color)
            
        plt.tick_params(colors=text_color, which='both')
        for spine in plt.gca().spines.values():
            spine.set_color(text_color)
            
        if ctrl_name == 'PID':
            fname = '16_robustness_PID.png'
        elif ctrl_name == 'Lead-Lag':
            fname = '17_robustness_LeadLag.png'
        else:
            fname = f'robustness_{ctrl_name}.png'
            
        plt.savefig(os.path.join(assets_dir, fname))
        plt.close()

if __name__ == "__main__":
    # --- Override System with Dierson's Parameters globally ---
    # We define it here to pass to controllers, though comparison function creates its own instance to be safe
    s = ct.TransferFunction.s
    km = 1.2
    am = 13.2
    ae = 950
    sys = km/(s*(s+am)*(s+ae))

    if not os.path.exists('../assets/images'): os.makedirs('../assets/images')
    if not os.path.exists('../assets/report_images'): os.makedirs('../assets/report_images')
    
    analyze_open_loop(sys, mode='dark')
    analyze_open_loop(sys, mode='light')
    
    controllers_to_test = {}
    
    print("\n--- Running Control Simulation in DARK mode ---")
    configure_plot_style('dark')
    Kp_p = design_p_controller(sys, mode='dark')
    ctrl_lag = design_lag_controller(sys, mode='dark')
    ctrl_lead = design_lead_controller(sys, mode='dark')
    ctrl_leadlag = design_lead_lag_controller(sys, mode='dark')
    ctrl_pid = design_pid_controller(sys, mode='dark')
    
    controllers_to_test = {
        'Proportional': Kp_p,
        'Lead-Lag': ctrl_leadlag,
        'PID': ctrl_pid
    }
    
    print("\n--- Running Control Simulation in LIGHT mode (Prioritizing Report Assets) ---")
    configure_plot_style('light')
    Kp_p = design_p_controller(sys, mode='light')
    ctrl_lag = design_lag_controller(sys, mode='light')
    design_lead_controller(sys, mode='light')
    design_lead_lag_controller(sys, mode='dark')
    design_pid_controller(sys, mode='dark')
    
    # Generate comparative plots with Dierson's strict parameters
    generate_comparative_plots(sys, Kp_p, ctrl_lag, mode='dark')
    generate_comparative_plots(sys, Kp_p, ctrl_lag, mode='light')

    analyze_robustness(controllers_to_test, mode='dark')
    analyze_robustness(controllers_to_test, mode='light')
    
    print("\nTodas as simulações e gráficos foram atualizados.")
