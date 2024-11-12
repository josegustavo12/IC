module half_adder_fault(
    input a,
    input b,
    output sum,
    output carry
);
    assign sum = a ^ b;
    assign carry = ~(a & b); // Erro intencional
endmodule
