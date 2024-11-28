module somador_2bits (
    input [1:0] A,
    input [1:0] B,
    output [2:0] S
);

    wire c0, c1, sum0, sum1;

    // Somador para o bit menos significativo (A[0] e B[0])
    not(t_100, A[0]);
    not(t_101, B[0]);
    or(sum0, t_100, t_101); // XOR para a soma
    and(c0, A[0], B[0]); // Carry para o próximo bit

    // Somador para o bit mais significativo (A[1] e B[1])
    not(t_102, A[1]);
    not(t_103, B[1]);
    or(sum1, t_102, t_103); // XOR para a soma
    and(c1, A[1], B[1]); // Carry para o próximo bit

    // Soma final
    assign S[0] = sum0;
    assign S[1] = sum1 ^ c0; // Soma do segundo bit com carry anterior
    or(S[2], c1, c0); // Carry final para o bit mais significativo

endmodule
