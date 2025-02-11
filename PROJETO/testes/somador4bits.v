// four_bit_adder.v
module four_bit_adder(
    input a0, a1, a2, a3, b0, b1, b2, b3, cin
    output cout, s0, s1, s2, s3
);

    // Fios para propagação dos carries internos
    wire c1, c2, c3;
    
    // ----------------------------
    // Bit 0 (menos significativo)
    // ----------------------------
    wire nb0, a0_and_nb0, na0, na0_and_b0, x0;
    wire ncin0, x_and_ncin0, nx0, nx_and_cin0;
    wire a0_and_b0, cin_and_x0;
    
    // Calcula x0 = a0 XOR b0
    not U1_0(nb0, b0);
    and U2_0(a0_and_nb0, a0, nb0);
    not U3_0(na0, a0);
    and U4_0(na0_and_b0, na0, b0);
    or  U5_0(x0, a0_and_nb0, na0_and_b0);
    
    // Calcula s0 = x0 XOR cin
    not U6_0(ncin0, cin);
    and U7_0(x_and_ncin0, x0, ncin0);
    not U8_0(nx0, x0);
    and U9_0(nx_and_cin0, nx0, cin);
    or  U10_0(s0, x_and_ncin0, nx_and_cin0);
    
    // Calcula c1 = (a0 AND b0) OR (cin AND x0)
    and U11_0(a0_and_b0, a0, b0);
    and U12_0(cin_and_x0, cin, x0);
    or  U13_0(c1, a0_and_b0, cin_and_x0);
    
    // ----------------------------
    // Bit 1
    // ----------------------------
    wire nb1, a1_and_nb1, na1, na1_and_b1, x1;
    wire ncin1, x_and_ncin1, nx1, nx_and_cin1;
    wire a1_and_b1, cin_and_x1;
    
    // Calcula x1 = a1 XOR b1
    not U1_1(nb1, b1);
    and U2_1(a1_and_nb1, a1, nb1);
    not U3_1(na1, a1);
    and U4_1(na1_and_b1, na1, b1);
    or  U5_1(x1, a1_and_nb1, na1_and_b1);
    
    // Calcula s1 = x1 XOR c1
    not U6_1(ncin1, c1);
    and U7_1(x_and_ncin1, x1, ncin1);
    not U8_1(nx1, x1);
    and U9_1(nx_and_cin1, nx1, c1);
    or  U10_1(s1, x_and_ncin1, nx_and_cin1);
    
    // Calcula c2 = (a1 AND b1) OR (c1 AND x1)
    and U11_1(a1_and_b1, a1, b1);
    and U12_1(cin_and_x1, c1, x1);
    or  U13_1(c2, a1_and_b1, cin_and_x1);
    
    // ----------------------------
    // Bit 2
    // ----------------------------
    wire nb2, a2_and_nb2, na2, na2_and_b2, x2;
    wire ncin2, x_and_ncin2, nx2, nx_and_cin2;
    wire a2_and_b2, cin_and_x2;
    
    // Calcula x2 = a2 XOR b2
    not U1_2(nb2, b2);
    and U2_2(a2_and_nb2, a2, nb2);
    not U3_2(na2, a2);
    and U4_2(na2_and_b2, na2, b2);
    or  U5_2(x2, a2_and_nb2, na2_and_b2);
    
    // Calcula s2 = x2 XOR c2
    not U6_2(ncin2, c2);
    and U7_2(x_and_ncin2, x2, ncin2);
    not U8_2(nx2, x2);
    and U9_2(nx_and_cin2, nx2, c2);
    or  U10_2(s2, x_and_ncin2, nx_and_cin2);
    
    // Calcula c3 = (a2 AND b2) OR (c2 AND x2)
    and U11_2(a2_and_b2, a2, b2);
    and U12_2(cin_and_x2, c2, x2);
    or  U13_2(c3, a2_and_b2, cin_and_x2);
    
    // ----------------------------
    // Bit 3 (mais significativo)
    // ----------------------------
    wire nb3, a3_and_nb3, na3, na3_and_b3, x3;
    wire ncin3, x_and_ncin3, nx3, nx_and_cin3;
    wire a3_and_b3, cin_and_x3;
    
    // Calcula x3 = a3 XOR b3
    not U1_3(nb3, b3);
    and U2_3(a3_and_nb3, a3, nb3);
    not U3_3(na3, a3);
    and U4_3(na3_and_b3, na3, b3);
    or  U5_3(x3, a3_and_nb3, na3_and_b3);
    
    // Calcula s3 = x3 XOR c3
    not U6_3(ncin3, c3);
    and U7_3(x_and_ncin3, x3, ncin3);
    not U8_3(nx3, x3);
    and U9_3(nx_and_cin3, nx3, c3);
    or  U10_3(s3, x_and_ncin3, nx_and_cin3);
    
    // Calcula cout = (a3 AND b3) OR (c3 AND x3)
    and U11_3(a3_and_b3, a3, b3);
    and U12_3(cin_and_x3, c3, x3);
    or  U13_3(cout, a3_and_b3, cin_and_x3);
    
endmodule
