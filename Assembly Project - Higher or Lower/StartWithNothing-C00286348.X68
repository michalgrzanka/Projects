*-----------------------------------------------------------
* Title         :  Random seeded number guessing game
* Date Started  :  28/02/2024
* Written by    :  Michal Grzanka // C00286348
* Description   :  This very simple game prompts the user to enter a seed
*                  number and then generates a random number based
*                  on the seed. The user is then asked to guess the
*                  random number. After each guess, the program
*                  provides feedback if the guess is higher or lower
*                  than the generated number until the correct
*                  number is guessed. A fun prize is given at the end for the winner
*-----------------------------------------------------------
    ORG    $1000
START:                  
    
    ; Prompt the user to enter a seed number
    LEA     PROMPTSEED,A1
    MOVE    #14,D0         ; Display string
    TRAP    #15            ; Trap for output
    
    ; Read seed number from user input
    MOVE    #4,D0          ; Read integer input
    TRAP    #15            ; Trap for input
    
    ; Calculate random number based on the seed
    MOVE    #7,D2          ; Multiply seed by 7
    MULU    D1,D2          ; Not really random but works
    ADD     #34,D2         ; Add 34 to the result (Can change the calculations to suit user)
    
    ; Display message asking user to guess the number
    LEA     SECRET,A1
    MOVE    #14,D0         ; Display string
    TRAP    #15            ; Trap for output
    
MAIN_LOOP:
    ; Read user's guess
    MOVE    #4,D0          ; Read integer input
    TRAP    #15            ; Trap for input
    
    ; Compare user's guess with the generated number
    CMP     D2,D1
    BGT     DOWN           ; Branch if guess is higher
    BLT     UP             ; Branch if guess is lower
    BEQ     DONE           ; Branch if guess is correct
    
UP:
    ; Display message indicating the guess is higher
    LEA     HIGHER,A1
    JMP     PRINT_MESSAGE  ; Jump to print message
    
DOWN:
    ; Display message indicating the guess is lower
    LEA     LOWER,A1
    JMP     PRINT_MESSAGE  ; Jump to print message
    
DONE:
    LEA     CORRECT,A1
    JMP     PRINT_DONE   ; Jump to print message
    
PRINT_MESSAGE:
    MOVE    #14,D0         ; Display string
    TRAP    #15            ; Trap for output
    BRA     MAIN_LOOP      ; Restart the main loop
    
    
    ; Load address of the trophy string     
 
PRINT_DONE:
    MOVE    #14,D0         ; Display string
    TRAP    #15            ; Trap for output
    
    LEA     TROPHY1,A1
    MOVE    #14,D0         ; Display string
    TRAP    #15            ; Trap for output
    
    JMP     END_PRINTING   





END_PRINTING:
    SIMHALT                    
; Strings
HIGHER      DC.B    'Go higher + ',13,10,0   ; Message for higher guess
LOWER       DC.B    'Go lower - ',13,10,0    ; Message for lower guess
CORRECT     DC.B    'CORRECT!!. ',13,10,0   ; Message for correct guess
TROPHY1            DC.B        '________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ',13,10
TROPHY2            DC.B        '________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ',13,10
TROPHY3            DC.B        '___¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ',13,10
TROPHY4            DC.B       ' _¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ',13,10
TROPHY5            DC.B       ' ¶¶¶¶______¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_______¶¶¶¶ ',13,10
TROPHY6            DC.B      '  ¶¶¶_______¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶¶¶ ',13,10
TROPHY7            DC.B      '  ¶¶________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶________¶¶¶ ',13,10
TROPHY8            DC.B      '  ¶¶¶_____¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶______¶¶¶ ',13,10
TROPHY9            DC.B      '  ¶¶¶____¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶____¶¶¶¶ ',13,10
TROPHY10            DC.B      ' _¶¶¶___¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶____¶¶¶ ',13,10
TROPHY11            DC.B      ' _¶¶¶¶___¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶__¶¶¶¶ ',13,10
TROPHY12            DC.B      ' ___¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶ ',13,10
TROPHY13            DC.B      ' ____¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶¶¶ ',13,10
TROPHY14           DC.B      '  ______¶¶¶¶¶¶__¶¶¶¶¶¶¶¶¶¶¶¶¶¶___¶¶¶¶¶¶ ',13,10
TROPHY15            DC.B      ' _______________¶¶¶¶¶¶¶¶¶¶¶¶ ',13,10
TROPHY16            DC.B      ' _________________¶¶¶¶¶¶¶¶ ',13,10
TROPHY17            DC.B      ' ___________________¶¶¶¶ ',13,10
TROPHY18            DC.B      ' ___________________¶¶¶¶ ',13,10
TROPHY19            DC.B      ' ___________________¶¶¶¶ ',13,10
TROPHY20            DC.B      ' ___________________¶¶¶¶ ',13,10
TROPHY21            DC.B      ' _______________¶¶¶¶¶¶¶¶¶¶¶¶ ',13,10
TROPHT22            DC.B      ' ____________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ',13,10
TROPHY23            DC.B      ' ____________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶  ',13,10
TROPHY24            DC.B      ' ____________¶¶¶____________¶¶¶ ',13,10
TROPHY25            DC.B      ' ____________¶¶¶____________¶¶¶ ',13,10
TROPHY26            DC.B      ' ____________¶¶¶____________¶¶¶ ',13,10
TROPHY27            DC.B      ' ____________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ',13,10
TROPHY28            DC.B      ' ____________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ',13,10
TROPHY29            DC.B      ' __________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ',13,10
TROPHY30            DC.B      ' _________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶',13,10


PROMPTSEED  DC.B    'Please enter in a seed (number):. ',0  ; Prompt for seed input
SECRET      DC.B    'Now guess the random number. ',13,10,0 ; Message for guessing

    END     START   
    
    
    
    
;END NOTES:
;   If i was to do this project again I would try to get a real randomu number genearotor working in this code
;   I would also fix the 'seed number prompt' message being printed at the end. (the simulator froze when i moved the strings from after the trophy image to before, and idk why)
;   I would also dedicated more time to this project as I had alot of failed games that I overcomplicated as to get high marks but I had to fall back upon this as my plan B
;   This is a simple beginning and guidline to start any games with random possibilites such as gambling games (poker blackjack), or even a story game
o 


*~Font name~Courier New~
*~Font size~10~
*~Tab type~1~
*~Tab size~4~
