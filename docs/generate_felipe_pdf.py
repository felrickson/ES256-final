
import numpy as np
# Monkey patch for numpy 2.0 compatibility with older control libs
if not hasattr(np, 'NaN'):
    np.NaN = np.nan

import matplotlib.pyplot as plt
import control as ct
from simulations.model import define_system
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os

# Ensure assets dir exists
if not os.path.exists("assets/images"):
    os.makedirs("assets/images")

def generate_plots():
    sys = define_system()
    
    # 1. Root Locus
    plt.figure(figsize=(8, 6))
    ct.rlocus(sys, plot=True, grid=True)
    plt.title("Locus das Raízes - Sistema em Malha Aberta")
    plt.savefig("assets/images/felipe_rlocus.png")
    plt.close()
    
    # 2. Step Response Comparison
    plt.figure(figsize=(8, 6))
    ks = [1, 5, 20]
    for k in ks:
        sys_cl = ct.feedback(k * sys, 1)
        t, y = ct.step_response(sys_cl)
        plt.plot(t, y, label=f'Kp={k}')
        
    plt.title("Resposta ao Degrau para Diferentes Ganhos Kp")
    plt.ylabel("Posição (rad)")
    plt.xlabel("Tempo (s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("assets/images/felipe_step_compare.png")
    plt.close()
    
    # 3. Final Design (e.g., Kp=5)
    kp_final = 5.0
    sys_cl = ct.feedback(kp_final * sys, 1)
    t, y = ct.step_response(sys_cl)
    plt.figure(figsize=(8, 6))
    plt.plot(t, y)
    plt.title(f"Resposta Final com Kp={kp_final}")
    plt.grid(True)
    plt.savefig("assets/images/felipe_final_step.png")
    plt.close()

def create_pdf():
    c = canvas.Canvas("input_materials/Servomecanismo - Felipe.pdf", pagesize=A4)
    width, height = A4
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, height - 2*cm, "Servomecanismo - Projeto do Controlador Proporcional")
    c.setFont("Helvetica", 12)
    c.drawString(2*cm, height - 3*cm, "Responsável: Felipe (Integração/P)")
    c.drawString(2*cm, height - 3.5*cm, "Data: 06/12/2025")
    
    # 1. Objetivo
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, height - 5*cm, "1. Objetivo")
    c.setFont("Helvetica", 11)
    text = c.beginText(2*cm, height - 5.5*cm)
    text.textLines("""
    O objetivo desta etapa é projetar um controlador Proporcional (P) para o servomecanismo
    modelado. O controlador deve garantir erro nulo em regime permanente para uma entrada
    degrau (garantido pelo tipo do sistema) e melhorar a resposta transitória dentro dos limites
    de estabilidade.
    """)
    c.drawText(text)
    
    # 2. Análise do Lugar das Raízes
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, height - 8*cm, "2. Análise do Lugar das Raízes")
    c.drawImage("assets/images/felipe_rlocus.png", 2*cm, height - 16*cm, width=14*cm, height=7*cm, preserveAspectRatio=True)
    
    c.setFont("Helvetica", 11)
    text = c.beginText(2*cm, height - 16.5*cm)
    text.textLines("""
    O Locus das Raízes mostra que o sistema é estável para todos os ganhos positivos (K > 0),
    pois os ramos permanecem no semiplano esquerdo. No entanto, aumentar K aproxima os polos
    do eixo imaginário, aumentando a oscilação.
    """)
    c.drawText(text)
    
    # 3. Comparação de Ganhos
    c.showPage() # New Page
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, height - 2*cm, "3. Seleção do Ganho (Kp)")
    
    c.drawImage("assets/images/felipe_step_compare.png", 2*cm, height - 10*cm, width=14*cm, height=7*cm, preserveAspectRatio=True)
    
    c.setFont("Helvetica", 11)
    text = c.beginText(2*cm, height - 10.5*cm)
    text.textLines("""
    Foram testados três valores de ganho:
    - Kp = 1: Resposta lenta, sem overshoot significativo.
    - Kp = 5: Bom compromisso entre velocidade e oscilação.
    - Kp = 20: Muito rápido, mas com overshoot excessivo e oscilação prolongada.
    """)
    c.drawText(text)
    
    # 4. Conclusão
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, height - 13*cm, "4. Conclusão e Definição")
    c.setFont("Helvetica", 11)
    text = c.beginText(2*cm, height - 13.5*cm)
    text.textLines("""
    Optou-se pelo ganho Kp = 5.0. 
    Este valor proporciona um tempo de subida aceitável para a aplicação
    sem introduzir oscilações perigosas que poderiam excitar as dinâmicas não modeladas.
    
    O erro em regime permanente para degrau é zero, conforme previsto pela modelagem (Tipo 1).
    """)
    c.drawText(text)
    
    c.save()
    print("PDF Gerado com sucesso: input_materials/Servomecanismo - Felipe.pdf")

if __name__ == "__main__":
    generate_plots()
    create_pdf()
