L_main:
    la sp, stack_end
    addi gp, sp, 0
    j L_simple
L_add:
    sw ra, 0(sp)
    addi fp, sp, 0
    addi sp, sp, -28
    lw t1, -12(fp)
    lw t2, -16(fp)
    add t0, t1, t2
    sw t0, -24(fp)
    lw t1, -24(fp)
    lw t0, -20(fp)
    sw t1, (t0)
    lw ra, 0(fp)
    jr ra
L_simple:
    sw ra, 0(sp)
    addi fp, sp, 0
    addi sp, sp, -28
    li t1, 5
    sw t1, -12(gp)
    li t1, 10
    sw t1, -16(gp)
    lw a0, -12(gp)
    li a7, 1
    ecall
    li a0, 10
    li a7, 11
    ecall
    lw a0, -16(gp)
    li a7, 1
    ecall
    li a0, 10
    li a7, 11
    ecall
    lw t1, -12(gp)
    sw t1, -40(sp)
    lw t1, -16(gp)
    sw t1, -44(sp)
    addi t1, fp, -24
    sw t1, -48(sp)
    addi t0, fp, 0
    sw t0, -32(sp)
    addi t0, fp, 0
    sw t0, -36(sp)
    addi sp, sp, -28
    jal L_add
    addi sp, sp, 28
    lw t1, -24(gp)
    sw t1, -20(gp)
    lw a0, -20(gp)
    li a7, 1
    ecall
    li a0, 10
    li a7, 11
    ecall
    li a7, 5
    ecall
    sw a0, -12(gp)
    lw a0, -12(gp)
    li a7, 1
    ecall
    li a0, 10
    li a7, 11
    ecall
    li a0, 0
    li a7, 93
    ecall
    lw ra, 0(fp)
    jr ra

.data
stack: .space 10240
stack_end:
