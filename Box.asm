// Box.asm  (Capstone Part C)
// Roll no 2501730501 -> K = 01
//
// Box ki details:
//   Start row   = K            = 1
//   Height      = 20 rows      (row 1 se row 20)
//   Width       = 16 x ((K mod 4) + 1) = 16 x 2 = 32 pixels = 2 words
//   Start addr  = SCREEN + 32*K = 16384 + 32 = 16416
//
// Key dabi hai  -> black box (-1)
// Key chhoda    -> box gayab (0)

(MAIN)
    // check karo koi key dabi hai ya nahi
    @KBD
    D=M

    @PRESSED
    D;JNE

    // key nahi dabi -> color = 0 (white)
    @color
    M=0

    @START
    0;JMP

(PRESSED)
    // key dabi hai -> color = -1 (black)
    @color
    M=-1

(START)
    // addr = SCREEN + 32 (row 1 ka pehla word)
    @SCREEN
    D=A
    @32
    D=D+A
    @addr
    M=D

    // rows = 20
    @20
    D=A
    @rows
    M=D

(ROWLOOP)
    // word 0 paint karo
    @color
    D=M
    @addr
    A=M
    M=D

    // word 1 paint karo (agla word)
    A=A+1
    M=D

    // addr = addr + 32 (agli row)
    @32
    D=A
    @addr
    M=D+M

    // rows = rows - 1, jab tak 0 na ho loop karo
    @rows
    MD=M-1
    @ROWLOOP
    D;JGT

    // wapas key check par
    @MAIN
    0;JMP
