; ModuleID = "programa"
target datalayout = ""

@"c" = external global float
define i32 @"principal"() 
{
entry:
  %".2" = sitofp i32 1 to float
  store float %".2", float* @"c"
}
