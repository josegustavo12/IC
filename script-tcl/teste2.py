import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk

# Variáveis globais
tcl_file = None
text_no_error = None
text_with_error = None
text_comparison = None


def create_widgets(root):
    # Frame principal
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Label do título
    tk.Label(main_frame, text="Executor de Simulação TCL para ModelSim", font=("Arial", 16, "bold")).pack(pady=10)

    # Botão para selecionar script TCL
    tcl_button = tk.Button(main_frame, text="Selecionar Script TCL", command=load_tcl_file)
    tcl_button.pack(pady=5)

    # Label para exibir o caminho do arquivo selecionado
    global tcl_label
    tcl_label = tk.Label(main_frame, text="Nenhum arquivo selecionado", fg="gray")
    tcl_label.pack()

    # Botão para executar o script
    global run_button
    run_button = tk.Button(main_frame, text="Executar Script", command=run_tcl_script, state=tk.DISABLED)
    run_button.pack(pady=5)

    # Criação das abas
    global tab_control, text_no_error, text_with_error, text_comparison
    tab_control = ttk.Notebook(main_frame)
    tab_control.pack(fill=tk.BOTH, expand=True, pady=10)

    # Aba para saída do circuito sem erros
    tab_no_error = ttk.Frame(tab_control)
    tab_control.add(tab_no_error, text='Circuito Sem Erros')
    text_no_error = create_text_area(tab_no_error, 'Saída do Circuito Sem Erros')

    # Aba para saída do circuito com erros
    tab_with_error = ttk.Frame(tab_control)
    tab_control.add(tab_with_error, text='Circuito Com Erros')
    text_with_error = create_text_area(tab_with_error, 'Saída do Circuito Com Erros')

    # Aba para comparação
    tab_comparison = ttk.Frame(tab_control)
    tab_control.add(tab_comparison, text='Comparação')
    text_comparison = create_text_area(tab_comparison, 'Resultados da Comparação')

    # Botão para fechar a aplicação
    tk.Button(main_frame, text="Sair", command=root.quit).pack(pady=10)


def create_text_area(parent, label_text):
    label = tk.Label(parent, text=label_text, font=("Arial", 12))
    label.pack(pady=5)
    text_area = scrolledtext.ScrolledText(parent, width=80, height=20, state=tk.DISABLED)
    text_area.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
    return text_area


def load_tcl_file():
    global tcl_file, run_button, tcl_label

    # Abrir diálogo para selecionar o arquivo TCL
    tcl_file = filedialog.askopenfilename(filetypes=[("Arquivos TCL", "*.tcl")], title="Selecione o Script TCL")
    if tcl_file:
        tcl_label.config(text=f"Script Selecionado: {tcl_file}")
        run_button.config(state=tk.NORMAL)
    else:
        tcl_label.config(text="Nenhum arquivo selecionado")
        run_button.config(state=tk.DISABLED)


def run_tcl_script():
    global tcl_file, text_no_error, text_with_error, text_comparison

    # Verificar se o arquivo foi selecionado
    if not tcl_file:
        messagebox.showerror("Erro", "Selecione um arquivo TCL antes de executar!")
        return

    # Especifique o caminho completo para o ModelSim
    modelsim_path = r"C:\\intelFPGA\\19.1\\modelsim_ase\\win32aloem\\vsim.exe"

    # Diretório onde os logs serão salvos
    results_dir = os.path.join(os.path.dirname(tcl_file), 'results')

    # Executar o script TCL no ModelSim
    try:
        # Limpar áreas de texto
        clear_text_areas()

        # Executar o script TCL
        process = subprocess.run(
            [modelsim_path, "-c", "-do", tcl_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(tcl_file)
        )

        # Verificar sucesso ou falha
        if process.returncode == 0:
            messagebox.showinfo("Sucesso", "Script executado com sucesso!")
        else:
            messagebox.showwarning("Erro", "Erros ocorreram durante a execução. Verifique os detalhes na saída.")

        # Exibir os logs nas abas correspondentes
        display_logs(results_dir)

    except FileNotFoundError:
        messagebox.showerror("Erro", "O ModelSim não foi encontrado no caminho especificado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Um erro inesperado ocorreu:\n{e}")


def clear_text_areas():
    # Limpar áreas de texto (torná-las editáveis temporariamente)
    for text_widget in [text_no_error, text_with_error, text_comparison]:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.config(state=tk.DISABLED)


def display_logs(results_dir):
    global text_no_error, text_with_error, text_comparison

    # Exibir o log do circuito sem erros
    no_error_log = os.path.join(results_dir, 'results_no_fault.log')
    if os.path.exists(no_error_log):
        with open(no_error_log, 'r') as file:
            content = file.read()
        update_text_widget(text_no_error, content)
    else:
        update_text_widget(text_no_error, 'Log não encontrado.')

    # Exibir os logs do circuito com erros e comparações
    fault_nodes = ['/C17/G8', '/C17/G9', '/C17/G12', '/C17/G15']
    for node in fault_nodes:
        sanitized_node = node.replace('/', '_')
        # Log do circuito com erro
        with_error_log = os.path.join(results_dir, f'results_with_fault_{sanitized_node}.log')
        if os.path.exists(with_error_log):
            with open(with_error_log, 'r') as file:
                content = file.read()
            update_text_widget(text_with_error, f"=== Falha no nó {node} ===\n{content}\n", append=True)
        else:
            update_text_widget(text_with_error, f"Log para {node} não encontrado.\n", append=True)

        # Log de comparação
        comparison_log = os.path.join(results_dir, f'comparison_{sanitized_node}.log')
        if os.path.exists(comparison_log):
            with open(comparison_log, 'r') as file:
                content = file.read()
            update_text_widget(text_comparison, f"=== Comparação para {node} ===\n{content}\n", append=True)
        else:
            update_text_widget(text_comparison, f"Comparação para {node} não encontrada.\n", append=True)


def update_text_widget(text_widget, content, append=False):
    text_widget.config(state=tk.NORMAL)
    if append:
        text_widget.insert(tk.END, content)
    else:
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)
    text_widget.config(state=tk.DISABLED)


if __name__ == "__main__":
    # Iniciar a aplicação
    root = tk.Tk()
    root.title("Executor de Simulação ModelSim")
    create_widgets(root)
    root.mainloop()
