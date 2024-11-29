# Como executar o script

1. **Abrir o quartus e o Projeto escrito C17 (por enquanto só tem esse)**

2. **Tools -> Run Simulation tool -> RTL Simulation**

3. **Entre no diretório que está o projeto e os arquivos verilog e o script tcl**
```bash
cd C:/Users/14783765/Desktop/IC/script-tcl/quartus
```

4. **Execute o Script (nesse em especifico eu não preciso carregar o C17.v por que o script faz isso sozinho)**

```bash
do C17_simulation.tcl
```

5 **Saída do script**

```tcl
# vsim work.C17 
# Start time: 11:15:25 on Nov 29,2024
# Loading work.C17
# /C17/G8 /C17/G9 /C17/G12 /C17/G15
# 0 1 1 0 1
# 1 0 0 0 1
# 0 1 1 1 1
# 1 0 1 1 0
# 1 0 0 0 1
# 1 0 0 1 0
# 0 1 0 1 1
# 0 1 0 1 1
# 1 1 0 1 1
# 0 1 1 0 0
# 0 0 1 0 0
# 0 0 1 1 1
# 1 0 0 1 1
# 1 0 1 1 0
# 0 1 0 1 1
# 1 0 1 1 1
# 1 0 0 1 1
# 0 1 1 1 0
# 1 1 1 1 1
# 0 1 1 0 0
# Injetando falha no nó: /C17/G8
# Injetando falha no nó: /C17/G9
# Injetando falha no nó: /C17/G12
# Injetando falha no nó: /C17/G15
```