import re

"""
Validador de CPF
"""


def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = ((soma * 10) % 11) % 10
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = ((soma * 10) % 11) % 10
    return dig1 == int(cpf[9]) and dig2 == int(cpf[10])


"""
Validador de CNPJ
"""


def validar_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1
    soma1 = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    dig1 = 11 - soma1 % 11
    dig1 = dig1 if dig1 < 10 else 0
    soma2 = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    dig2 = 11 - soma2 % 11
    dig2 = dig2 if dig2 < 10 else 0
    return dig1 == int(cnpj[12]) and dig2 == int(cnpj[13])


"""
Validador de CPF ou CNPJ
"""


def validar_cpf_cnpj(valor: str) -> bool:
    return validar_cpf(valor) or validar_cnpj(valor)
