# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# semantica.py
# Analisador semantico e geração de uma tabela de símbolos
# Autor: Gustavo Correia Gonzalez
#-------------------------------------------------------------------------

from sintatica import *

class semantica():
	def __init__ (self, codigo):
		self.árvore = parse_tree(codigo)
		self.símbolos = {}
		self.escopo = 'global'

	def programa(self):
		if self.árvore.type == 'Programa_Declaracoes':
			print('asdfasfdasdf')

if __name__ == '__main__':
	import sys
	code = open(sys.argv[1])
	s = semantica(code.read())
	s.programa()
	print("Tabela de símbolos:", s.símbolos)