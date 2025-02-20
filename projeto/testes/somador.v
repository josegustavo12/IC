// full_adder.v
module full_adder(sum, cout, a, b, cin);
    input a, b, cin;
    output sum, cout;
    
    // Calcula a XOR b = (a AND (NOT b)) OR ((NOT a) AND b)
    not U1(nb, b);
    and U2(a_and_nb, a, nb);
    not U3(na, a);
    and U4(na_and_b, na, b);
    or U5(x, a_and_nb, na_and_b);
    
    // Calcula sum = x XOR cin = (x AND (NOT cin)) OR ((NOT x) AND cin)
    not U6(ncin, cin);
    and U7(x_and_ncin, x, ncin);
    not U8(nx, x);
    and U9(nx_and_cin, nx, cin);
    or U10(sum, x_and_ncin, nx_and_cin);
    
    // Calcula cout = (a AND b) OR (cin AND x)
    and U11(a_and_b, a, b);
    and U12(cin_and_x, cin, x);
    or U13(cout, a_and_b, cin_and_x);
endmodule
