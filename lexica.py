# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# lexica.py
# Analisador léxico para a linguagem T++
# Autor: Gustavo Correia Gonzalez
#-------------------------------------------------------------------------

import ply.lex as lex

# class Lexer:

#     def __init__(self):
#         self.lexica = lex.lex(debug=False, module=self, optimize=False)

keywords = {
    u'se': 'SE',
    u'então': 'ENTAO',
    u'senão': 'SENAO',
    u'fim': 'FIM',
    u'repita': 'REPITA',
    u'flutuante': 'FLUTUANTE',
    u'até': 'ATE',
    u'leia': 'LEIA',
    u'escreva': 'ESCREVA',
    u'inteiro': 'INTEIRO',
    u'principal': 'PRINCIPAL',
    u'retorna': 'RETORNA',
    u'vazio': 'VAZIO',
}

tokens = [
    'N_FLUTUANTE',
    'N_INTEIRO',
    'SOMA',
    'SUBTRACAO',
    'MULTIPLICACAO',
    'DIVISAO',
    'IGUALDADE',
    'VIRGULA',
    'ATRIBUICAO',
    'MENOR',
    'MAIOR',
    'MENORIGUAL',
    'MAIORIGUAL',
    'ABREPARENTES',
    'FECHAPARENTES',
    'DOISPONTOS',
    'IDENTIFICADOR'
] + list(keywords.values())

t_SOMA = r'\+'
t_SUBTRACAO = r'\-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'/'
t_IGUALDADE = r'='
t_VIRGULA = r','
t_ATRIBUICAO = r':='
t_MENOR = r'<'
t_MAIOR = r'>'
t_MENORIGUAL = r'<='
t_MAIORIGUAL = r'>='
t_ABREPARENTES = r'\('
t_FECHAPARENTES = r'\)'
t_DOISPONTOS = r':'
#t_NUMERO = r'[+-]?[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?'

def t_N_FLUTUANTE(t):
    r'\d+(\.\d+)?(e(\+|\-)?(\d+))?'
    t.value = float(t.value)
    return t

def t_N_INTEIRO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Zá-ũÁ-Ũ][a-zA-Zá-ũÁ-Ũ0-9]*'
    t.type = keywords.get(t.value, 'IDENTIFICADOR')
    return t

def t_COMMENTARIO(t):
    r'{[^\{^\}]*}'

def t_NOVALINHA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Item ilegal: '%s', linha %d, coluna %d" % (t.value[0],
                                                      t.lineno, t.lexpos))
    t.lexer.skip(1)

def test(code):
    lex.input(code)
    while True:
        t = lex.token()
        if not t:
            break
        print(t)

lexico = lex.lex()

if __name__ == '__main__':
    import sys
    code = open(sys.argv[1])
    lex.input(code.read())
    while True:
        tok = lex.token()
        if not tok:
            break
        print(tok)