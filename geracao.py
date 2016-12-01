from llvmlite import ir, binding
from semantica import Semantica
from sintatica import *
from subprocess import call
from sys import exit
import os

class geracao:

	def __init__(self, code):
		semantica = Semantica(code.read())
		semantica.Principal()
		self.semantica = semantica.arvore
		self.construtor = None
		self.func = None
		self.simbolos = semantica.simbolos
		self.phi = False
		self.tipo_variavel = None
		self.escopo = 'global'
		self.modulo = ir.Module('programa')
		self.escrevaFlutuante = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), [ir.FloatType()]), 'escrevaFlutuante')
		self.escrevaInteiro = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), [ir.IntType(32)]), 'escrevaInteiro')
		self.leiaFlutuante = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), []), 'leiaFlutuante')
		self.leiaInteiro = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), []), 'leiaInteiro')

		self.ger_programa(self.semantica)
		print(self.modulo)

# def p_programa(p):
	
#     '''
#     Programa : Programa Declaracoes  
#              | Declaracoes
#     '''
	
#     if (len(p) == 3):
#         p[0] = tree('Programa_Declaracoes_Programa', [p[1], p[2]])
#     else:
#         p[0] = tree('Programa_Declaracoes', [p[1]])

	def ger_programa(self, no):
		if no.type == 'Programa_Declaracoes_Programa':
			self.ger_programa(no.child[0])
			self.ger_declaracoes(no.child[1])
		else:
			self.ger_declaracoes(no.child[0])

# def p_declaracoes(p):

#     '''
#     Declaracoes : Declaracao_Variavel
#                 | Funcao
#     '''

#     p[0] = tree('Declaracoes', [p[1]])

	def ger_declaracoes(self, no):
		if no.child[0].type == 'Declaracao_Variavel':
			self.ger_declaracao_variavel(no.child[0])
		else:
			self.ger_funcao(no.child[0])

# def p_funcao(p):

#     'Funcao : Tipo IDENTIFICADOR ABREPARENTES Conjunto_Parametros FECHAPARENTES Conjunto_Declaracoes FIM'    

#     p[0] = tree('Funcao', [p[1], p[4], p[6]], [p[2]])

# def p_funcao_sem_declaracoes(p):

#     'Funcao : Tipo IDENTIFICADOR ABREPARENTES Conjunto_Parametros FECHAPARENTES FIM'

#     p[0] = tree('Funcao_Sem_Declaracoes', [p[1], p[4]], [p[2]])

	def ger_funcao(self, no):
		self.escopo = no.value[0]
		tipo = self.ger_get_tipo(no.child[0])

		lista_parametros = self.ger_conjunto_parametros(no.child[1])

		if no.value[0] == 'principal':
			função = ir.FunctionType(tipo, [lista_parametros[i][0] for i in range(0, len(lista_parametros))])
			self.func = ir.Function(self.modulo, função, name = 'main')
			bloco = self.func.append_basic_block('entry')
			self.construtor = ir.IRBuilder(bloco)
		else:
			função = ir.FunctionType(tipo, [lista_parametros[i][0] for i in range(0, len(lista_parametros))])
			self.func = ir.Function(self.modulo, função, name = no.value[0])
			bloco = self.func.append_basic_block('entry')
			self.construtor = ir.IRBuilder(bloco)

		for i, param in enumerate(lista_parametros):
			self.func.args[i].name = param[1]
			self.simbolos[self.escopo + '@' + param[1]][2] = self.construtor.alloca(param[0], name = param[1])
			self.construtor.store(self.func.args[i], self.simbolos[self.escopo + '@' + param[1]][2])

		if no.type == 'Funcao':
			self.ger_conjunto_declaracoes(no.child[2])

		self.escopo = 'global'

# def p_declaracao_variavel(p):
	
#     'Declaracao_Variavel : Tipo DOISPONTOS Variaveis'

#     p[0] = tree('Declaracao_Variavel', [p[1], p[3]])

	def ger_declaracao_variavel(self, no):
		tipo = self.ger_get_tipo(no.child[0])

		lista_variaveis = self.ger_variaveis(no.child[1])

		if self.escopo == 'global':
			for i in enumerate(lista_variaveis):
				self.simbolos[self.escopo + '@' + i[1]][2] = ir.GlobalVariable(self.modulo, tipo, i[1])
		else:
			for i in enumerate(lista_variaveis):
				self.simbolos[self.escopo + '@' + i[1]][2] = self.construtor.alloca(tipo, size=None, name=i[1])
			
			return self.simbolos[self.escopo + '@' + i[1]][2]

	def ger_get_tipo(self, no):
		if no.value[0] == 'inteiro':
			return ir.IntType(32)

		return ir.FloatType()

