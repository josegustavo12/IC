# Carregar o módulo C17 no ModelSim
vsim work.C17

# Criar diretório de resultados, se necessário
if {![file exists "./results"]} {
    file mkdir "./results"
}

# Caminho para o arquivo de vetores de teste
set vectors_file "C:/Users/14783765/Desktop/IC/script-tcl/RANDOM/random_vectors.txt"

# Carregar os vetores de teste
set vectors [list]
set fp [open $vectors_file r]
while {[gets $fp line] >= 0} {
    # Verificar se a linha não está vazia e possui 5 entradas
    if {[string trim $line] ne "" && [llength [split $line " "]] == 5} {
        lappend vectors $line
    } else {
        puts "Aviso: Vetor inválido ou incompleto encontrado e será ignorado: \"$line\""
    }
}
close $fp

# Função para executar a simulação e capturar estados
proc run_simulation {fault_node vectors} {
    # Reiniciar a simulação de forma forçada
    restart -f
    
    # Executar um tempo para estabilizar após o reset
    run 10ns
    
    # Injetar falha se especificado
    if {$fault_node ne ""} {
        force $fault_node 0
    }
    
    # Capturar estado inicial
    set g16_initial [examine /C17/G16]
    set g17_initial [examine /C17/G17]
    
    # Aplicar vetores de teste
    foreach vector $vectors {
        set inputs [split $vector " "]
        
        # Forçar os sinais de entrada
        force /C17/G1 [lindex $inputs 0]
        force /C17/G2 [lindex $inputs 1]
        force /C17/G3 [lindex $inputs 2]
        force /C17/G4 [lindex $inputs 3]
        force /C17/G5 [lindex $inputs 4]
        
        # Executar a simulação por 100 ns para cada vetor
        run 100ns
    }
    
    # Executar tempo adicional para estabilização após aplicação dos vetores
    run 50ns
    
    # Capturar estado final
    set g16_final [examine /C17/G16]
    set g17_final [examine /C17/G17]
    
    # Remover a falha injetada
    if {$fault_node ne ""} {
        noforce $fault_node
    }
    
    # Retornar os estados capturados
    return [list $g16_initial $g17_initial $g16_final $g17_final]
}

# Simulação SEM falhas
puts "Iniciando simulação SEM falhas..."

# Executar a simulação sem injetar falhas
set results_no_fault [run_simulation "" $vectors]

# Extrair estados iniciais e finais
set g16_initial_no_fault [lindex $results_no_fault 0]
set g17_initial_no_fault [lindex $results_no_fault 1]
set g16_final_no_fault [lindex $results_no_fault 2]
set g17_final_no_fault [lindex $results_no_fault 3]

# Salvar estados SEM falhas em um arquivo
set fp_no_fault [open "./results/states_no_fault.log" w]
puts $fp_no_fault "Estados SEM falhas:"
puts $fp_no_fault "Estado Inicial: $g16_initial_no_fault $g17_initial_no_fault"
puts $fp_no_fault "Estado Final: $g16_final_no_fault $g17_final_no_fault"
close $fp_no_fault

puts "Simulação SEM falhas concluída. Resultados salvos em ./results/states_no_fault.log"

# Lista de nós internos onde as falhas serão injetadas com o nome da porta
# Cada entrada é {node gate_name}
set fault_nodes {
    {/C17/G8 NAND2_0}
    {/C17/G9 NAND2_1}
    {/C17/G12 NAND2_2}
    {/C17/G15 NAND2_3}
}

# Simulações COM falhas
foreach fault_entry $fault_nodes {
    # Extrair node e gate_name
    set node [lindex $fault_entry 0]
    set gate [lindex $fault_entry 1]
    
    puts "Iniciando simulação COM falha na porta: $gate"
    
    # Executar a simulação com a falha injetada
    set results_with_fault [run_simulation $node $vectors]
    
    # Extrair estados iniciais e finais
    set g16_initial_with_fault [lindex $results_with_fault 0]
    set g17_initial_with_fault [lindex $results_with_fault 1]
    set g16_final_with_fault [lindex $results_with_fault 2]
    set g17_final_with_fault [lindex $results_with_fault 3]
    
    # Salvar estados COM falha em um arquivo (modo append)
    set fp_with_fault [open "./results/states_with_fault.log" a]
    puts $fp_with_fault "Estados COM falhas na porta: $gate"
    puts $fp_with_fault "Estado Inicial: $g16_initial_with_fault $g17_initial_with_fault"
    puts $fp_with_fault "Estado Final: $g16_final_with_fault $g17_final_with_fault"
    puts $fp_with_fault ""
    close $fp_with_fault
    
    puts "Simulação COM falha na porta $gate concluída. Resultados adicionados a ./results/states_with_fault.log"
}

puts "Todas as simulações foram concluídas. Resultados salvos na pasta ./results"
