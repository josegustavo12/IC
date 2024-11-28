# Carregar o módulo C17 no ModelSim
vsim work.C17

# Configuração de saída para registrar os sinais
log -r /*

# Procedimento para carregar os vetores de teste
proc load_test_vectors {filename} {
    set vectors [list]
    set fp [open $filename r]
    while {[gets $fp line] >= 0} {
        lappend vectors $line
    }
    close $fp
    return $vectors
}

# Procedimento para aplicar os vetores ao circuito e injetar falhas
proc apply_vectors {vectors fault_node} {
    foreach vector $vectors {
        set inputs [split $vector " "]

        # Configurar os sinais de entrada
        force /C17/G1 [lindex $inputs 0]
        force /C17/G2 [lindex $inputs 1]
        force /C17/G3 [lindex $inputs 2]
        force /C17/G4 [lindex $inputs 3]
        force /C17/G5 [lindex $inputs 4]

        # Injetar falha stuck-at-0 no nó especificado
        force $fault_node 0

        # Executar a simulação por 100 ns
        run 100ns

        # Remover a falha
        noforce $fault_node
    }
}

# Lista de nós internos onde as falhas serão injetadas
set fault_nodes {/C17/G8 /C17/G9 /C17/G12 /C17/G15}

# Carregar os vetores de teste
set vectors [load_test_vectors "C:/Users/14783765/Desktop/IC/script-tcl/RANDOM/random_vectors.txt"]

# Aplicar os vetores e injetar falhas
foreach node $fault_nodes {
    puts "Injetando falha no nó: $node"
    apply_vectors $vectors $node
}

# Procedimento para salvar os valores das saídas
proc save_results {filename} {
    set fp [open $filename w]
    # Loop para capturar os valores das saídas e salvar
    foreach signal {/C17/G16 /C17/G17} {
        set value [examine $signal]
        puts $fp "$signal: $value"
    }
    close $fp
}

# Salvar os resultados no arquivo 'results.log'
save_results "results.log"