# def p_variaveis(p):

#     '''
#     Variaveis : Variaveis VIRGULA IDENTIFICADOR
#               | IDENTIFICADOR 
#     '''

#     if(len(p) == 4):
#         p[0] = tree('Variaveis_Virgula', [p[1]], p[3])
#     else:
#         p[0] = tree('Variaveis', [], p[1])

	def ger_variaveis(self, no):
		lista_variaveis = []

		if no.type == 'Variaveis_Virgula':
			while(no.type == 'Variaveis_Virgula'):
				lista_variaveis.append(no.value)
				
				no = no.child[0]

		if no.type == 'Variaveis':
			lista_variaveis.append(no.value)

		return lista_variaveis


# def p_conjunto_instrucoes(p):

#     ''' 
#     Conjunto_Parametros : Tipo DOISPONTOS IDENTIFICADOR VIRGULA Conjunto_Parametros 
#                         | Tipo DOISPONTOS IDENTIFICADOR
#                         | empty 
#     '''

#     if (len(p) == 6):
#         p[0] = tree('Conjunto_Parametros_Virgula_Instrucoes', [p[1], p[5]], [p[3]])
#     elif (len(p) == 4):
#         p[0] = tree('Conjunto_Parametros', [p[1]], [p[3]])
#     else:
#         p[0] = tree('Conjunto_Parametros_Empty', [])

	def ger_conjunto_parametros(self, no):
		variaveis = []

		if len(no.child) > 0:
			tipo = self.ger_get_tipo(no.child[0])
			variaveis.append((tipo,no.value[0]))

			if len(no.child) > 1:
				variaveis = variaveis + self.ger_conjunto_parametros(no.child[1])

		return variaveis

# def p_tipo(p):
	
#     '''
#     Tipo : INTEIRO
#          | FLUTUANTE
#     '''

#     if p[1] == 'inteiro':
#         p[0] = tree('Tipo_Inteiro', [], [p[1]])
#     elif p[1] == 'flutuante':
#         p[0] = tree('Tipo_Flutuante', [], [p[1]])

# def p_conjunto_declaracoes(p):

#     ''' 
#     Conjunto_Declaracoes : Conjunto_Declaracoes Declaracao
#                          | Declaracao 
#     '''

#     if (len(p) == 3):
#         p[0] = tree('Conjunto_Declaracoes_Declaracoes_Declaracao', [p[1], p[2]])
#     else:
#         p[0] = tree('Conjunto_Declaracoes_Declaracao', [p[1]])

	def ger_conjunto_declaracoes(self, no):
		if len(no.child) > 1:
			self.ger_conjunto_declaracoes(no.child[0])
			self.ger_declaracao(no.child[1])
		else:
			self.ger_declaracao(no.child[0])

# def p_declaracao(p):

#     '''
#     Declaracao : Declaracao_Se
#                | Declaracao_Repita
#                | Declaracao_Atribuicao
#                | Declaracao_Leia
#                | Declaracao_Escreva
#                | Declaracao_Variavel
#                | Declaracao_Retorno
#                | Chama_Funcao
#     '''
#     p[0] = tree('Declaracao', [p[1]])

	def ger_declaracao(self, no):
		# if no.child[0].type == 'Declaracao_Se':
		# 	self.Declaracao_Se(no.child[0])
		
		# if no.child[0].type == 'Declaracao_Repita':
		# 	self.Declaracao_Repita(no.child[0])
		
		if no.child[0].type == 'Declaracao_Atribuicao':
			self.ger_declaracao_atribuicao(no.child[0])

		if no.child[0].type == 'Declaracao_Leia':
			self.ger_declaracao_leia(no.child[0])
		
		if no.child[0].type == 'Declaracao_Escreva':
			self.ger_declaracao_escreva(no.child[0])

		if no.child[0].type == 'Declaracao_Variavel':
			self.ger_declaracao_variavel(no.child[0])

		if no.child[0].type == 'Declaracao_Retorno':
			self.ger_declaracao_retorna(no.child[0])
			
		if no.child[0].type == 'Chama_Funcao' or no.child[0].type == 'Chama_Funcao_Vazia':
			self.ger_chama_funcao(no.child[0])
		

# def p_declaracao_se(p):
	
#     '''
#     Declaracao_Se : SE Expressao_Comparacional ENTAO Conjunto_Declaracoes FIM
#                   | SE Expressao_Comparacional ENTAO Conjunto_Declaracoes SENAO Conjunto_Declaracoes FIM
#     '''

#     if (len(p) == 6):
#         p[0] = tree('Declaracao_Se', [p[2], p[4]])
#     else:
#         p[0] = tree('Declaracao_Senao', [p[2], p[4], p[6]])  

	def ger_declaracao_se(self, no):
		pass
		# formula a condição
		# cond = self.ger_conjunto_declaracoes(no.child[0])
        # adiciona os blocos básicos
        # entao_block = self.func.append_basic_block('then')
        # senao_block = self.func.append_basic_block('else')
        # merge_block = self.func.append_basic_block('ifcont')

# def p_declaracao_repita(p):

#     'Declaracao_Repita : REPITA Conjunto_Declaracoes ATE Expressao_Comparacional'
	
#     p[0] = tree('Declaracao_Repita', [p[2], p[4]])

# def p_declaracao_atribuicao(p):

#     'Declaracao_Atribuicao : IDENTIFICADOR ATRIBUICAO Conjunto_Expressao'
	
#     p[0] = tree('Declaracao_Atribuicao', [p[3]], p[1])

	
	def ger_declaracao_atribuicao(self, no):
		if (self.escopo + '@' + no.value) in self.simbolos.keys():
			self.tipo_variavel = self.simbolos[self.escopo + '@' + no.value][1]
		else:
			self.tipo_variavel = self.simbolos['global@' + no.value][1]

		resultado = self.ger_conjunto_expressao(no.child[0])

		if (self.escopo + '@' + no.value) in self.simbolos.keys():
			self.construtor.store(resultado, self.simbolos[self.escopo + '@' + no.value][2])
		else:
			self.construtor.store(resultado, self.simbolos['global@' + no.value][2])

		# olhar aqui depois
		self.tipo_variavel = None

# def p_declaracao_leia(p):

#     'Declaracao_Leia : LEIA ABREPARENTES IDENTIFICADOR FECHAPARENTES'
	
#     p[0] = tree('Declaracao_Leia', [], p[3])

	def ger_declaracao_leia(self, no):
		if self.escopo + '@' + no.value[0] in self.simbolos.keys():
			if self.simbolos[self.escopo + '@' + no.value[0]][1] == 'inteiro':
				valor = self.construtor.call(self.leiaInteiro, [])
			else:
				valor = self.construtor.call(self.leiaFlutuante, [])
		else:
			if self.simbolos['global@' + no.value[0]][1] == 'inteiro':
				valor = self.construtor.call(self.leiaInteiro, [])
			else:
				valor = self.construtor.call(self.leiaFlutuante, [])
		return self.construtor.store(valor, self.simbolos[self.escopo + '@' + no.value[0]][2])

# def p_declaracao_escreva(p):

#     'Declaracao_Escreva : ESCREVA ABREPARENTES Conjunto_Expressao FECHAPARENTES'
	
#     p[0] = tree('Declaracao_Escreva', [p[3]])

	def ger_declaracao_escreva(self, no):
		expressão = self.ger_conjunto_expressao(no.child[0])

		print(expressão)

		if str(expressão).split(' ')[0] == 'i32':
			return self.construtor.call(self.escrevaInteiro, [expressão])
		elif str(expressão).split(' ')[3] == 'i32,':
			return self.construtor.call(self.escrevaInteiro, [expressão])
		if str(expressão).split(' ')[0] == 'float':
			return self.construtor.call(self.escrevaFlutuante, [expressão])	



# def p_declaracao_retorna(p):
	
#     'Declaracao_Retorno : RETORNA ABREPARENTES Conjunto_Expressao FECHAPARENTES'
	
#     p[0] = tree('Declaracao_Retorno', [p[3]])

	def ger_declaracao_retorna(self, no):
		self.tipo_variavel = self.simbolos[self.escopo][1]

		expressão = self.ger_conjunto_expressao(no.child[0])
		
		if self.phi:
			return expressão
		
		return self.construtor.ret(expressão)
		

# def p_conjunto_expressao(p):

