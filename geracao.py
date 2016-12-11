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
		self.block_atual = None
		self.retorno = False
		self.guarda_retorno = None
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

	def ger_programa(self, node):
		if node.type == 'Programa_Declaracoes_Programa':
			self.ger_programa(node.child[0])
			self.ger_declaracoes(node.child[1])
		else:
			self.ger_declaracoes(node.child[0])

# def p_declaracoes(p):

#     '''
#     Declaracoes : Declaracao_Variavel
#                 | Funcao
#     '''

#     p[0] = tree('Declaracoes', [p[1]])

	def ger_declaracoes(self, node):
		if node.child[0].type == 'Declaracao_Variavel':
			self.ger_declaracao_variavel(node.child[0])
		else:
			self.ger_funcao(node.child[0])

# def p_funcao(p):

#     'Funcao : Tipo IDENTIFICADOR ABREPARENTES Conjunto_Parametros FECHAPARENTES Conjunto_Declaracoes FIM'    

#     p[0] = tree('Funcao', [p[1], p[4], p[6]], [p[2]])

# def p_funcao_sem_declaracoes(p):

#     'Funcao : Tipo IDENTIFICADOR ABREPARENTES Conjunto_Parametros FECHAPARENTES FIM'

#     p[0] = tree('Funcao_Sem_Declaracoes', [p[1], p[4]], [p[2]])

	def ger_funcao(self, node):
		self.retorno = False
		self.escopo = node.value[0]
		tipo = self.ger_get_tipo(node.child[0])

		lista_parametros = self.ger_conjunto_parametros(node.child[1])

		if node.value[0] == 'principal':
			função = ir.FunctionType(tipo, [lista_parametros[i][0] for i in range(0, len(lista_parametros))])
			self.func = ir.Function(self.modulo, função, name = 'main')
			bloco = self.func.append_basic_block('entry')
			self.construtor = ir.IRBuilder(bloco)
			self.block_atual = ir.IRBuilder(bloco)
		else:
			função = ir.FunctionType(tipo, [lista_parametros[i][0] for i in range(0, len(lista_parametros))])
			self.func = ir.Function(self.modulo, função, name = node.value[0])
			bloco = self.func.append_basic_block('entry')
			self.construtor = ir.IRBuilder(bloco)
			self.block_atual = ir.IRBuilder(bloco)

		for i, param in enumerate(lista_parametros):
			self.func.args[i].name = param[1]
			self.simbolos[self.escopo + '@' + param[1]][2] = self.construtor.alloca(param[0], name = param[1])
			self.construtor.store(self.func.args[i], self.simbolos[self.escopo + '@' + param[1]][2])

		if node.type == 'Funcao':
			self.ger_conjunto_declaracoes(node.child[2])

		self.escopo = 'global'

# def p_declaracao_variavel(p):
	
#     'Declaracao_Variavel : Tipo DOISPONTOS Variaveis'

#     p[0] = tree('Declaracao_Variavel', [p[1], p[3]])

	def ger_declaracao_variavel(self, node):
		tipo = self.ger_get_tipo(node.child[0])

		lista_variaveis = self.ger_variaveis(node.child[1])

		if self.escopo == 'global':
			for i in enumerate(lista_variaveis):
				self.simbolos[self.escopo + '@' + i[1]][2] = ir.GlobalVariable(self.modulo, tipo, i[1])
		else:
			for i in enumerate(lista_variaveis):
				self.simbolos[self.escopo + '@' + i[1]][2] = self.construtor.alloca(tipo, size=None, name=i[1])
			
			return self.simbolos[self.escopo + '@' + i[1]][2]

# def p_variaveis(p):

#     '''
#     Variaveis : Variaveis VIRGULA IDENTIFICADOR
#               | IDENTIFICADOR 
#     '''

#     if(len(p) == 4):
#         p[0] = tree('Variaveis_Virgula', [p[1]], p[3])
#     else:
#         p[0] = tree('Variaveis', [], p[1])

	def ger_variaveis(self, node):
		lista_variaveis = []

		if node.type == 'Variaveis_Virgula':
			while(node.type == 'Variaveis_Virgula'):
				lista_variaveis.append(node.value)
				
				node = node.child[0]

		if node.type == 'Variaveis':
			lista_variaveis.append(node.value)

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

	def ger_conjunto_parametros(self, node):
		variaveis = []

		if len(node.child) > 0:
			tipo = self.ger_get_tipo(node.child[0])
			variaveis.append((tipo,node.value[0]))

			if len(node.child) > 1:
				variaveis = variaveis + self.ger_conjunto_parametros(node.child[1])

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

	
	def ger_get_tipo(self, node):
		if node.value[0] == 'inteiro':
			return ir.IntType(32)

		return ir.FloatType()

# def p_conjunto_declaracoes(p):

#     ''' 
#     Conjunto_Declaracoes : Conjunto_Declaracoes Declaracao
#                          | Declaracao 
#     '''

#     if (len(p) == 3):
#         p[0] = tree('Conjunto_Declaracoes_Declaracoes_Declaracao', [p[1], p[2]])
#     else:
#         p[0] = tree('Conjunto_Declaracoes_Declaracao', [p[1]])

	def ger_conjunto_declaracoes(self, node):
		if len(node.child) > 1:
			self.ger_conjunto_declaracoes(node.child[0])
			return self.ger_declaracao(node.child[1])
		else:
			return self.ger_declaracao(node.child[0])

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

	def ger_declaracao(self, node):
		if node.child[0].type == 'Declaracao_Se' or node.child[0].type == 'Declaracao_Senao':
			return self.ger_declaracao_se(node.child[0])
		
		if node.child[0].type == 'Declaracao_Repita':
			self.ger_declaracao_repita(node.child[0])
		
		if node.child[0].type == 'Declaracao_Atribuicao':
			return self.ger_declaracao_atribuicao(node.child[0])

		if node.child[0].type == 'Declaracao_Leia':
			return self.ger_declaracao_leia(node.child[0])
		
		if node.child[0].type == 'Declaracao_Escreva':
			return self.ger_declaracao_escreva(node.child[0])

		if node.child[0].type == 'Declaracao_Variavel':
			return self.ger_declaracao_variavel(node.child[0])

		if node.child[0].type == 'Declaracao_Retorno':
			return self.ger_declaracao_retorna(node.child[0])
			
		if node.child[0].type == 'Chama_Funcao' or node.child[0].type == 'Chama_Funcao_Vazia':
			return self.ger_chama_funcao(node.child[0])
		


# def p_declaracao_se(p):
	
#     '''
#     Declaracao_Se : SE Expressao_Comparacional ENTAO Conjunto_Declaracoes FIM
#                   | SE Expressao_Comparacional ENTAO Conjunto_Declaracoes SENAO Conjunto_Declaracoes FIM
#     '''

#     if (len(p) == 6):
#         p[0] = tree('Declaracao_Se', [p[2], p[4]])
#     else:
#         p[0] = tree('Declaracao_Senao', [p[2], p[4], p[6]])  

	def ger_declaracao_se(self, node):
		self.phi = True
		self.retorno = True
		condição = self.ger_expressao_comparacional(node.child[0])

		print(len(node.child))

		bloco_então = self.func.append_basic_block('entao')
		if len(node.child) == 3:
			bloco_senão = self.func.append_basic_block('senao')
		bloco_fim = self.func.append_basic_block('fim')

		if len(node.child) == 3:
			self.construtor.cbranch(condição, bloco_então, bloco_senão)
		else:
			self.construtor.cbranch(condição, bloco_então, bloco_fim)

		self.construtor.position_at_end(bloco_então)
		valor_então = self.ger_conjunto_declaracoes(node.child[1])
		self.phi = True
		self.construtor.branch(bloco_fim)
		bloco_então = self.construtor.basic_block

		if len(node.child) == 3:
			self.construtor.position_at_end(bloco_senão)
			valor_senão = self.ger_conjunto_declaracoes(node.child[2])
			self.phi = True
			self.construtor.branch(bloco_fim)
			bloco_senão = self.construtor.basic_block

		self.construtor.position_at_end(bloco_fim)
		phi = self.construtor.phi(ir.IntType(32), 'se')
		phi.add_incoming(valor_então, bloco_então)
		if len(node.child) == 3:
			phi.add_incoming(valor_senão, bloco_senão)
		self.phi = False
		return phi


# def p_declaracao_repita(p):

#     'Declaracao_Repita : REPITA Conjunto_Declaracoes ATE Expressao_Comparacional'
	
#     p[0] = tree('Declaracao_Repita', [p[2], p[4]])

	def ger_declaracao_repita(self, node):
		self.phi = True
		bloco_repita = self.func.append_basic_block('repita')
		bloco_fim_repita = self.func.append_basic_block('fimRepita')
		self.construtor.branch(bloco_repita)
		self.construtor.position_at_end(bloco_repita)
		valor_repita = self.ger_conjunto_declaracoes(node.child[0])
		bloco_repita = self.construtor.basic_block

		print(node.child[1])
		condição = self.ger_expressao_comparacional(node.child[1])
		print(condição)
		self.construtor.cbranch(condição, bloco_repita, bloco_fim_repita)
		self.construtor.position_at_end(bloco_fim_repita)
		phi = self.construtor.phi(ir.IntType(32), 'repitaTmp')
		phi.add_incoming(valor_repita, bloco_repita)
		self.phi = False
		return phi

# def p_declaracao_atribuicao(p):

#     'Declaracao_Atribuicao : IDENTIFICADOR ATRIBUICAO Conjunto_Expressao'
	
#     p[0] = tree('Declaracao_Atribuicao', [p[3]], p[1])

	
	def ger_declaracao_atribuicao(self, node):
		if (self.escopo + '@' + node.value) in self.simbolos.keys():
			self.tipo_variavel = self.simbolos[self.escopo + '@' + node.value][1]
		else:
			self.tipo_variavel = self.simbolos['global@' + node.value][1]

		resultado = self.ger_conjunto_expressao(node.child[0])

		if (self.escopo + '@' + node.value) in self.simbolos.keys():
			self.construtor.store(resultado, self.simbolos[self.escopo + '@' + node.value][2])
			return self.construtor.load(self.simbolos[self.escopo + '@' + node.value][2])
		else:
			self.construtor.store(resultado, self.simbolos['global@' + node.value][2])
			return self.construtor.load(self.simbolos['global@' + node.value][2])

		# olhar aqui depois
		self.tipo_variavel = None

# def p_declaracao_leia(p):

#     'Declaracao_Leia : LEIA ABREPARENTES IDENTIFICADOR FECHAPARENTES'

#     p[0] = tree('Declaracao_Leia', [], p[3])

	def ger_declaracao_leia(self, node):
		if self.escopo + '@' + node.value[0] in self.simbolos.keys():
			if self.simbolos[self.escopo + '@' + node.value[0]][1] == 'inteiro':
				valor = self.construtor.call(self.leiaInteiro, [])
			else:
				valor = self.construtor.call(self.leiaFlutuante, [])
		else:
			if self.simbolos['global@' + node.value[0]][1] == 'inteiro':
				valor = self.construtor.call(self.leiaInteiro, [])
			else:
				valor = self.construtor.call(self.leiaFlutuante, [])
		return self.construtor.store(valor, self.simbolos[self.escopo + '@' + node.value[0]][2])

# def p_declaracao_escreva(p):

#     'Declaracao_Escreva : ESCREVA ABREPARENTES Conjunto_Expressao FECHAPARENTES'
	
#     p[0] = tree('Declaracao_Escreva', [p[3]])

	def ger_declaracao_escreva(self, node):
		expressão = self.ger_conjunto_expressao(node.child[0])

		if 'i32' in str(expressão):
			return self.construtor.call(self.escrevaInteiro, [expressão])
		else:
			return self.construtor.call(self.escrevaFlutuante, [expressão])	

# def p_declaracao_retorna(p):
	
#     'Declaracao_Retorno : RETORNA ABREPARENTES Conjunto_Expressao FECHAPARENTES'
	
#     p[0] = tree('Declaracao_Retorno', [p[3]])

	def ger_declaracao_retorna(self, node):
		self.tipo_variavel = self.simbolos[self.escopo][1]

		expressão = self.ger_conjunto_expressao(node.child[0])

		if self.retorno == True:
			self.guarda_retorno = self.ger_conjunto_expressao(node.child[0])

			if self.phi:
				return self.guarda_retorno
			
			return self.construtor.ret(self.guarda_retorno)
		else:
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

	def ger_conjunto_expressao(self, node, sinal=''):
		if node.child[0].type == 'Expressoes_ID' or node.child[0].type == 'Expressoes_ID_Virgula':
			return self.ger_expressao_id(node.child[0])
		
		if node.child[0].type == 'Expressao_Aritmetica':
			return self.ger_expressao_aritmetica(node.child[0])
		
		if node.child[0].type == 'Expressao_Comparacional':
			return self.ger_expressao_comparacional(node.child[0])
		
		if node.child[0].type == 'Expressao_Parenteses':
			return self.ger_expressao_parenteses(node.child[0])
		
		if node.child[0].type == 'Expressao_Numero':
			return self.ger_expressao_numero(node.child[0], sinal)

		if node.child[0].type == 'Chama_Funcao' or node.child[0].type == 'Chama_Funcao_Vazia':
			return self.ger_chama_funcao(node.child[0])

		if node.child[0].type == 'Expressao_Unaria':
			return self.ger_expressao_unaria(node.child[0])

# def p_parametros(p):

#     '''
#     Parametros : Parametros VIRGULA Conjunto_Expressao
#                | Conjunto_Expressao     
#     '''
#     if(len(p) == 4):
#         p[0] = tree('Parametros_Virgula', [p[1], p[3]])
#     else:
#         p[0] = tree('Parametros', [p[1]])

	def ger_parametros(self, node):
		lista_parametros = []

		# TODO ARRUMAR PARA QUANDO A FUNCAO È DE UM TIPO E OS PARAMETROS SAO DE OUTRO

		if len(node.child) > 1:
			lista_parametros.append(self.ger_conjunto_expressao(node.child[1]))
			lista_parametros = lista_parametros + self.ger_parametros(node.child[0])
		elif len(node.child) == 1:
			lista_parametros.append(self.ger_conjunto_expressao(node.child[0]))

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

	def ger_chama_funcao(self, node):
		lista_parametros = []

		funcao = self.modulo.get_global(node.value)
		#tipo = self.simbolos[node.value][2]

		if node.type != 'Chama_Funcao_Vazia':
			lista_parametros = self.ger_parametros(node.child[0])

		return self.construtor.call(funcao,lista_parametros[::-1])


# def p_expressoes_id(p):

#     'Expressao_ID : IDENTIFICADOR'

#     p[0] = tree('Expressoes_ID', [], p[1])

	def ger_expressao_id(self, node):
		if (self.escopo + '@' + node.value) in self.simbolos.keys():
			if self.tipo_variavel == self.simbolos[self.escopo + '@' + node.value][1]:
				valor = self.construtor.load(self.simbolos[self.escopo + '@' + node.value][2])
			else:
				valor = self.construtor.load(self.simbolos[self.escopo + '@' + node.value][2])
				if self.tipo_variavel == 'inteiro':
					valor =	self.construtor.fptosi(valor, ir.IntType(32))
				else:
					valor = self.construtor.sitofp(valor, ir.FloatType())
		else:
			if self.tipo_variavel == self.simbolos['global@' + node.value][1]:
				valor = self.construtor.load(self.simbolos['global@' + node.value][2])
				if self.tipo_variavel == 'inteiro':
					valor = self.construtor.fptosi(valor, ir.IntType(32))
				else:
					valor = self.construtor.sitofp(valor, ir.FloatType())
		return valor

# def p_expressao_aritmetica(p):

#     '''
#     Expressao_Aritmetica : Conjunto_Expressao SOMA Conjunto_Expressao
#                          | Conjunto_Expressao SUBTRACAO Conjunto_Expressao
#                          | Conjunto_Expressao MULTIPLICACAO Conjunto_Expressao
#                          | Conjunto_Expressao DIVISAO Conjunto_Expressao
#     '''

#     p[0] = tree('Expressao_Aritmetica', [p[1], p[3]], p[2])

	def ger_expressao_aritmetica(self, node):
		# if self.tipo_variavel == None:
		# 	if type(node.child[0].child[0].value) == float or type(node.child[1].child[0].value) == float:
		# 		self.tipo_variavel = 'flutuante'
		# 	else:
		# 		self.tipo_variavel = 'inteiro'

		esquerda = self.ger_conjunto_expressao(node.child[0])
		direita = self.ger_conjunto_expressao(node.child[1])
		print(esquerda)
		print(direita)

		if self.tipo_variavel == 'inteiro':
			if node.value == '+':
				return self.construtor.add(esquerda, direita, name='add')
			elif node.value == '-':
				return self.construtor.sub(esquerda, direita, name='sub')
			elif node.value == '*':
				return self.construtor.mul(esquerda, direita, name='mul')
			else:
				return self.construtor.sdiv(esquerda, direita, name='div')
		else:
			if node.value == '+':
				return self.construtor.fadd(esquerda, direita, name='fadd')
			elif node.value == '-':
				return self.construtor.fsub(esquerda, direita, name='fsub')
			elif node.value == '*':
				return self.construtor.fmul(esquerda, direita, name='fmul')
			else:
				return self.construtor.fdiv(esquerda, direita, name='fdiv')

# def p_expressao_aritmetica_unaria(p):

#     '''
#     Expressao_Unaria : SOMA Conjunto_Expressao
#                      | SUBTRACAO Conjunto_Expressao
#     '''
#     p[0] = tree('Expressao_Unaria', [p[2]])

	def ger_expressao_unaria(self, node):
		return self.ger_conjunto_expressao(node.child[0],sinal = node.value)

# def p_expressao_comparacional(p):

#     '''
#     Expressao_Comparacional : Conjunto_Expressao MAIOR Conjunto_Expressao
#                             | Conjunto_Expressao MENOR Conjunto_Expressao
#                             | Conjunto_Expressao MAIORIGUAL Conjunto_Expressao
#                             | Conjunto_Expressao MENORIGUAL Conjunto_Expressao
#                             | Conjunto_Expressao IGUALDADE Conjunto_Expressao
#     '''
#     p[0] = tree('Expressao_Comparacional', [p[1], p[3]])

	def ger_expressao_comparacional(self, node):
		esquerda = self.ger_conjunto_expressao(node.child[0])
		direita = self.ger_conjunto_expressao(node.child[1])

		if node.value == '=':
			node.value = '=='

		return self.construtor.icmp_unsigned(node.value, esquerda, direita, name='comparacao') 
			

# def p_expressao_parenteses(p):

#     'Expressao_Parenteses : ABREPARENTES Conjunto_Expressao FECHAPARENTES'

#     p[0] = tree('Expressao_Parenteses', [p[2]], [p[1], p[3]])

	def ger_expressao_parenteses(self, node):
		return self.ger_conjunto_expressao(node.child[0])


# def p_expressao_numero(p):

#     'Expressao_Numero : NUMERO'

#     p[0] = tree('Expressao_Numero', [], p[1])

	def ger_expressao_numero(self, node, sinal=''):
		numero = node.value

		if sinal == '-':
			numero = float(node.value) * -1

		if self.tipo_variavel == 'inteiro' and type(numero) == float:
			valor = ir.Constant(ir.FloatType(), numero)

			return self.construtor.fptosi(valor, ir.IntType(32))

		if self.tipo_variavel == 'flutuante' and type(numero) == int:
			valor = ir.Constant(ir.IntType(32), numero)

			return self.construtor.sitofp(valor, ir.FloatType())

		if type(numero) == int:
			return ir.Constant(ir.IntType(32), numero)
		else:
			return ir.Constant(ir.FloatType(), numero)

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