section .data
    prompt db 'Enter number: ', 0  ; Define a prompt message for user input, terminated with null byte
    result db 'The sum is: ', 0     ; Define a message for displaying the sum, terminated with null byte
    crlf   db 0x0D, 0x0A, 0 ; Define ASCII characters for printing a new line, terminated with null byte.

;---------------------------------------------------------------------------------------
section .text
    global _start

_start:

    ; Display prompt for entering the first number
    mov     rax, 1        ; Load system call number for write into rax
    mov     rdi, 1        ; Load file descriptor for stdout into rdi
    mov     rsi, prompt  ; Load address of prompt message into rsi
    mov     rdx, 14       ; Load length of prompt message into rdx
    syscall              ; Invoke system call to write prompt

    ; Read the first number input by the user
    mov     rax, 0        ; Load system call number for read into rax
    mov     rsi, 0        ; Load file descriptor for stdin into rsi
    mov     rdi, 0        ; Load address to store input into rdi
    syscall              ; Invoke system call to read user input
    mov     r8, rax       ; Store the input value in register r8

    ; Display prompt for entering the second number
    mov     rax, 1        ; Load system call number for write into rax
    mov     rdi, 1        ; Load file descriptor for stdout into rdi
    mov     rsi, prompt  ; Load address of prompt message into rsi
    mov     rdx, 14       ; Load length of prompt message into rdx
    syscall              ; Invoke system call to write prompt

    ; Read the second number input by the user and add it to the first number
    mov     rax, 0        ; Load system call number for read into rax
    mov     rsi, 0        ; Load file descriptor for stdin into rsi
    mov     rdi, 0        ; Load address to store input into rdi
    syscall              ; Invoke system call to read user input
    add     r8, rax       ; Add the second input to the first input and store in r8

;-----------------------------------------------------------------------------------
    ; Display result message
    mov     rax, 1        ; Load system call number for write into rax
    mov     rdi, 1        ; Load file descriptor for stdout into rdi
    mov     rsi, result   ; Load address of result message into rsi
    mov     rdx, 12       ; Load length of result message into rdx
    syscall              ; Invoke system call to write result message

    ; Display the sum stored in register r8
    mov     rax, 1        ; Load system call number for write into rax
    mov     rdi, 1        ; Load file descriptor for stdout into rdi
    mov     rsi, r8       ; Load the sum stored in r8 into rsi
    mov     rdx, 10       ; Load length of the sum into rdx
    syscall              ; Invoke system call to write the sum

    ; Call the newLine subroutine to print a newline
    call    newLine      ; Invoke subroutine to print a newline

;-----------------------------------------------------------------------------
    ; Display prompt for entering the first number again
    mov     rax, 1        ; Load system call number for write into rax
    mov     rdi, 1        ; Load file descriptor for stdout into rdi
    mov     rsi, prompt  ; Load address of prompt message into rsi
    mov     rdx, 14       ; Load length of prompt message into rdx
    syscall              ; Invoke system call to write prompt

    ; Read the first number input by the user and push it onto the stack
    mov     rax, 0        ; Load system call number for read into rax
    mov     rsi, 0        ; Load file descriptor for stdin into rsi
    mov     rdi, 0        ; Load address to store input into rdi
    syscall              ; Invoke system call to read user input
    push    rax          ; Push the first input onto the stack

    ; Display prompt for entering the second number again
    mov     rax, 1        ; Load system call number for write into rax
    mov     rdi, 1        ; Load file descriptor for stdout into rdi
    mov     rsi, prompt  ; Load address of prompt message into rsi
    mov     rdx, 14       ; Load length of prompt message into rdx
    syscall              ; Invoke system call to write prompt

    ; Read the second number input by the user and push it onto the stack
    mov     rax, 0        ; Load system call number for read into rax
    mov     rsi, 0        ; Load file descriptor for stdin into rsi
    mov     rdi, 0        ; Load address to store input into rdi
    syscall              ; Invoke system call to read user input
    push    rax          ; Push the second input onto the stack
    push    0             ; Push an additional value to maintain stack alignment

    ; Call the Adder2 subroutine to add the two inputs on the stack
    call    Adder2      ; Invoke subroutine to add the two inputs

;-----------------------------------------------------------------------------
    ; Display result message
    mov     rax, 1        ; Load system call number for write into rax
    mov     rdi, 1        ; Load file descriptor for stdout into rdi
    mov     rsi, result   ; Load address of result message into rsi
    mov     rdx, 12       ; Load length of result message into rdx
    syscall              ; Invoke system call to write result message

    ; Display the sum stored in register r8
    pop     rax          ; Pop the result of the addition from the stack into rax
    mov     rdi, rax      ; Move the result into rdi for syscall
    mov     rax, 1        ; Load system call number for write into rax
    mov     rsi, rdi      ; Move the result into rsi for syscall
    mov     rdx, 10       ; Load length of the result into rdx
    syscall              ; Invoke system call to write the sum

    ; Call the newLine subroutine to print a newline
    call    newLine      ; Invoke subroutine to print a newline

    ; Stop program execution by making a syscall to exit
    mov     rax, 60       ; Load system call number for exit into rax
    xor     rdi, rdi      ; Clear rdi (exit code)
    syscall              ; Invoke system call to exit program
;----------------------------------------------------------------------------------
Adder2:
    ; Pop num2 from the stack, pop num1 from the stack,
    ; add num1 and num2, push the sum onto the stack, and return from subroutine
    pop     rbx          ; Pop the second number from the stack into rbx
    pop     rax          ; Pop the first number from the stack into rax
    add     rax, rbx     ; Add the two numbers
    push    rax          ; Push the sum onto the stack
    ret                   ; Return from subroutine

newLine:
    ; Display a newline by making a syscall to write newline characters,
    ; and return from subroutine
    mov     rax, 1        ; Load system call number for write into rax
    mov     rdi, 1        ; Load file descriptor for stdout into rdi
    mov     rsi, crlf     ; Load address of newline characters into rsi
    mov     rdx, 2        ; Load length of newline characters into rdx
    syscall              ; Invoke system call to write newline
    ret                   ; Return from subroutine