#     ''' 
#     Conjunto_Expressao : Expressao_ID
#                        | Expressao_Aritmetica
#                        | Expressao_Comparacional
#                        | Expressao_Parenteses
#                        | Expressao_Numero
#                        | Chama_Funcao
#                        | Expressao_Unaria
#     '''

#     p[0] = tree('Conjunto_Expressao', [p[1]])

	def ger_conjunto_expressao(self, no, sinal=''):
		if no.child[0].type == 'Expressoes_ID' or no.child[0].type == 'Expressoes_ID_Virgula':
			return self.ger_expressao_id(no.child[0])
		
		if no.child[0].type == 'Expressao_Aritmetica':
			return self.ger_expressao_aritmetica(no.child[0])
		
		if no.child[0].type == 'Expressao_Comparacional':
			return self.ger_expressao_comparacional(no.child[0])
		
		if no.child[0].type == 'Expressao_Parenteses':
			return self.ger_expressao_parenteses(no.child[0])
		
		if no.child[0].type == 'Expressao_Numero':
			return self.ger_expressao_numero(no.child[0], sinal)

		if no.child[0].type == 'Chama_Funcao':
			return self.ger_chama_funcao(no.child[0])

		if no.child[0].type == 'Expressao_Unaria':
			return self.ger_expressao_unaria(no.child[0])

# def p_parametros(p):

#     '''
#     Parametros : Parametros VIRGULA Conjunto_Expressao
#                | Conjunto_Expressao     
#     '''
#     if(len(p) == 4):
#         p[0] = tree('Parametros_Virgula', [p[1], p[3]])
#     else:
#         p[0] = tree('Parametros', [p[1]])

	def ger_parametros(self, no):
		lista_parametros = []

		if len(no.child) > 1:
			lista_parametros.append(self.ger_conjunto_expressao(no.child[1]))
			lista_parametros = lista_parametros + self.ger_parametros(no.child[0])
		elif len(no.child) == 1:
			lista_parametros.append(self.ger_conjunto_expressao(no.child[0]))

		return lista_parametros

# def p_chama_funcao(p):

#     '''
#     Chama_Funcao : IDENTIFICADOR ABREPARENTES Parametros FECHAPARENTES
#                  | IDENTIFICADOR ABREPARENTES FECHAPARENTES
#     '''
		
#     if(len(p) == 5):
#         p[0] = tree('Chama_Funcao', [p[3]], p[1])
#     else:
#         p[0] = tree('Chama_Funcao_Vazia', [], p[1])

	def ger_chama_funcao(self, no):
		lista_parametros = []

		if no.type != 'Chama_Funcao_Vazia':
			lista_parametros = self.ger_parametros(no.child[0])

		funcao = self.modulo.get_global(no.value)
		tipo = self.simbolos[no.value][2]

		return self.construtor.call(funcao,lista_parametros[::-1])



# def p_expressoes_id(p):

#     'Expressao_ID : IDENTIFICADOR'

#     p[0] = tree('Expressoes_ID', [], p[1])

	def ger_expressao_id(self, no):
		if (self.escopo + '@' + no.value) in self.simbolos.keys():
			if self.tipo_variavel == self.simbolos[self.escopo + '@' + no.value][1]:
				return self.construtor.load(self.simbolos[self.escopo + '@' + no.value][2])
			else:
				valor = self.construtor.load(self.simbolos[self.escopo + '@' + no.value][2])
				if self.tipo_variavel == 'inteiro':
					return	self.construtor.fptosi(valor, ir.IntType(32))
				else:
					return	self.construtor.sitofp(valor, ir.FloatType())
		else:
			if self.tipo_variavel == self.simbolos['global@' + no.value][1]:
				valor = self.construtor.load(self.simbolos['global@' + no.value][2])
				if self.tipo_variavel == 'inteiro':
					return	self.construtor.fptosi(valor, ir.IntType(32))
				else:
					return	self.construtor.sitofp(valor, ir.FloatType())

# def p_expressao_aritmetica(p):

#     '''
#     Expressao_Aritmetica : Conjunto_Expressao SOMA Conjunto_Expressao
#                          | Conjunto_Expressao SUBTRACAO Conjunto_Expressao
#                          | Conjunto_Expressao MULTIPLICACAO Conjunto_Expressao
#                          | Conjunto_Expressao DIVISAO Conjunto_Expressao
#     '''

