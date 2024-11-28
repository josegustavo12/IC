module c17_tb;
    // Declaração de sinais
    reg x1, x2, x3, x6, x7;
    wire z1, z2;

    // Instância do módulo principal (C17)
    c17 uut (
        .x1(x1), .x2(x2), .x3(x3), .x6(x6), .x7(x7),
        .z1(z1), .z2(z2)
    );

    // Variável para multiplexação de falhas
    reg sel; 
    wire g1_fault;

    // Injeta falha por multiplexação
    assign g1_fault = sel ? 1'b0 : uut.g1; // Stuck-at-0 quando sel=1

    initial begin
        $monitor("Time=%0t | x1=%b x2=%b x3=%b x6=%b x7=%b | z1=%b z2=%b", 
                 $time, x1, x2, x3, x6, x7, z1, z2);

        // Teste normal (sem falha)
        $display("Teste Normal:");
        x1 = 0; x2 = 0; x3 = 0; x6 = 0; x7 = 0; sel = 0; #10;
        x1 = 1; x2 = 0; x3 = 1; x6 = 1; x7 = 0; sel = 0; #10;
        x1 = 1; x2 = 1; x3 = 1; x6 = 0; x7 = 1; sel = 0; #10;

        // Teste de Falha Stuck-At
        $display("Teste Stuck-At-0 em g1:");
        sel = 1; // Ativa stuck-at-0 em g1
        x1 = 1; x2 = 1; x3 = 1; x6 = 0; x7 = 1; #10;
        sel = 0; // Desativa falha

        // Teste de Curto-Circuito (g1 para g2)
        $display("Teste de Curto-Circuito entre g1 e g2:");
        assign uut.g2 = uut.g1; // Simula o curto
        x1 = 1; x2 = 0; x3 = 1; x6 = 1; x7 = 0; #10;

        // Teste de Temporização
        $display("Teste de Temporização:");
        x1 = 0; x2 = 1; #5;
        x1 = 1; x2 = 0; #15; 
        x1 = 1; x2 = 1; #10;

        // Teste de Redundância
        $display("Teste de Redundância:");
        wire redundant_output;
        assign redundant_output = (z1 & z2) | (z1 & x7) | (z2 & x7); // Lógica de voto
        x1 = 1; x2 = 0; x3 = 1; x6 = 0; x7 = 1; #10;
        $display("Redundancy Output: %b", redundant_output);

        // Finaliza a simulação
        $stop;
    end
endmodule
