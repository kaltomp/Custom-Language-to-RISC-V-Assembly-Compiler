L_main:
    la sp, stack_end
    addi gp, sp, 0
    j L_test
L_anotheruseless:
    sw ra, 0(sp)
    addi fp, sp, 0
    addi sp, sp, -16
    li a0, 1
    li a7, 1
    ecall
    li a0, 10
    li a7, 11
    ecall
    lw ra, 0(fp)
    jr ra
L_useless:
    sw ra, 0(sp)
    addi fp, sp, 0
    addi sp, sp, -24
    li t1, 1
    li t2, 2
    add t0, t1, t2
    sw t0, -16(fp)
    lw t1, -16(fp)
    li t2, 3
    mul t0, t1, t2
    sw t0, -20(fp)
    lw a0, -20(fp)
    li a7, 1
    ecall
    li a0, 10
    li a7, 11
    ecall
    lw ra, 0(fp)
    jr ra
L_increase:
    sw ra, 0(sp)
    addi fp, sp, 0
    addi sp, sp, -32
    lw t1, -12(fp)
    li t2, 1
    add t0, t1, t2
    sw t0, -24(fp)
    lw t1, -24(fp)
    lw t0, -16(fp)
    sw t1, (t0)
    lw t1, -12(fp)
    li t2, 10
    add t0, t1, t2
    sw t0, -28(fp)
    lw t1, -28(fp)
    lw t0, -20(fp)
    sw t1, (t0)
    lw ra, 0(fp)
    jr ra
L_test:
    sw ra, 0(sp)
    addi fp, sp, 0
    addi sp, sp, -156
    li t1, 1
    sw t1, -12(gp)
    lw t1, -12(gp)
    lw t2, -12(gp)
    mul t0, t1, t2
    sw t0, -24(gp)
    li t1, 2
    lw t2, -12(gp)
    sub t0, t1, t2
    sw t0, -28(gp)
    li t1, 2
    lw t2, -12(gp)
    mul t0, t1, t2
    sw t0, -32(gp)
    lw t1, -28(gp)
    lw t2, -32(gp)
    sub t0, t1, t2
    sw t0, -36(gp)
    lw t1, -24(gp)
    lw t2, -36(gp)
    div t0, t1, t2
    sw t0, -40(gp)
    li t1, 2
    lw t2, -40(gp)
    add t0, t1, t2
    sw t0, -44(gp)
    lw t1, -44(gp)
    sw t1, -16(gp)
    lw t1, -12(gp)
    sw t1, -44(sp)
    addi t1, fp, -16
    sw t1, -48(sp)
    addi t1, fp, -48
    sw t1, -52(sp)
    addi t0, fp, 0
    sw t0, -36(sp)
    addi t0, fp, 0
    sw t0, -40(sp)
    addi sp, sp, -32
    jal L_increase
    addi sp, sp, 32
    lw t1, -48(gp)
    sw t1, -20(gp)
    li t1, 1
    sw t1, -16(gp)
L30:
    lw t1, -16(gp)
    li t2, 10
    blt t1, t2, L32
    j L41
L32:
    lw t1, -16(gp)
    li t2, 22
    bne t1, t2, L38
    j L34
L34:
    lw t1, -16(gp)
    li t2, 23
    bge t1, t2, L36
    j L40
L36:
    lw t1, -16(gp)
    li t2, 24
    ble t1, t2, L38
    j L40
