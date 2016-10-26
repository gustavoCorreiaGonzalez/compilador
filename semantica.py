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

	def programa(self):
		if self.arvore.type == 'Programa_Declaracoes_Programa':
			self.Declaracoes(self.arvore.child[0])
			self.Programa(self.arvore.child[1])
		else:
			self.Declaracoes(self.arvore.child[0])

	def Declaracoes(self, no):
		if no.child[0].type == 'Declaracao_Variavel':
			self.Declaracao_Variavel(no.child[0])
		else:
			self.Funcao(no.child[0])

	def Programa(self, no):
		print('sfsdf')

	def Declaracao_Variavel(self, no):
		if len(no.child) > 0:
			simbolos

		tipo = self.getTipo(nó.filho[0])
        if tipo == 'vazio':
            print("Erro semântico: ID '" + nó.folha[0] + "' não pode ser do tipo 'vazio'")
            exit(1)
        if self.escopo + '.' + nó.folha[0] in self.símbolos.keys():
            print("Erro semântico: ID '" + nó.folha[0] + "' já foi declarado")
            exit(1)
        if nó.folha[0] is self.símbolos.keys():
            print("Erro semântico: ID '" + nó.folha[0] + "' foi declarado como função")
            exit(1)
        self.símbolos[self.escopo + '.' + nó.folha[0]] = ['variável', tipo, 0, False]



		print(no.child[])
		print('sfsdf')

	def Funcao(self, no):
		print('sfafdsfasdfsdf')

	def getTipo(self, nó):
        return nó.folha[0]


if __name__ == '__main__':
	import sys
	code = open(sys.argv[1])
	s = semantica(code.read())
	s.programa()
	print("Tabela de símbolos:", s.simbolos)