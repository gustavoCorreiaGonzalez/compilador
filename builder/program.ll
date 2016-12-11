; ModuleID = "programa"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare float @"escrevaFlutuante"(float %".1") 

declare i32 @"escrevaInteiro"(i32 %".1") 

declare float @"leiaFlutuante"() 

declare i32 @"leiaInteiro"() 

define i32 @"teste1"() 
{
entry:
  %"a" = alloca float
  %".2" = call float () @"leiaFlutuante"()
  store float %".2", float* %"a"
  %".4" = load float, float* %"a"
  %".5" = sitofp i32 2 to float
  %".6" = sitofp i32 20 to float
  %"fadd" = fadd float %".5", %".6"
  %"fmul" = fmul float %".4", %"fadd"
  %".7" = sitofp i32 4 to float
  %"fdiv" = fdiv float %"fmul", %".7"
  store float %"fdiv", float* %"a"
  %".9" = load float, float* %"a"
  %".10" = load float, float* %"a"
  %".11" = fptosi float %".10" to i32
  ret i32 %".11"
}

define i32 @"teste2"() 
{
entry:
  %"a" = alloca i32
  %".2" = call i32 () @"leiaInteiro"()
  store i32 %".2", i32* %"a"
  %".4" = load i32, i32* %"a"
  %"comparacao" = icmp ugt i32 %".4", 10
  br i1 %"comparacao", label %"entao", label %"senao"
entao:
  br label %"fim"
senao:
  br label %"fim"
fim:
  %"se" = phi i32 [1, %"entao"], [2, %"senao"]
  ret i32 10
}

define i32 @"teste3"() 
{
entry:
  %"n" = alloca i32
  store i32 3, i32* %"n"
  %".3" = load i32, i32* %"n"
  br label %"repita"
repita:
  %".5" = load i32, i32* %"n"
  %"sub" = sub i32 %".5", 1
  store i32 %"sub", i32* %"n"
  %".7" = load i32, i32* %"n"
  %".8" = load i32, i32* %"n"
  %"comparacao" = icmp ugt i32 %".8", 0
  br i1 %"comparacao", label %"repita", label %"fimRepita"
fimRepita:
  %"repitaTmp" = phi i32 [%".7", %"repita"]
  %".10" = load i32, i32* %"n"
  ret i32 %".10"
}

define i32 @"main"() 
{
entry:
  %"a" = alloca i32
  %".2" = call i32 () @"teste1"()
  store i32 %".2", i32* %"a"
  %".4" = load i32, i32* %"a"
  %".5" = load i32, i32* %"a"
  %".6" = call i32 (i32) @"escrevaInteiro"(i32 %".5")
  ret i32 1
}
