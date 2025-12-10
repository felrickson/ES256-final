import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# Planta do usuário
s = ctl.TransferFunction.s
G = 849/(s*(s+13.2)*(s+950))

print("Planta G(s) =", G)

# Parâmetros do compensador lag: C(s) = (s+b)/(s+a)
a_values = [0.01, 0.03, 0.05, 0.1, 0.3, 0.5, 1.0, 3.0, 5.0]
K_values = np.concatenate((np.linspace(0.1, 20, 200), np.linspace(20, 250, 200)))

resultados = []

for a in a_values:
    b = 10 * a
    C = (s+b)/(s+a)
    
    # sistema compensado sem realimentação: L(s) = K * C(s) * G(s)
    for K in K_values:
        L = K * C * G
        T = ctl.feedback(L, 1)  # realimentação unitária
        
        # resposta ao degrau
        t, y = ctl.step_response(T)
        
        # ---------- Especificações ----------
        # 1. Overshoot (em %)
        Mp = (max(y) - 1) * 100
        
        # 2. Tempo de acomodação 2%
        idx = np.where(abs(y - 1) <= 0.02)[0]
        ts = t[idx[0]] if len(idx) > 0 else np.inf
        
        # 3. Erro de regime para degrau
        ess = abs(1 - y[-1])

        # 4. Erro de rampa (Kv)
        er_rampa = 1/(K*0.0677)
        er_rampa_clag = 1/(K*0.677)
        Kv = K*0.677
        
        # ---------- Filtros das especificações ----------
        if (
            5 <= Mp <= 15 and
            0.5 <= ts <= 1.0 and
            ess <= 0.01 and
            er_rampa_clag <=0.01
        ):
            resultados.append((a, b, K, Mp, ts, ess, er_rampa, er_rampa_clag, Kv))

# Exibir resultados
if len(resultados) == 0:
    print("\nNenhum conjunto (a, b, K) atendeu TODAS as especificações.")
else:
    print("\nSoluções encontradas:")
    for r in resultados:
        a, b, K, Mp, ts, ess, er_rampa, er_rampa_clag, Kv = r
        print(f"\na={a:.3f}, b={b:.3f}, K={K:.3f}")
        print(f"Overshoot Mp = {Mp:.2f}%")
        print(f"Tempo ts = {ts:.3f} s")
        print(f"Erro de regime (degrau) = {ess*100:.3f}%")
        print(f"Kv = {Kv:.5f}")
        print(f"Erro de rampa = {er_rampa:.5f}")
        print(f"Erro de rampa Clag = {er_rampa_clag:.5f}")