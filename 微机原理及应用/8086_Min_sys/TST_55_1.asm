;=============================
; func：8位数字0-7
; CPU：8086
; IO：8255A
;=============================

; ------寄存器使用--------
; si存显存数组No当前下标
; cx存循环次数
; al和IO口交互，同时暂存No当前位数值
; ah存位选信号//PA0连第一位数码管。。
; bx存led段码表基址，用于换码寻址
; -----------------------

; ------8255使用---------
; 寄存器   |功能           |地址    |配置
; A口：     位选；          0280h    方式0输出
; B口：     段码；          0282h    方式0输出
; CT_reg：  控制寄存器；    0286h
; -----------------------

DATA	SEGMENT
    LED	DB	3FH,06H,5BH,4FH,66H,6DH,7DH,07H,7FH,6FH	;段码表
            ;0  1   2   3   4   5   6   7   8   9
    No1	DB	0,1,2,3,4,5,6,7	;要显示的数字

; 8086
    PORT_A EQU   0280h       ;A口地址
    PORT_B EQU   0282h       ;B口地址
    CT_reg EQU   0286h       ;控制寄存器地址
    CTRO_W EQU   10001001b    ;方式控制字 AB口方式0输出
DATA ENDS



stack_seg segment ;32bytes
    dw 16 dup(0)
stack_seg ends

code segment
    assume cs:code , ds:data, ss:stack_seg
START:
    ;初始化寄存器 ds，ss，bx，8255
    mov ax,data
    mov ds,ax
    mov ax,stack_seg
    mov ss,ax
    mov sp,32

    ;bx
    mov bx,offset LED
    ;8255
    mov dx, CT_reg
    mov al, CTRO_W
    out dx,al

    ;主循环
M_LOOP:
    lea si,No1  ; 配置显存地址
go_lp:
    ; 重置位选、si指向、计数器cx（i）
    mov ah,11111110B
    mov cx,8
    ; 8个显示帧
SC_lp:  ; 输出位选信号
        mov dx,PORT_A
        mov al,ah
        out dx,al
        ; 更新位选信号
        rol ah,1
        ; 输出段码信号
        mov dx,PORT_B
        mov al,ds:[si]   ; 根据si指向找到显存数组当前位
        xlat
        out dx,al
        ; si指向下一位
        inc si
        call DELAY
    
    loop SC_lp

    ; 主循环返回
    jmp M_LOOP

    ; 延时
DELAY:
    push cx
    mov cx,40
de_lp:
    NOP
    loop de_lp
    pop cx
    ret

code ends
end START