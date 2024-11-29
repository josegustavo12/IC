import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


class ModelSimExecutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Executor de Simulação ModelSim")

        # Interface principal
        self.create_widgets()

    def create_widgets(self):
        # Label do título
        tk.Label(self.root, text="Executor de Simulação TCL para ModelSim", font=("Arial", 16, "bold")).pack(pady=10)

        # Botão para selecionar script TCL
        self.tcl_button = tk.Button(self.root, text="Selecionar Script TCL", command=self.load_tcl_file)
        self.tcl_button.pack(pady=5)

        # Label para exibir o caminho do arquivo selecionado
        self.tcl_label = tk.Label(self.root, text="Nenhum arquivo selecionado", fg="gray")
        self.tcl_label.pack()

        # Botão para executar o script
        self.run_button = tk.Button(self.root, text="Executar Script", command=self.run_tcl_script, state=tk.DISABLED)
        self.run_button.pack(pady=5)

        # Área de exibição de resultados
        tk.Label(self.root, text="Saída do Script:", font=("Arial", 12)).pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.output_text.pack(pady=5)

        # Botão para fechar a aplicação
        tk.Button(self.root, text="Sair", command=self.root.quit).pack(pady=10)

    def load_tcl_file(self):
        # Abrir diálogo para selecionar o arquivo TCL
        tcl_file = filedialog.askopenfilename(
            filetypes=[("Arquivos TCL", "*.tcl")], title="Selecione o Script TCL"
        )
        if tcl_file:
            self.tcl_file = tcl_file
            self.tcl_label.config(text=f"Script Selecionado: {tcl_file}")
            self.run_button.config(state=tk.NORMAL)
        else:
            self.tcl_label.config(text="Nenhum arquivo selecionado")
            self.run_button.config(state=tk.DISABLED)

    def run_tcl_script(self):
        # Verificar se o arquivo foi selecionado
        if not hasattr(self, "tcl_file") or not self.tcl_file:
            messagebox.showerror("Erro", "Selecione um arquivo TCL antes de executar!")
            return

        # Especifique o caminho completo para o ModelSim
        modelsim_path = r"C:\\intelFPGA\\19.1\\modelsim_ase\\win32aloem\\vsim.exe"  

        # Executar o script TCL no ModelSim
        try:
            self.output_text.delete(1.0, tk.END)  # Limpar área de saída
            process = subprocess.run(
                [modelsim_path, "-c", "-do", self.tcl_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            # Exibir saída e erros na área de texto
            self.output_text.insert(tk.END, "=== Saída do Script ===\n")
            self.output_text.insert(tk.END, process.stdout)
            self.output_text.insert(tk.END, "\n=== Erros do Script ===\n")
            self.output_text.insert(tk.END, process.stderr)

            # Notificar sucesso ou falha
            if process.returncode == 0:
                messagebox.showinfo("Sucesso", "Script executado com sucesso!")
            else:
                messagebox.showwarning("Erro", "Erros ocorreram durante a execução. Verifique os detalhes na saída.")
        except FileNotFoundError:
            messagebox.showerror("Erro", "O ModelSim não foi encontrado no caminho especificado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Um erro inesperado ocorreu:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModelSimExecutorApp(root)
    root.mainloop()
