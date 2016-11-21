{Teste compiladores do João Martins Filho}

inteiro: n, g, a
flutuante: d
inteiro fatorial(inteiro: n, inteiro: g, inteiro: ga)
	d := 5.6 
	flutuante: fat
	fat := 2e+89 + 67*12
	se fat > 10 então
		se n > 0 então {não calcula se n > 0}
			fat := 1
			repita
				repita
					fat := fat * n
					n := n - 1e+10
				até n = 0
				fat := fat * n
				n := n - 1e+10
			até n = 0
			retorna(fat) {retorna o valor do fatorial de n}
		senão
			retorna(0 + 1)
		fim
	fim
	inteiro: teste
	teste := (5+10)*14
	teste := 5+ 10*14
	teste := 5-(1+5)
	teste := 5-1
	teste := -10+10
fim

inteiro faznada()
fim

inteiro principal()
	leia(n)
	escreva(fatorial(fatorial(n<1,a),n+2))
	fatorial(a)
fim