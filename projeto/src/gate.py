from .DAlgebra import D_Value


class Gate:
    def __init__(self, id, type, input_gates, outputpin):
        self.id = id
        self.type = type
        self.input_gates = input_gates
        self.output_gates = []  # lista de portas conectadas à saída
        self.outputpin = outputpin
        self.value = D_Value.X  # inicia com um valor indefinido
        self.faulty = False  # flag para a falha
        self.fault_value = None

        if type == "input_pin" or type == "output_pin":  # define pino de entrada ou saída
            self.is_pin = True
        else:
            self.is_pin = False

        # Define a flag de inversion_parity para portas que invertem o sinal
        if type in ["NOT", "NAND", "NOR", "XNOR"]:
            self.inversion_parity = 1
        else:
            self.inversion_parity = 0

        # Define o valor não controlador (importante para SCOAP) conforme o tipo da porta
        if type in ["BUFF", "BUF", "NOT"]:
            self.non_controlling_value = D_Value.ONE
        elif type in ["OR", "NOR", "XOR", "XNOR"]:
            self.non_controlling_value = D_Value.ZERO
        elif type in ["AND", "NAND"]:
            self.non_controlling_value = D_Value.ONE

        self.explored = False  # controle de visitas em algoritmos recursivos

        # Distance Parameters
        self.PI_distance = 0
        self.PO_distance = 0

        # SCOAP Parameters
        self.CC0 = 0  # 0-controllability
        self.CC1 = 0  # 1-controllability
        self.CCb = 0  # observability

        self.is_zero_out_controllable = False
        self.is_one_out_controllable = False

        if self.type in ["AND", "NOR", "XNOR"]:
            self.is_one_out_controllable = False
            self.is_zero_out_controllable = True
        elif self.type in ["NOT", "BUFF", "BUF"]:
            self.is_one_out_controllable = True
            self.is_zero_out_controllable = True
        else:
            self.is_one_out_controllable = True
            self.is_zero_out_controllable = False

        return

    def evaluate(self):
        """
        Seleciona a função de avaliação apropriada para cada tipo de porta.
        """
        if self.type == "input_pin":  # valor já definido
            pass
        elif self.type == "output_pin":
            self.value = self.input_gates[0].value
        elif self.type == "AND":
            self.value = self.evaluate_and()
        elif self.type == "OR":
            self.value = self.evaluate_or()
        elif self.type == "XOR":
            self.value = self.evaluate_xor()
        elif self.type in ["BUFF", "BUF"]:
            self.value = self.evaluate_buff()
        elif self.type == "NOT":
            self.value = self.evaluate_not()
        elif self.type == "NAND":
            self.value = self.evaluate_nand()
        elif self.type == "NOR":
            self.value = self.evaluate_nor()
        elif self.type == "XNOR":
            self.value = self.evaluate_xnor()

        # Se a porta estiver marcada como com falha, ajusta o valor conforme a discrepância
        if self.faulty:
            tempval = [self.value.value[1], self.fault_value.value[1]]
            if tempval == [1, 0]:
                self.value = D_Value.D
            elif tempval == [0, 1]:
                self.value = D_Value.D_PRIME
            elif tempval == [0, 0]:
                self.value = D_Value.ZERO
            elif tempval == [1, 1]:
                self.value = D_Value.ONE
            elif "X" in tempval:
                self.value = D_Value.X

        return

    def evaluate_and(self):
        """
        Avalia uma porta AND com base nos valores das portas de entrada.
        
        Regras:
          - Se qualquer entrada for ZERO, retorna ZERO.
          - Se houver qualquer X, retorna X.
          - Se ambos D e D_PRIME estiverem presentes, retorna ZERO.
          - Se somente D estiver presente e todas as entradas forem ONE ou D, retorna D.
          - Se somente D_PRIME estiver presente e todas as entradas forem ONE ou D_PRIME, retorna D_PRIME.
          - Caso contrário, retorna ONE.
        """
        values = [g.value for g in self.input_gates]

        if D_Value.ZERO in values:
            return D_Value.ZERO

        if D_Value.X in values:
            return D_Value.X

        has_D = D_Value.D in values
        has_Dp = D_Value.D_PRIME in values

        if has_D and has_Dp:
            return D_Value.ZERO

        if has_D:
            if all(v in (D_Value.ONE, D_Value.D) for v in values):
                return D_Value.D

        if has_Dp:
            if all(v in (D_Value.ONE, D_Value.D_PRIME) for v in values):
                return D_Value.D_PRIME

        return D_Value.ONE

    def evaluate_or(self):
        """
        Avalia uma porta OR com base nos valores das portas de entrada.
        
        Regras:
          - Se qualquer entrada for ONE, retorna ONE.
          - Se houver qualquer X, retorna X.
          - Se ambos D e D_PRIME estiverem presentes, retorna ONE.
          - Se somente D estiver presente e todas as entradas forem ZERO ou D, retorna D.
          - Se somente D_PRIME estiver presente e todas as entradas forem ZERO ou D_PRIME, retorna D_PRIME.
          - Caso contrário, retorna ZERO.
        """
        values = [g.value for g in self.input_gates]

        if D_Value.ONE in values:
            return D_Value.ONE

        if D_Value.X in values:
            return D_Value.X

        has_D = D_Value.D in values
        has_Dp = D_Value.D_PRIME in values

        if has_D and has_Dp:
            return D_Value.ONE

        if has_D:
            if all(v in (D_Value.ZERO, D_Value.D) for v in values):
                return D_Value.D

        if has_Dp:
            if all(v in (D_Value.ZERO, D_Value.D_PRIME) for v in values):
                return D_Value.D_PRIME

        return D_Value.ZERO

    def evaluate_xor(self):
        """
        Avalia uma porta XOR com base nos valores das portas de entrada.
        
        Regras:
          - Se qualquer entrada for X, retorna X.
          - Se não houver discrepâncias (nem D nem D_PRIME), calcula a paridade dos ONE's.
          - Se ambos D e D_PRIME estiverem presentes, retorna X (ou pode-se definir outro comportamento).
          - Se somente D estiver presente, propaga D.
          - Se somente D_PRIME estiver presente, propaga D_PRIME.
        """
        values = [g.value for g in self.input_gates]

        if D_Value.X in values:
            return D_Value.X

        if D_Value.D not in values and D_Value.D_PRIME not in values:
            one_count = values.count(D_Value.ONE)
            return D_Value.ONE if one_count % 2 == 1 else D_Value.ZERO

        if D_Value.D in values and D_Value.D_PRIME in values:
            return D_Value.X

        if D_Value.D in values:
            return D_Value.D

        if D_Value.D_PRIME in values:
            return D_Value.D_PRIME

        return D_Value.X

    def evaluate_not(self):
        """
        Avalia uma porta NOT.
        
        Regras:
          - Se a entrada é D, retorna D_PRIME.
          - Se a entrada é D_PRIME, retorna D.
          - Se a entrada é ONE, retorna ZERO.
          - Se a entrada é ZERO, retorna ONE.
          - Se a entrada é X, retorna X.
        """
        values = [g.value for g in self.input_gates]
        input_val = values[0]
        if input_val == D_Value.D:
            return D_Value.D_PRIME
        elif input_val == D_Value.D_PRIME:
            return D_Value.D
        elif input_val == D_Value.ONE:
            return D_Value.ZERO
        elif input_val == D_Value.ZERO:
            return D_Value.ONE
        else:
            return D_Value.X

    def evaluate_buff(self):
        """
        Avalia uma porta BUFF (buffer), que apenas repassa o valor da entrada.
        """
        values = [g.value for g in self.input_gates]
        return values[0]

    def evaluate_nand(self):
        """
        Avalia uma porta NAND criando internamente uma porta AND e, em seguida, uma porta NOT.
        """
        and_gate = Gate("AND", "AND", self.input_gates, None)
        and_gate.evaluate()
        not_gate = Gate("NOT", "NOT", [and_gate], None)
        not_gate.evaluate()
        return not_gate.value

    def evaluate_nor(self):
        """
        Avalia uma porta NOR criando internamente uma porta OR e, em seguida, uma porta NOT.
        """
        or_gate = Gate("OR", "OR", self.input_gates, None)
        or_gate.evaluate()
        not_gate = Gate("NOT", "NOT", [or_gate], None)
        not_gate.evaluate()
        return not_gate.value

    def evaluate_xnor(self):
        """
        Avalia uma porta XNOR criando internamente uma porta XOR e, em seguida, uma porta NOT.
        """
        xor_gate = Gate("XOR", "XOR", self.input_gates, None)
        xor_gate.evaluate()
        not_gate = Gate("NOT", "NOT", [xor_gate], None)
        not_gate.evaluate()
        return not_gate.value

    def calculate_CC0(self):
        res = 0
        if self.type == "AND":
            res = min(g.CC0 for g in self.input_gates) + 1
        elif self.type == "NAND":
            res = sum(g.CC1 for g in self.input_gates) + 1
        elif self.type == "OR":
            res = sum(g.CC0 for g in self.input_gates) + 1
        elif self.type == "NOR":
            res = min(g.CC1 for g in self.input_gates) + 1
        elif self.type == "XOR":  # suporte para duas entradas
            res = min(
                self.input_gates[0].CC0 + self.input_gates[1].CC0,
                self.input_gates[0].CC1 + self.input_gates[1].CC1,
            ) + 1
        elif self.type == "XNOR":  # suporte para duas entradas
            res = min(
                self.input_gates[0].CC1 + self.input_gates[1].CC0,
                self.input_gates[0].CC0 + self.input_gates[1].CC1,
            ) + 1
        elif self.type == "NOT":
            res = self.input_gates[0].CC1 + 1
        elif self.type in ["BUFF", "BUF"]:
            res = self.input_gates[0].CC0 + 1
        elif self.type == "input_pin":
            res = 1
        elif self.type == "output_pin":
            res = min(g.CC0 for g in self.input_gates)
        self.CC0 = res

    def calculate_CC1(self):
        res = -1
        if self.type == "AND":
            res = sum(g.CC1 for g in self.input_gates) + 1
        elif self.type == "NAND":
            res = min(g.CC0 for g in self.input_gates) + 1
        elif self.type == "OR":
            res = min(g.CC1 for g in self.input_gates) + 1
        elif self.type == "NOR":
            res = sum(g.CC0 for g in self.input_gates) + 1
        elif self.type == "XOR":
            res = min(
                self.input_gates[0].CC0 + self.input_gates[1].CC1,
                self.input_gates[0].CC1 + self.input_gates[1].CC0,
            ) + 1
        elif self.type == "XNOR":
            res = min(
                self.input_gates[0].CC0 + self.input_gates[1].CC0,
                self.input_gates[0].CC1 + self.input_gates[1].CC1,
            ) + 1
        elif self.type == "NOT":
            res = self.input_gates[0].CC0 + 1
        elif self.type in ["BUFF", "BUF"]:
            res = self.input_gates[0].CC1 + 1
        elif self.type == "input_pin":
            res = 1
        elif self.type == "output_pin":
            res = min(g.CC1 for g in self.input_gates)
        self.CC1 = res

    def calculate_CCb(self):
        res = -1
        CCb_output = 0
        if self.output_gates:
            CCb_output = min(g.CCb for g in self.output_gates)
        if self.type == "AND":
            res = CCb_output + sum(g.CC1 for g in self.input_gates) + 1
        elif self.type == "NAND":
            res = CCb_output + sum(g.CC1 for g in self.input_gates) + 1
        elif self.type == "OR":
            res = CCb_output + sum(g.CC0 for g in self.input_gates) + 1
        elif self.type == "NOR":
            res = CCb_output + sum(g.CC0 for g in self.input_gates) + 1
        elif self.type == "XOR":  # suporte futuro para XOR
            pass
        elif self.type == "XNOR":  # suporte futuro para XNOR
            pass
        elif self.type == "NOT":
            res = CCb_output + 1
        elif self.type in ["BUFF", "BUF"]:
            res = CCb_output + 1
        elif self.type == "input_pin":
            res = CCb_output
        elif self.type == "output_pin":
            res = 0
        self.CCb = res

    def check_controllable_value(self, value):
        ret = False
        if value == D_Value.ONE:
            ret = self.is_one_out_controllable
        elif value == D_Value.ZERO:
            ret = self.is_zero_out_controllable
        return ret

    def get_easiest_to_satisfy_gate(self, objective_value):
        easiest_gate = None
        easiest_value = 0
        for gate in self.input_gates:
            if objective_value == D_Value.ZERO:
                if gate.CC0 < easiest_value:
                    easiest_gate = gate
                    easiest_value = gate.CC0
            elif objective_value == D_Value.ONE:
                if gate.CC1 < easiest_value:
                    easiest_gate = gate
                    easiest_value = gate.CC1
        return easiest_gate

    def get_hardest_to_satisfy_gate(self, objective_value):
        hardest_gate = None
        hardest_value = 0
        for gate in self.input_gates:
            if objective_value == D_Value.ZERO:
                if gate.CC0 > hardest_value:
                    hardest_gate = gate
                    hardest_value = gate.CC0
            elif objective_value == D_Value.ONE:
                if gate.CC1 > hardest_value:
                    hardest_gate = gate
                    hardest_value = gate.CC1
        return hardest_gate
