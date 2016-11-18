# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# semantica.py
# Analisador semantico e geração de uma tabela de símbolos
# Autor: Gustavo Correia Gonzalez
#-------------------------------------------------------------------------

from sintatica import *

class semantica():
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

		if no_atual.type == 'Variaveis':
			if ('global@' + no_atual.value[0] in self.simbolos.keys()):
				print("Erro semântico: ID '" + no_atual.value[0] + "' já foi declarado")
				exit(1)

			self.simbolos['global@' + no_atual.value[0]] = ['variável', tipo, 0, False]
		else:
			while(no_atual.type == 'Variaveis_Virgula'):
				if ('global@' + no_atual.value[0] in self.simbolos.keys()):
					print("Erro semântico: ID '" + no_atual.value[0] + "' já foi declarado")
					exit(1)

				self.simbolos['global@' + no_atual.value[0]] = ['variável', tipo, 0, False]

				no_atual = no_atual.child[0]

		if ('global@' + no_atual.value[0] in self.simbolos.keys()):
			print("Erro semântico: ID '" + no_atual.value[0] + "' já foi declarado")
			exit(1)

		self.simbolos['global@' + no_atual.value[0]] = ['variável', tipo, 0, False]
		

	def Funcao(self, node):
		tipo = self.getTipo(node.child[0])

		if (node.value[0] in self.simbolos.keys()):
			print("Erro semântico: ID '" + node.value[0] + "' já foi declarado")
			exit(1)

		lista_parametros = self.Conjunto_Parametros(node.child[1])
		
		self.simbolos[node.value[0]] = ['funcao', tipo, lista_parametros]

		if node.type == 'Funcao':
			self.Conjunto_Declaracoes(node.child[2])

	def Conjunto_Parametros(self, node):		
		variaveis = []
		if len(node.child) > 0:
			tipo = self.getTipo(node.child[0])
			variaveis.append(tipo)
			self.simbolos[str(self.escopo + '.' + node.value[0])] = ['variável', tipo, 0, True]
			if len(node.child) > 1:
				variaveis = variaveis + self.Conjunto_Parametros(node.child[1])
		return variaveis

	def Conjunto_Declaracoes(self, node):
		if len(node.child) > 1:
			self.Conjunto_Declaracoes(node.child[0])
			self.Declaracao(node.child[1])
		else:
			self.Declaracao(node.child[0])

	def Declaracao(self, node):
		if node.child[0].type == 'Declaracao_Se':
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
			
		if node.child[0].type == 'Chama_Funcao':
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
		print('ac')

	def Declaracao_Leia(self, node):
		print('ad')

	def Declaracao_Escreva(self, node):
		self.Conjunto_Expressao(node.child[0])

	def Declaracao_Retorno(self, node):
		print('ag')

	def Chama_Funcao(self, node):
		print('ah')    
	    
	def Expressao_Comparacional(self, node):
		print('Expressao_Comparacional')

	def Conjunto_Expressao(self, node):
		if node.child[0].type == 'Expressao_ID':
			self.Expressao_ID(node.child[0])
		
		if node.child[0].type == 'Expressao_Aritmetica':
			self.Expressao_Aritmetica(node.child[0])
		
		if node.child[0].type == 'Expressao_Comparacional':
			self.Expressao_Comparacional(node.child[0])
		
		if node.child[0].type == 'Expressao_Parenteses':
			self.Expressao_Parenteses(node.child[0])
		
		if node.child[0].type == 'Expressao_Numero':
			self.Expressao_Numero(node.child[0])

		if node.child[0].type == 'Chama_Funcao':
			self.Chama_Funcao(node.child[0])

		if node.child[0].type == 'Expressao_Unaria':
			self.Expressao_Unaria(node.child[0])

	def Expressao_ID(self, node):
		print('ba')

	def Expressao_Aritmetica(self, node):
		print('bb')

	def Expressao_Parenteses(self, node):
		self.Conjunto_Expressao(node.child[0])

	def Expressao_Numero(self, node):
		print('be')

	def Expressao_Unaria(self, node):
		print('bf')

	def getTipo(self, node):
		return node.value[0]


if __name__ == '__main__':
	import sys
	code = open(sys.argv[1])
	s = semantica(code.read())
	s.Principal()
	print("Tabela de símbolos:", s.simbolos)