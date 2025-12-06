from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Plano de Trabalho - Equipe ES256', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 6, label, 0, 1, 'L', True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

def create_pdf():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # 1. Introducao
    pdf.chapter_title('1. Objetivo e Metodologia')
    pdf.chapter_body(
        "Objetivo: Entregar uma analise completa de sistemas de controle em formato de Apresentacao Web.\n"
        "Metodologia: Divisao por pares de responsabilidade (Engenharia + Apresentacao). Cada membro contribui com uma parte tecnica e uma parte na construcao do produto final."
    )
    
    # 2. Divisao de Tarefas
    pdf.chapter_title('2. Atribuicoes Individuais')
    roles = (
        "GABRIEL (Modelagem & Roteiro):\n"
        "   > Tecnica: Definir Matrizes (A,B,C,D), Polos, Zeros e Estabilidade.\n"
        "   > Apresentacao: Redacao da Introducao, Conclusoes e conexao entre topicos.\n"
        "------------------------------------------------\n"
        "FELIPE (Controlador P & Integracao):\n"
        "   > Tecnica: Controlador Proporcional (P) e Analise de Erro Estacionario.\n"
        "   > Apresentacao: Estruturacao do HTML/CSS, Git e Montagem final.\n"
        "------------------------------------------------\n"
        "CINTIA (Compensador Lead & Diagramacao):\n"
        "   > Tecnica: Compensador de Avanco de Fase (Lead).\n"
        "   > Apresentacao: Criacao de Diagramas de Bloco e Esquematicos visuais.\n"
        "------------------------------------------------\n"
        "DIERSON (Compensador Lag & Visualizacao):\n"
        "   > Tecnica: Compensador de Atraso de Fase (Lag).\n"
        "   > Apresentacao: Padronizacao estetica dos graficos (Matplotlib).\n"
        "------------------------------------------------\n"
        "GUILHERME (PID & Revisao Tecnica):\n"
        "   > Tecnica: Controlador PID (Sintonia Ziegler-Nichols).\n"
        "   > Apresentacao: Revisao de consistencia tecnica e equacoes.\n"
        "------------------------------------------------\n"
        "NICOLAS (Robustez & Qualidade (QA)):\n"
        "   > Tecnica: Analise de Robustez e Incertezas.\n"
        "   > Apresentacao: Testes de usabilidade e conducao do Ensaio."
    )
    pdf.chapter_body(roles)
    
    # 3. Cronograma
    pdf.chapter_title('3. Cronograma de Execucao')
    
    schedule = (
        "FASE 1 - Setup (Sexta/Sabado):\n"
        "- M1 define e compartilha os dados do modelo.\n"
        "- M2 configura o ambiente de desenvolvimento (Repo/Site).\n"
        "- Todos iniciam suas simulacoes individuais.\n\n"
        "FASE 2 - Desenvolvimento (Domingo/Segunda):\n"
        "- Simulacoes concluidas e graficos gerados.\n"
        "- M3 e M4 produzem os elementos visuais de apoio.\n"
        "- Envio de material para M2 integrar no site.\n\n"
        "FASE 3 - Finalizacao (Terca/Quarta):\n"
        "- M5 revisa todo o conteudo tecnico.\n"
        "- M6 testa a apresentacao e cronometra o tempo.\n"
        "- Ajustes finais e entrega."
    )
    pdf.chapter_body(schedule)

    pdf.output("Plano_Equipe_ES256_Final.pdf")

if __name__ == '__main__':
    create_pdf()
