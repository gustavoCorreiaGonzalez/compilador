inteiro: n
inteiro: único

inteiro fatorial(inteiro: n, inteiro: b)
  inteiro: fat
  se n > 0 então {não calcula se n > 0}
    fat := 1
    repita
      fät := fät * n
      n := n - 1
    até n = 0
    retorna(fat) {retorna o valor do fatorial de n}
  senão
    retorna(0)
  fim
fim

flutuante : aaa

inteiro fatorial2(inteiro: n, inteiro: b)
  inteiro: fat
  se n > 0 então {não calcula se n > 0}
    fat := 1
    repita
      fät := fät * n
      n := n - 1
    até n = 0
    retorna(fat) {retorna o valor do fatorial de n}
  senão
    retorna(0)
  fim
fim



inteiro principal()
  leia(n)
  escreva(fatorial(n))
fim

inteiro : mn

