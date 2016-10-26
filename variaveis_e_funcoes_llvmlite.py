from llvmlite import ir

'''
Este módulo contém duas funções e criação de variáveis locais
Será gerado um código em LLVM como este em C:

int foo() {
	int a = 7;
	int b = a + 6;
	return b;
}

int main() {
	int c = foo();
	return 0;
}
'''

mod = ir.Module('meu_modulo')
t_int = ir.IntType(32)
t_func = ir.FunctionType(t_int, ())

######## Função "foo"

foo = ir.Function(mod, t_func, name='foo')
bb = foo.append_basic_block('entry')
builder = ir.IRBuilder(bb)

a = builder.alloca(t_int, name='a')
b = builder.alloca(t_int, name='b')

builder.store(ir.Constant(ir.IntType(32), 7), a)

# operando deve ser carregado antes de utilizá-lo
load_a = builder.load(a)
add = builder.add(load_a, ir.Constant(ir.IntType(32), 6), name='add')
builder.store(add, b)

load_b = builder.load(b)
builder.ret(load_b)

######## Função "main"

main = ir.Function(mod, t_func, name='main')
bb = main.append_basic_block('entry')
builder = ir.IRBuilder(bb)

c = builder.alloca(t_int, name='c')
call = builder.call(foo, (), name='call')
builder.store(call, c)
builder.ret(ir.Constant(ir.IntType(32), 0))

print(mod)