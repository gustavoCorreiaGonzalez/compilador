# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# lexer.py
# Analisador sintático e geração de uma árvore sintática abstrata para a
#   linguagem T++
# Autor: Gustavo Correia Gonzalez
#-------------------------------------------------------------------------

from ply import yacc
from lexica import tokens

class Tree:

    def __init__(self, type_node, child=[], value=''):
        self.type = type_node
        self.child = child
        self.value = value

    def __str__(self):
        return self.type

    def __str__(self, level = 0):
        ret = "| " * level + self.type + "\n"
        level = level + 1
        for child in self.child:
            ret += child.__str__(level)
        return ret

precedence = (
    ('left', 'IGUALDADE', 'MAIOR', 'MAIORIGUAL', 'MENOR', 'MENORIGUAL'),
    ('left', 'SOMA', 'SUBTRACAO'),
    ('left', 'MULTIPLICACAO', 'DIVISAO'),
)

def p_programa(p):
    
    '''
    Programa : Declaracoes Programa 
             | Declaracoes
    '''
    
    if (len(p) == 3):
        p[0] = Tree('Programa_Global_Funcao_Principal', [p[1], p[2]])
    else:
        p[0] = Tree('Programa_Funcao_Principal', [p[1]])

def p_declaracoes(p):

    '''
    Declaracoes : Declaracao_Variavel
                | Funcao
    '''

    p[0] = Tree('Declaracoes', [p[1]])

def p_funcao(p):

    'Funcao : Tipo IDENTIFICADOR ABREPARENTES Conjunto_Parametros FECHAPARENTES Conjunto_Declaracoes FIM'    

    p[0] = Tree('Funcao', [p[1], p[4], p[6]], [p[2]])

def p_funcao_sem_declaracoes(p):

    'Funcao : Tipo IDENTIFICADOR ABREPARENTES Conjunto_Parametros FECHAPARENTES FIM'

    p[0] = Tree('Funcao_Sem_Declaracoes', [p[1], p[4]], [p[2]])

def p_declaracao_variavel(p):
    
    'Declaracao_Variavel : Tipo DOISPONTOS Variaveis'

    p[0] = Tree('Declaracao_Variavel', [p[1], p[3]])

def p_variaveis(p):

    '''
    Variaveis : Variaveis VIRGULA IDENTIFICADOR
              | IDENTIFICADOR 
    '''

    if(len(p) == 4):
        p[0] = Tree('Variaveis_Virgula', [p[1]], p[3])
    else:
        p[0] = Tree('Variaveis', [], p[1])

def p_conjunto_instrucoes(p):

    ''' 
    Conjunto_Parametros : Tipo DOISPONTOS IDENTIFICADOR VIRGULA Conjunto_Parametros 
                        | Tipo DOISPONTOS IDENTIFICADOR
                        | empty 
    '''

    if (len(p) == 6):
        p[0] = Tree('Conjunto_Parametros_Virgula_Instrucoes', [p[1], p[5]], [p[3]])
    elif (len(p) == 4):
        p[0] = Tree('Conjunto_Parametros', [p[1]], [p[3]])
    else:
        p[0] = Tree('Conjunto_Parametros_Empty', [])

def p_tipo(p):
    
    '''
    Tipo : INTEIRO
         | FLUTUANTE
    '''

    if p[1] == 'inteiro':
        p[0] = Tree('Tipo_Inteiro', [], [p[1]])
    elif p[1] == 'flutuante':
        p[0] = Tree('Tipo_Flutuante', [], [p[1]])

def p_conjunto_declaracoes(p):

    ''' 
    Conjunto_Declaracoes : Conjunto_Declaracoes Declaracao
                         | Declaracao 
    '''

    if (len(p) == 3):
        p[0] = Tree('Conjunto_Declaracoes_Declaracoes_Declaracao', [p[1], p[2]])
    else:
        p[0] = Tree('Conjunto_Declaracoes_Declaracao', [p[1]])

def p_declaracao(p):

    '''
    Declaracao : Declaracao_Se
               | Declaracao_Repita
               | Declaracao_Atribuicao
               | Declaracao_Leia
               | Declaracao_Escreva
               | Declaracao_Variavel
               | Declaracao_Retorno
    '''
    p[0] = Tree('Declaracao', [p[1]])

def p_declaracao_se(p):
    
    '''
    Declaracao_Se : SE Expressao_Comparacional ENTAO Conjunto_Declaracoes FIM
                  | SE Expressao_Comparacional ENTAO Conjunto_Declaracoes SENAO Conjunto_Declaracoes FIM
    '''

    if (len(p) == 6):
        p[0] = Tree('Declaracao_Se', [p[2], p[4]])
    else:
        p[0] = Tree('Declaracao_Senao', [p[2], p[4], p[6]])  

