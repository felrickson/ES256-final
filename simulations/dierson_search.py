import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# Planta do usuário
# G = 849/(s*(s+13.2)*(s+950))
s = ctl.TransferFunction.s
G = 849/(s*(s+13.2)*(s+950))

print("Planta G(s) =", G)

# Parâmetros do compensador lag: C(s) = (s+b)/(s+a)
a_values = [0.01, 0.03, 0.05, 0.1, 0.3, 0.5, 1.0, 3.0, 5.0]
# Reduced points for speed in this test, but keeping range
K_values = np.concatenate((np.linspace(0.1, 20, 50), np.linspace(20, 250, 50)))

resultados = []

print("Iniciando busca de parâmetros...")

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
        if len(y) > 0:
            Mp = (max(y) - 1) * 100
        else:
            Mp = 100 # invalid
        
        # 2. Tempo de acomodação 2%
        idx = np.where(abs(y - 1) <= 0.02)[0]
        # Check if it actually stays settled (simple check: is the last point settled?)
        if abs(y[-1] - 1) <= 0.02 and len(idx) > 0:
             # Find the first index where it settles and stays settled (simplified for now: just first match end)
             # Better check: iterate backwards
             settled_idx = len(y) - 1
             while settled_idx >= 0 and abs(y[settled_idx] - 1) <= 0.02:
                 settled_idx -= 1
             ts = t[settled_idx + 1] if settled_idx + 1 < len(t) else t[-1]
        else:
            ts = np.inf
        
        # 3. Erro de regime para degrau
        ess = abs(1 - y[-1])

        # 4. Erro de rampa (Kv)
        # G(s) has type 1 (one integrator). Lag adds no integrators.
        # System is Type 1.
        # Kv = limit s->0 s * K * C(s) * G(s)
        # C(0) = b/a = 10.
        # G(s) ~ 849 / (s * 13.2 * 950) = 849/(12540*s) = 0.0677/s
        # L(s) ~ K * 10 * 0.0677 / s = 0.677*K / s
        # Kv = 0.677 * K
        # ess_ramp = 1/Kv
        
        Kv = K * 0.677
        er_rampa_clag = 1/Kv if Kv > 0 else np.inf
        
        # ---------- Filtros das especificações ----------
        if (
            5 <= Mp <= 15 and
            0.5 <= ts <= 1.0 and
            ess <= 0.01 and  # 1% steady state error
            er_rampa_clag <= 0.01 # This seems very strict? 1/Kv <= 0.01 => Kv >= 100. K*0.677 >= 100 => K >= 147.
        ):
            resultados.append((a, b, K, Mp, ts, ess, er_rampa_clag, Kv))

# Exibir resultados
if len(resultados) == 0:
    print("\nNenhum conjunto (a, b, K) atendeu TODAS as especificações.")
else:
    print(f"\nSoluções encontradas: {len(resultados)}")
    # Sort by smallest error or fastest ts
    resultados.sort(key=lambda x: x[3]) # Sort by overshoot (Mp)
    
    for i, r in enumerate(resultados[:5]): # Show top 5
        a, b, K, Mp, ts, ess, er_rampa_clag, Kv = r
        print(f"\nSolução {i+1}:")
        print(f"a={a:.3f}, b={b:.3f}, K={K:.3f}")
        print(f"Overshoot Mp = {Mp:.2f}%")
        print(f"Tempo ts = {ts:.3f} s")
        print(f"Erro de regime (degrau) = {ess*100:.3f}%")
        print(f"Kv = {Kv:.5f}")
        print(f"Erro de rampa Clag = {er_rampa_clag:.5f}")
