	.text
	.file	"builder/program.ll"
	.section	.rodata.cst4,"aM",@progbits,4
	.align	4
.LCPI0_0:
	.long	1102053376              # float 22
.LCPI0_1:
	.long	1082130432              # float 4
	.text
	.globl	teste1
	.align	16, 0x90
	.type	teste1,@function
teste1:                                 # @teste1
	.cfi_startproc
# BB#0:                                 # %entry
	pushq	%rax
.Ltmp0:
	.cfi_def_cfa_offset 16
	callq	leiaFlutuante
	movss	%xmm0, 4(%rsp)
	mulss	.LCPI0_0(%rip), %xmm0
	divss	.LCPI0_1(%rip), %xmm0
	movss	%xmm0, 4(%rsp)
	cvttss2si	%xmm0, %eax
	popq	%rdx
	retq
.Lfunc_end0:
	.size	teste1, .Lfunc_end0-teste1
	.cfi_endproc

	.globl	teste2
	.align	16, 0x90
	.type	teste2,@function
teste2:                                 # @teste2
	.cfi_startproc
# BB#0:                                 # %entry
	pushq	%rax
.Ltmp1:
	.cfi_def_cfa_offset 16
	callq	leiaInteiro
	movl	%eax, 4(%rsp)
	cmpl	$10, %eax
	movl	$10, %eax
	popq	%rdx
	retq
.Lfunc_end1:
	.size	teste2, .Lfunc_end1-teste2
	.cfi_endproc

	.globl	teste3
	.align	16, 0x90
	.type	teste3,@function
teste3:                                 # @teste3
	.cfi_startproc
# BB#0:                                 # %entry
	movl	$3, -4(%rsp)
	.align	16, 0x90
.LBB2_1:                                # %repita
                                        # =>This Inner Loop Header: Depth=1
	decl	-4(%rsp)
	jne	.LBB2_1
# BB#2:                                 # %fimRepita
	movl	-4(%rsp), %eax
	retq
.Lfunc_end2:
	.size	teste3, .Lfunc_end2-teste3
	.cfi_endproc

	.globl	main
	.align	16, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# BB#0:                                 # %entry
	pushq	%rax
.Ltmp2:
	.cfi_def_cfa_offset 16
	callq	teste1
	movl	%eax, 4(%rsp)
	movl	%eax, %edi
	callq	escrevaInteiro
	movl	$1, %eax
	popq	%rdx
	retq
.Lfunc_end3:
	.size	main, .Lfunc_end3-main
	.cfi_endproc


	.section	".note.GNU-stack","",@progbits
