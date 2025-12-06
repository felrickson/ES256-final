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
    ctrl = ct.tf([Kd, Kp, Ki], [1, 0])
    sys_cl = ct.feedback(ctrl * sys, 1)
    
    t, y = ct.step_response(sys_cl)
    
    plt.figure()
    plt.plot(t, y)
    plt.title(f'Resposta ao Degrau - PID (Kp={Kp}, Ki={Ki}, Kd={Kd})')
    plt.grid(True)
    plt.savefig('../assets/images/step_response_PID.png')
    plt.close()

if __name__ == "__main__":
    sys = define_system()
    
    # TODO: Tune these values
    design_p_controller(sys, Kp=10)
    design_pid_controller(sys, Kp=10, Ki=5, Kd=2)
    print("Simulações de controle concluídas.")
