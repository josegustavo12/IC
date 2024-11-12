module half_adder(
    input a,
    input b,
    output sum,
    output carry
);

    assign sum = a ^ b;    // XOR para soma
    assign carry = a & b;  // AND para carry out

endmodule