def p_declaracao_repita(p):

    'Declaracao_Repita : REPITA Conjunto_Declaracoes ATE Expressao_Comparacional'
    
    p[0] = Tree('Declaracao_Repita', [p[2], p[4]])

def p_declaracao_atribuicao(p):

    'Declaracao_Atribuicao : IDENTIFICADOR ATRIBUICAO Conjunto_Expressao'
    
    p[0] = Tree('Declaracao_Atribuicao', [p[3]], p[1])

def p_declaracao_leia(p):

    'Declaracao_Leia : LEIA ABREPARENTES IDENTIFICADOR FECHAPARENTES'
    
    p[0] = Tree('Declaracao_Leia', [], p[3])

def p_declaracao_escreva(p):

    'Declaracao_Escreva : ESCREVA ABREPARENTES Conjunto_Expressao FECHAPARENTES'
    
    p[0] = Tree('Declaracao_Escreva', [p[3]])

def p_declaracao_retorna(p):
    
    'Declaracao_Retorno : RETORNA ABREPARENTES Conjunto_Expressao FECHAPARENTES'
    
    p[0] = Tree('Declaracao_Retorno', [p[3]])

def p_conjunto_expressao(p):

    ''' 
    Conjunto_Expressao : Expressao_ID
                       | Expressao_Aritmetica
                       | Expressao_Comparacional
                       | Expressao_Parenteses
                       | Expressao_Numero
                       | Chama_Funcao
                       | Expressao_Unaria
    '''

    p[0] = Tree('Conjunto_Expressao', [p[1]])

def p_parametros(p):

    '''
    Parametros : Parametros VIRGULA Conjunto_Expressao
               | Conjunto_Expressao     
    '''

    if(len(p) == 4):
        p[0] = Tree('Parametros_Virgula', [p[1], p[3]])
    else:
        p[0] = Tree('Parametros', [p[1]])

def p_chama_funcao(p):

    '''
    Chama_Funcao : IDENTIFICADOR ABREPARENTES Parametros FECHAPARENTES
                 | IDENTIFICADOR ABREPARENTES FECHAPARENTES
    '''
        
    if(len(p) == 5):
        p[0] = Tree('Chama_Funcao', [p[3]], p[1])
    else:
        p[0] = Tree('Chama_Funcao_Vazia', [], p[1])

def p_expressoes_id(p):

    '''
    Expressao_ID : Expressao_ID VIRGULA IDENTIFICADOR
                 | IDENTIFICADOR 
    '''

    if(len(p) == 4):
        p[0] = Tree('Expressoes_ID_Virgula', [p[1]], p[3])
    else:
        p[0] = Tree('Expressoes_ID', [], p[1])

def p_expressao_aritmetica(p):

    '''
    Expressao_Aritmetica : Conjunto_Expressao SOMA Conjunto_Expressao
                         | Conjunto_Expressao SUBTRACAO Conjunto_Expressao
                         | Conjunto_Expressao MULTIPLICACAO Conjunto_Expressao
                         | Conjunto_Expressao DIVISAO Conjunto_Expressao
    '''

    p[0] = Tree('Expressao_Aritmetica', [p[1], p[3]])


def p_expressao_aritmetica_unaria(p):

    '''
    Expressao_Unaria : SOMA Conjunto_Expressao
                     | SUBTRACAO Conjunto_Expressao
    '''
    p[0] = Tree('Expressao_Unaria', [p[2]])


def p_expressao_comparacional(p):

    '''
    Expressao_Comparacional : Conjunto_Expressao MAIOR Conjunto_Expressao
                            | Conjunto_Expressao MENOR Conjunto_Expressao
                            | Conjunto_Expressao MAIORIGUAL Conjunto_Expressao
                            | Conjunto_Expressao MENORIGUAL Conjunto_Expressao
                            | Conjunto_Expressao IGUALDADE Conjunto_Expressao
    '''

    p[0] = Tree('Expressao_Aritmetica', [p[1], p[3]])

def p_expressao_parenteses(p):

    'Expressao_Parenteses : ABREPARENTES Conjunto_Expressao FECHAPARENTES'

    p[0] = Tree('Expressao_Parenteses', [p[2]], [p[1], p[3]])

def p_expressao_numero(p):

    'Expressao_Numero : NUMERO'

    p[0] = Tree('Expressao_Numero', [], p[1])

def p_empty(p):
    ' empty : '

def p_error(p):
    if p:
        print("Erro sintático: '%s', linha %d" % (p.value, p.lineno))
        exit(1)
    else:
        print('Erro sintático: definições incompletas!')
        exit(1)

if __name__ == '__main__':
    import sys
    parser = yacc.yacc(debug=True)
    code = open(sys.argv[1])
    print(parser.parse(code.read()))