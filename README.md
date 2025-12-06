# Projeto Final ES256 - Servomecanismo

Este repositório contém a estrutura para a apresentação final do projeto.

## Estrutura de Pastas

*   `input_materials/`: Materiais originais (PDF do professor, áudios, etc).
*   `docs/`: Documentação do grupo (Plano de Ação, Scripts de gestão).
*   `index.html`: A apresentação em si. **Não edite a estrutura sem falar com o Tech Lead.**
*   `css/`: Estilos visuais.
*   `js/`: Scripts da página.
*   `assets/images/`: **Destino dos gráficos gerados pelo Python.** Salve seus plots aqui.
*   `simulations/`: Scripts Python para modelagem e controle.

## Divisão de Tarefas (Conforme Plano PDF)

*   **Gabriel (Modelagem & Roteiro):** Define matrizes e escreve a história (Intro/Conclusão).
*   **Felipe (Controlador P & Integração):** Faz o P e cuida do HTML/CSS/Git.
*   **Cintia (Lead & Diagramas):** Faz o Compensador Lead e diagramas visuais.
*   **Dierson (Lag & Visualização):** Faz o Compensador Lag e padroniza gráficos Matplotlib.
*   **Guilherme (PID & Revisão):** Faz o PID (técnico) e revisa consistência técnica.
*   **Nicolas (Robustez & QA):** Faz análise de robustez e testes da apresentação.

## Para o Grupo A (Simulação)

1.  Instale as dependências:
    ```bash
    pip3 install numpy matplotlib control
    ```
2.  Edite `simulations/model.py` para inserir as matrizes A, B, C, D corretas do PDF.
3.  Use `simulations/controllers.py` para projetar os controladores.
4.  Ao rodar os scripts, as imagens serão salvas automaticamente em `assets/images/`.

## Para o Grupo B (Frontend/Design)

1.  Abra `index.html` no navegador para visualizar.
2.  Para editar o conteúdo de texto, procure pelas seções marcadas com comentários (Ex: `<!-- Introduction -->`).
3.  Estamos usando TailwindCSS via CDN para agilidade. Consulte a [documentação do Tailwind](https://tailwindcss.com/docs) para classes.

## Próximos Passos (Sexta/Sábado)

*   **Grupo A:** Preencher `model.py` com os dados reais.
*   **Grupo B:** Revisar os textos do `index.html` e ajustar o Design se necessário.

## Como Publicar (Deploy)

A maneira mais fácil de compartilhar essa apresentação é via **GitHub Pages**:

1.  Faça o upload de todos os arquivos para um repositório no GitHub.
2.  No GitHub, vá em **Settings** > **Pages**.
3.  Em "Source", escolha **Deploy from a branch**.
4.  Selecione a branch `main` e a pasta `/ (root)`.
5.  Clique em Save. Em alguns minutos, sua apresentação estará online.
