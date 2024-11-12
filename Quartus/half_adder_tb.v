`timescale 1ns/1ps

module half_adder_tb;
    reg a;
    reg b;
    wire sum;
    wire carry;

    // Instanciar o módulo a ser testado
    half_adder_fault uut (
        .a(a),
        .b(b),
        .sum(sum),
        .carry(carry)
    );

    initial begin
        // Abrir o arquivo para dump das formas de onda (opcional)
        $dumpfile("half_adder_tb.vcd");
        $dumpvars(0, half_adder_tb);

        // Aplicar estímulos às entradas
        a = 0; b = 0; #10;
        $display("Tempo=%0t ns | a=%b, b=%b | sum=%b, carry=%b", $time, a, b, sum, carry);

        a = 0; b = 1; #10;
        $display("Tempo=%0t ns | a=%b, b=%b | sum=%b, carry=%b", $time, a, b, sum, carry);

        a = 1; b = 0; #10;
        $display("Tempo=%0t ns | a=%b, b=%b | sum=%b, carry=%b", $time, a, b, sum, carry);

        a = 1; b = 1; #10;
        $display("Tempo=%0t ns | a=%b, b=%b | sum=%b, carry=%b", $time, a, b, sum, carry);

        $finish;
    end
endmodule