L38:
    lw t1, -16(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -52(gp)
    lw t1, -52(gp)
    sw t1, -16(gp)
L40:
    j L30
L41:
    li a7, 5
    ecall
    sw a0, -16(gp)
    li t1, 12
    li t2, 12
    add t0, t1, t2
    sw t0, -56(gp)
    lw t1, -56(gp)
    sw t1, -20(gp)
    lw t1, -12(gp)
    li t2, 1
    beq t1, t2, L46
    j L49
L46:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -60(gp)
    lw t1, -60(gp)
    sw t1, -12(gp)
    j L63
L49:
    lw t1, -12(gp)
    li t2, 2
    beq t1, t2, L51
    j L54
L51:
    lw t1, -12(gp)
    li t2, 2
    add t0, t1, t2
    sw t0, -64(gp)
    lw t1, -64(gp)
    sw t1, -12(gp)
    j L63
L54:
    lw t1, -12(gp)
    li t2, 3
    beq t1, t2, L56
    j L61
L56:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -68(gp)
    lw t1, -68(gp)
    sw t1, -12(gp)
    lw t1, -12(gp)
    li t2, 2
    add t0, t1, t2
    sw t0, -72(gp)
    lw t1, -72(gp)
    sw t1, -12(gp)
    j L63
L61:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -76(gp)
    lw t1, -76(gp)
    sw t1, -12(gp)
L63:
    lw t1, -12(gp)
    li t2, 1
    beq t1, t2, L65
    j L68
L65:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -80(gp)
    lw t1, -80(gp)
    sw t1, -12(gp)
    j L63
L68:
    lw t1, -12(gp)
    li t2, 2
    beq t1, t2, L70
    j L73
L70:
    lw t1, -12(gp)
    li t2, 2
    add t0, t1, t2
    sw t0, -84(gp)
    lw t1, -84(gp)
    sw t1, -12(gp)
    j L63
L73:
    lw t1, -12(gp)
    li t2, 3
    beq t1, t2, L75
    j L80
L75:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -88(gp)
    lw t1, -88(gp)
    sw t1, -12(gp)
    lw t1, -12(gp)
    li t2, 2
    add t0, t1, t2
    sw t0, -92(gp)
    lw t1, -92(gp)
    sw t1, -12(gp)
    j L63
L80:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -96(gp)
    lw t1, -96(gp)
    sw t1, -12(gp)
L82:
    li t1, 0
    sw t1, -100(gp)
    lw t1, -12(gp)
    li t2, 1
    beq t1, t2, L85
    j L88
L85:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -104(gp)
    lw t1, -104(gp)
    sw t1, -12(gp)
    li t1, 1
    sw t1, -100(gp)
L88:
    lw t1, -12(gp)
    li t2, 2
    beq t1, t2, L90
    j L93
L90:
    lw t1, -12(gp)
    li t2, 2
    add t0, t1, t2
    sw t0, -108(gp)
    lw t1, -108(gp)
    sw t1, -12(gp)
    li t1, 1
    sw t1, -100(gp)
L93:
    lw t1, -12(gp)
    li t2, 3
    beq t1, t2, L95
    j L100
L95:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -112(gp)
    lw t1, -112(gp)
    sw t1, -12(gp)
    lw t1, -12(gp)
    li t2, 2
    add t0, t1, t2
    sw t0, -116(gp)
    lw t1, -116(gp)
    sw t1, -12(gp)
    li t1, 1
    sw t1, -100(gp)
L100:
    li t1, 1
    lw t2, -100(gp)
    beq t1, t2, L82
L101:
    lw t1, -12(gp)
    li t2, 1
    beq t1, t2, L103
    j L105
L103:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -120(gp)
    lw t1, -120(gp)
    sw t1, -12(gp)
L105:
    lw t1, -12(gp)
    li t2, 2
    beq t1, t2, L107
    j L109
L107:
    lw t1, -12(gp)
    li t2, 2
    add t0, t1, t2
    sw t0, -124(gp)
    lw t1, -124(gp)
    sw t1, -12(gp)
L109:
    lw t1, -12(gp)
    li t2, 3
    beq t1, t2, L111
    j L115
L111:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -128(gp)
    lw t1, -128(gp)
    sw t1, -12(gp)
    lw t1, -12(gp)
    li t2, 2
    add t0, t1, t2
    sw t0, -132(gp)
    lw t1, -132(gp)
    sw t1, -12(gp)
L115:
    lw t1, -12(gp)
    li t2, 2
    bgt t1, t2, L117
    j L101
L117:
    li t1, 1
    sw t1, -16(gp)
L118:
    lw t1, -16(gp)
    li t2, 10
    bgt t1, t2, L136
    lw t1, -12(gp)
    li t2, 1
    beq t1, t2, L121
    j L123
L121:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -136(gp)
    lw t1, -136(gp)
    sw t1, -12(gp)
L123:
    lw t1, -12(gp)
    li t2, 2
    beq t1, t2, L125
    j L127
L125:
    lw t1, -12(gp)
    li t2, 2
    add t0, t1, t2
    sw t0, -140(gp)
    lw t1, -140(gp)
    sw t1, -12(gp)
L127:
    lw t1, -12(gp)
    li t2, 3
    beq t1, t2, L129
    j L133
L129:
    lw t1, -12(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -144(gp)
    lw t1, -144(gp)
    sw t1, -12(gp)
    lw t1, -12(gp)
    li t2, 2
    add t0, t1, t2
    sw t0, -148(gp)
    lw t1, -148(gp)
    sw t1, -12(gp)
L133:
    lw t1, -16(gp)
    li t2, 1
    add t0, t1, t2
    sw t0, -152(gp)
    lw t1, -152(gp)
    sw t1, -16(gp)
    j L118
L136:
    li a0, 0
    li a7, 93
    ecall
    lw ra, 0(fp)
    jr ra

.data
stack: .space 10240
stack_end:
