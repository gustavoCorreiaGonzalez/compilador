# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# semantica.py
# Analisador semantico e geração de uma tabela de símbolos
# Autor: Gustavo Correia Gonzalez
#-------------------------------------------------------------------------

from sintatica import *
from pprint import pprint

class Semantica():
	def __init__ (self, codigo):
		self.arvore = parse_tree(codigo)
		self.simbolos = {}
		self.escopo = 'global'

	def Principal(self):
		self.Programa(self.arvore)

	def Programa(self, node):
		if node.type == 'Programa_Declaracoes_Programa':
			self.Programa(node.child[0])
			self.Declaracoes(node.child[1])
		else:
			self.Declaracoes(node.child[0])

	def Declaracoes(self, node):
		if node.child[0].type == 'Declaracao_Variavel':
			self.Declaracao_Variavel(node.child[0])
		else:
			self.Funcao(node.child[0])

	def Declaracao_Variavel(self, node):
		tipo = self.getTipo(node.child[0])

		no_atual = node.child[1]

		if no_atual.type == 'Variaveis_Virgula':
			while(no_atual.type == 'Variaveis_Virgula'):
				if (self.escopo + '@' + no_atual.value in self.simbolos.keys()):
					print("Erro semântico: ID '" + no_atual.value + "' já foi declarado")
					exit(1)

				if (no_atual.value in self.simbolos.keys()):
					print("Erro semântico: ID '" + no_atual.value + "' já foi declarado como função")
					exit(1)

				self.simbolos[self.escopo + '@' + no_atual.value] = ['variável', tipo, 0, False]
				
				no_atual = no_atual.child[0]

		if no_atual.type == 'Variaveis':
			if (self.escopo + '@' + no_atual.value in self.simbolos.keys()):
				print("Erro semântico: ID '" + no_atual.value + "' já foi declarado")
				exit(1)

			if (no_atual.value in self.simbolos.keys()):
				print("Erro semântico: ID '" + no_atual.value + "' já foi declarado como função")
				exit(1)

			self.simbolos[self.escopo + '@' + no_atual.value] = ['variável', tipo, 0, False]

	def Funcao(self, node):
		self.escopo = node.value[0]
		tipo = self.getTipo(node.child[0])

		if (node.value[0] in self.simbolos.keys()):
			print("Erro semântico: Função '" + node.value[0] + "' já foi declarado")
			exit(1)

		lista_parametros = self.Conjunto_Parametros(node.child[1], node.value[0])

		self.simbolos[node.value[0]] = ['funcao', tipo, lista_parametros]

		if node.type == 'Funcao':
			self.Conjunto_Declaracoes(node.child[2])

		self.escopo = 'global'

	def Conjunto_Parametros(self, node, nome_funcao):		
		variaveis = []

		if len(node.child) > 0:
			tipo = self.getTipo(node.child[0])
			if self.escopo + '@' + node.value[0] not in self.simbolos.keys():
				self.simbolos[str(self.escopo + '@' + node.value[0])] = ['variável', tipo, 0, True]
				variaveis.append(tipo)
			else:
				print("Erro semântico: Variável '" + node.value[0] + "' já foi utilizada na declaração da função")
				exit(1)

			if node.value[0] == nome_funcao:
				print("Erro semântico: Variável '" + node.value[0] + "' já foi utilizada na declaração da função")
				exit(1)

			if len(node.child) > 1:
				variaveis = variaveis + self.Conjunto_Parametros(node.child[1], nome_funcao)

		return variaveis

	def Conjunto_Declaracoes(self, node):
		if len(node.child) > 1:
			self.Conjunto_Declaracoes(node.child[0])
			self.Declaracao(node.child[1])
		else:
			self.Declaracao(node.child[0])

	def Declaracao(self, node):
		if node.child[0].type == 'Declaracao_Se' or node.child[0].type == 'Declaracao_Senao':
			self.Declaracao_Se(node.child[0])
		
		if node.child[0].type == 'Declaracao_Repita':
			self.Declaracao_Repita(node.child[0])
		
		if node.child[0].type == 'Declaracao_Atribuicao':
			self.Declaracao_Atribuicao(node.child[0])
		
		if node.child[0].type == 'Declaracao_Leia':
			self.Declaracao_Leia(node.child[0])
		
		if node.child[0].type == 'Declaracao_Escreva':
			self.Declaracao_Escreva(node.child[0])

		if node.child[0].type == 'Declaracao_Variavel':
			self.Declaracao_Variavel(node.child[0])

		if node.child[0].type == 'Declaracao_Retorno':
			self.Declaracao_Retorno(node.child[0])
			
		if node.child[0].type == 'Chama_Funcao' or node.child[0].type == 'Chama_Funcao_Vazia':
			self.Chama_Funcao(node.child[0])

	def Declaracao_Se(self, node):
		self.Expressao_Comparacional(node.child[0])
		self.Conjunto_Declaracoes(node.child[1])
		if len(node.child) == 3:
			self.Conjunto_Declaracoes(node.child[2])

	def Declaracao_Repita(self, node):
		self.Conjunto_Declaracoes(node.child[0])
		self.Expressao_Comparacional(node.child[1])

	def Declaracao_Atribuicao(self, node):
		if (self.escopo + '@' + node.value not in self.simbolos.keys()) and ('global@' + node.value not in self.simbolos.keys()):
			print('Erro semântico: ID ' + node.value + ' não declarado')
			exit(1)

		lista_tipo = self.Conjunto_Expressao(node.child[0])

		if self.escopo + '@' + node.value in self.simbolos.keys():
			if self.simbolos[self.escopo + '@' + node.value][1] != lista_tipo:
				print("WARNING atribuição: ID '" + node.value + "' é do tipo '" + str(self.simbolos[self.escopo + '@' + node.value][1]) + "' está atribuindo uma expressão do tipo '" + str(lista_tipo) + "'")

			if not(self.simbolos[self.escopo + '@' + node.value][3]):
				self.simbolos[self.escopo + '@' + node.value][3] = True

		elif 'global@' + node.value in self.simbolos.keys():
			if self.simbolos['global@' + node.value][1] != lista_tipo:
				print("WARNING atribuição: ID '" + node.value + "' é do tipo '" + str(self.simbolos['global@' + node.value][1]) + "' está atribuindo uma expressão do tipo '" + str(lista_tipo) + "'")

			if not(self.simbolos['global@' + node.value][3]):
				self.simbolos['global@' + node.value][3] = True

	def Declaracao_Leia(self, node):
		if (self.escopo + '@' + node.value not in self.simbolos.keys()) and ('global@' + node.value not in self.simbolos.keys()):
			print('Erro semântico: ID ' + node.value + ' não declarado')
			exit(1)
		elif self.escopo + '@' + node.value in self.simbolos.keys():
			self.simbolos[self.escopo + '@' + node.value][3] = True
		else:
			self.simbolos['global@' + node.value][3] = True

	def Declaracao_Escreva(self, node):
		self.Conjunto_Expressao(node.child[0])

	def Declaracao_Retorno(self, node):
		lista_tipo = self.Conjunto_Expressao(node.child[0])		
		tipo_funcao = self.simbolos[self.escopo][1]

		if lista_tipo != tipo_funcao:
			print("WARNING: função '" + self.escopo + "' é do tipo '" + str(tipo_funcao) + "' e está retornando uma expressão do tipo '" + str(lista_tipo) + "'")

	def Chama_Funcao(self, node):
		if node.value not in self.simbolos.keys():
			print("Erro semântico: função '" + node.value + "' não foi declarada")
			exit(1)

		numero_parametros = []

		if node.type != 'Chama_Funcao_Vazia':
			numero_parametros = self.Parametros(node.child[0])

		if len(numero_parametros) != len(self.simbolos[node.value][2]):
			print("Erro semântico: esperado '" + str(len(self.simbolos[node.value][2])) + "' parâmetro(s) na função '" + node.value + ", mas foi passado '" + str(len(numero_parametros)) + "' parâmetro(s)")
			exit(1)

		if self.simbolos[node.value][2] != numero_parametros[::-1]:
			print("WARNING chamada de função: espera parâmetros dos tipos " + str(self.simbolos[node.value][2]) + " e está sendo passado " + str(numero_parametros[::-1]) + " na função '"  + node.value + "'")

		return self.simbolos[node.value][1]

	def Parametros(self, node):
		lista_parametros = []

		if len(node.child) > 1:
			lista_parametros.append(self.Conjunto_Expressao(node.child[1]))
			lista_parametros = lista_parametros + self.Parametros(node.child[0])
		elif len(node.child) == 1:
			lista_parametros.append(self.Conjunto_Expressao(node.child[0]))

		return lista_parametros
	

	def Expressao_Comparacional(self, node):
		self.Conjunto_Expressao(node.child[0])
		self.Conjunto_Expressao(node.child[1])

	def Conjunto_Expressao(self, node):
		if node.child[0].type == 'Expressoes_ID' or node.child[0].type == 'Expressoes_ID_Virgula':
			return self.Expressao_ID(node.child[0])
		
		if node.child[0].type == 'Expressao_Aritmetica':
			return self.Expressao_Aritmetica(node.child[0])
		
		if node.child[0].type == 'Expressao_Comparacional':
			return self.Expressao_Comparacional(node.child[0])
		
		if node.child[0].type == 'Expressao_Parenteses':
			return self.Expressao_Parenteses(node.child[0])
		
		if node.child[0].type == 'Expressao_Numero':
			return self.Expressao_Numero(node.child[0])

		if node.child[0].type == 'Chama_Funcao' or node.child[0].type == 'Chama_Funcao_Vazia':
			return self.Chama_Funcao(node.child[0])

		if node.child[0].type == 'Expressao_Unaria':
			return self.Expressao_Unaria(node.child[0])

	def Expressao_ID(self, node):
		if (self.escopo + '@' + node.value not in self.simbolos.keys()) and ('global@' + node.value not in self.simbolos.keys()):
			print('Erro semãntico: ID ' + node.value + ' não declarado')
			exit(1)

		if self.escopo + '@' + node.value in self.simbolos.keys():
			if not(self.simbolos[self.escopo + '@' + node.value][3]):
					print("Erro semântico: ID '" + node.value + "' não foi inicializado")
					exit(1)

			return self.simbolos[self.escopo + '@' + node.value][1]

		elif 'global@' + node.value in self.simbolos.keys():
			if not(self.simbolos['global@' + node.value][3]):
					print("Erro semântico: ID '" + node.value + "' não foi inicializado")
					exit(1)

			return self.simbolos['global@' + node.value][1]

	def Expressao_Aritmetica(self, node):
		esquerda = self.Conjunto_Expressao(node.child[0])
		direita = self.Conjunto_Expressao(node.child[1])

		if (esquerda == 'inteiro') and (direita == 'inteiro'):
			return 'inteiro'
		elif (esquerda == 'flutuante') and (direita == 'flutuante'):
			return 'flutuante'
		elif (esquerda == 'flutuante') or (direita == 'flutuante'):
			return 'flutuante'
		else:
			return 'inteiro'

	def Expressao_Parenteses(self, node):
		return self.Conjunto_Expressao(node.child[0])

	def Expressao_Numero(self, node):
		if type(node.value) == int:
			return 'inteiro'

		return 'flutuante'

	def Expressao_Unaria(self, node):
		return self.Conjunto_Expressao(node.child[0])

	def getTipo(self, node):
		return node.value[0]

if __name__ == '__main__':
	import sys
	code = open(sys.argv[1])
	s = Semantica(code.read())
	s.Principal()
	for keys,values in s.simbolos.items():
		if(values[0]=='variável' and values[3]!=True):
			print("WARNING: Variavel " +  keys + " não esta sendo utilizada" )
	print('Tabela de símbolos:')
	pprint(s.simbolos)