inteiro teste1()
	flutuante:a
	leia(a)
	a:=a*(2+20)/4

	retorna(a)
fim

inteiro teste2()
	inteiro:a

	leia(a)

	se a > 10 então
		retorna(1)
	senão
		retorna(2)
	fim

	retorna(10)
fim

inteiro teste3()
	inteiro:n

	n:=3

	repita
		n:=n-1
	até n > 0

	retorna(n)
fim

inteiro principal()
	inteiro: a
	a:=teste1()
	escreva(a)

	retorna(1)
fim