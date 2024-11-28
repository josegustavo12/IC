#!/usr/bin/env tclsh

# quase hello world do tcl

# Solicita o nome do usuário
puts -nonewline "Digite seu nome: "
# imprime imediatamente
flush stdout 
# pega o valor e guarda na variavel nome
gets stdin nome

# Cumprimenta o usuário
puts "Olá, $nome! Bem-vindo ao Tcl."