#     p[0] = tree('Expressao_Aritmetica', [p[1], p[3]], p[2])

	def ger_expressao_aritmetica(self, no):
		esquerda = self.ger_conjunto_expressao(no.child[0])
		direita = self.ger_conjunto_expressao(no.child[1])

		print(self.tipo_variavel)

		if self.tipo_variavel == 'inteiro':
			if no.value == '+':
				return self.construtor.add(esquerda, direita, name='add')
			elif no.value == '-':
				return self.construtor.sub(esquerda, direita, name='sub')
			elif no.value == '*':
				return self.construtor.mul(esquerda, direita, name='mul')
			else:
				return self.construtor.sdiv(esquerda, direita, name='div')
		else:
			if no.value == '+':
				return self.construtor.fadd(esquerda, direita, name='fadd')
			elif no.value == '-':
				return self.construtor.fsub(esquerda, direita, name='fsub')
			elif no.value == '*':
				return self.construtor.fmul(esquerda, direita, name='fmul')
			else:
				return self.construtor.fdiv(esquerda, direita, name='fdiv')

# def p_expressao_aritmetica_unaria(p):

#     '''
#     Expressao_Unaria : SOMA Conjunto_Expressao
#                      | SUBTRACAO Conjunto_Expressao
#     '''
#     p[0] = tree('Expressao_Unaria', [p[2]])

	def ger_expressao_unaria(self, no):
		return self.ger_conjunto_expressao(no.child[0],sinal = no.value)

# def p_expressao_comparacional(p):

#     '''
#     Expressao_Comparacional : Conjunto_Expressao MAIOR Conjunto_Expressao
#                             | Conjunto_Expressao MENOR Conjunto_Expressao
#                             | Conjunto_Expressao MAIORIGUAL Conjunto_Expressao
#                             | Conjunto_Expressao MENORIGUAL Conjunto_Expressao
#                             | Conjunto_Expressao IGUALDADE Conjunto_Expressao
#     '''
#     p[0] = tree('Expressao_Comparacional', [p[1], p[3]])

	def ger_expressao_comparacional(self, no):
		esquerda = self.ger_conjunto_expressao(no.child[0])
		direita = self.ger_conjunto_expressao(no.child[1])

		if self.tipo_variavel == 'inteiro':
			valor = self.construtor.icmp_signed(no.value, esquerda, direita, name='comparacao') 
			return self.construtor.trunc(valor, ir.IntType(32), name='trunc int')
		else:
			valor = self.construtor.fcmp_ordered(no.value, esquerda, direita, name='comparacao')
			return self.construtor.trunc(valor, ir.FloatType(), name='trunc float')

# def p_expressao_parenteses(p):

#     'Expressao_Parenteses : ABREPARENTES Conjunto_Expressao FECHAPARENTES'

#     p[0] = tree('Expressao_Parenteses', [p[2]], [p[1], p[3]])

	def ger_expressao_parenteses(self, no):
		self.ger_conjunto_expressao(no.child[0])


# def p_expressao_numero(p):

#     'Expressao_Numero : NUMERO'

#     p[0] = tree('Expressao_Numero', [], p[1])

	def ger_expressao_numero(self, no, sinal=''):
		teste = no.value

		if sinal == '-':
			teste = float(no.value) * -1

		if self.tipo_variavel == 'inteiro' and type(teste) == float:
			valor = ir.Constant(ir.FloatType(), teste)

			return self.construtor.fptosi(valor, ir.IntType(32))

		if self.tipo_variavel == 'flutuante' and type(teste) == int:
			valor = ir.Constant(ir.IntType(32), teste)

			return self.construtor.sitofp(valor, ir.FloatType())

		if type(teste) == int:
			return ir.Constant(ir.IntType(32), teste)
		else:
			return ir.Constant(ir.FloatType(), teste)

if __name__ == '__main__':
	import sys
	code = open(sys.argv[1])
	codigo = geracao(code)
	out = open('builder/program.ll', 'w')
	out.write(str(codigo.modulo))
	out.close()

	print("Compilando...")
	call("llc-3.7 builder/program.ll --mtriple \"x86_64-pc-linux-gnu\"", shell=True)
	call("gcc -c builder/program.s", shell=True)
	call("gcc -o builder/resultado program.o builder/leiaEscreva.o", shell=True)
	call("builder/./resultado", shell=True)
	print("Pronto.")