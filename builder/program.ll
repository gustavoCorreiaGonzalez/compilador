; ModuleID = "programa"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare float @"escrevaFlutuante"(float %".1") 

declare i32 @"escrevaInteiro"(i32 %".1") 

declare float @"leiaFlutuante"() 

declare i32 @"leiaInteiro"() 

define i32 @"main"() 
{
entry:
  %"add" = add i32 1, 3
  %".2" = call i32 (i32) @"escrevaInteiro"(i32 %"add")
  ret i32 0
}
