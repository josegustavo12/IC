#!/usr/bin/env wish
package require Tk

# Cria a janela de mensagem principal
message .m -text {Hello Tcl!} -background white
pack .m -expand true -fill both -ipadx 100 -ipady 40

# Cria a barra de menu principal com uma entrada Help-About
menu .menubar
menu .menubar.help -tearoff 0
.menubar add cascade -label Help -menu .menubar.help -underline 0
.menubar.help add command -label {About Hello ...} \
    -accelerator F1 -underline 0 -command showAbout

# Define um procedimento - ação para Help-About
proc showAbout {} {
    tk_messageBox -message "Tcl/Tk\nHello Windows\nVersion 1.0" \
        -title {About Hello}
}

# Configura a janela principal
wm title . {Hello Foundation Application}
. configure -menu .menubar -width 200 -height 150
bind . {<Key-F1>} {showAbout}

# Inicia o loop de eventos
# (No 'wish', geralmente não é necessário adicionar 'mainloop', mas pode ser adicionado para garantir)
# mainloop
