import numpy as np
import matplotlib.pyplot as plt
import control as ct
from model import define_system

def design_p_controller(sys, Kp):
    """
    Design and simulate a Proportional Controller.
    """
    # Closed loop system
    sys_cl = ct.feedback(Kp * sys, 1)
    
    # Step Response
    t, y = ct.step_response(sys_cl)
    
    plt.figure()
    plt.plot(t, y)
    plt.title(f'Resposta ao Degrau - Controlador P (Kp={Kp})')
    plt.grid(True)
    plt.savefig('../assets/images/step_response_P.png')
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
    
    plt.figure()
    plt.plot(t, y)
    plt.title(f'Resposta ao Degrau - PID (Kp={Kp}, Ki={Ki}, Kd={Kd})')
    plt.grid(True)
    plt.savefig('../assets/images/step_response_PID.png')
    plt.close()
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
    
    plt.figure()
    plt.plot(t, y)
    plt.title('Resposta ao Degrau - Compensador Lead')
    plt.grid(True)
    plt.savefig('../assets/images/step_response_Lead.png')
    plt.close()
    
    # Root Locus (Placeholder for one of the plots)
    plt.figure()
    ct.rlocus(sys)
    plt.title('Root Locus')
    plt.savefig('../assets/images/root_locus.png')
    plt.close()

def design_lag_controller(sys):
    """
    Design and simulate a Lag Compensator (Placeholder).
    """
    # Example Lag Compensator: Gc(s) = K * (s + z) / (s + p) where z > p
    # Placeholder values
    z = 1
    p = 0.1
    K = 1
    
    ctrl = K * ct.tf([1, z], [1, p])
    sys_cl = ct.feedback(ctrl * sys, 1)
    
    t, y = ct.step_response(sys_cl)
    
    plt.figure()
    plt.plot(t, y)
    plt.title('Resposta ao Degrau - Compensador Lag')
    plt.grid(True)
    plt.savefig('../assets/images/step_response_Lag.png')
    plt.close()

if __name__ == "__main__":
    sys = define_system()
    
    # TODO: Tune these values based on actual analysis
    design_p_controller(sys, Kp=10)
    design_pid_controller(sys, Kp=10, Ki=5, Kd=2)
    design_lead_controller(sys)
    design_lag_controller(sys)
    
    print("Simulações de controle concluídas. Gráficos em assets/images/")
