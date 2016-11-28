inteiro: n
flutuante: m

inteiro fatorial(inteiro: n, flutuante: a)
    inteiro: fat

    se n > 0 então {não calcula se n > 0}
        fat := 1
        repita
            fat := fat * n
            n := n - 1
        até n = 0
        retorna(fat) {retorna o valor do fatorial de n}
    senão
        retorna(0)
    fim
fim

inteiro principal()
    leia(n)
    escreva(fatorial(fatorial(1,2.2)))
    retorna(0)
fim