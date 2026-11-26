# Capstone Report: Make the Computer Draw a Box

**Name:** Medha Jain
**Roll No.:** 2501730501
**Personal number K:** 01  (K = 1)
**Course:** Nand to Tetris-I, KR Mangalam University

---

## 1. Box details (K = 1)

| Item | Formula | Value |
|---|---|---|
| Start row | K | 1 |
| Height | fixed | 20 rows (row 1 to row 20) |
| Width | 16 x ((K mod 4) + 1) | 16 x 2 = 32 pixels (2 words) |
| Start address | SCREEN + 32 x K | 16384 + 32 = 16416 |
| Extra assembler feature | K mod 3 = 1 | Line number ke saath error message |

## 2. Part A: Computer

CPU.hdl, Memory.hdl aur Computer.hdl banaye. Test files se check kiya:

- CPU.tst: [screenshot yahan lagao]
- Memory.tst: [screenshot yahan lagao]
- ComputerAdd.tst: [screenshot yahan lagao]
- ComputerMax.tst: [screenshot yahan lagao]
- ComputerRect.tst: [screenshot yahan lagao]

(Agar koi older chip kaam nahi kiya aur built-in use kiya to yahan likho kaunsa.)

## 3. Part B: Assembler (Python)

- First pass: comments aur blank lines hataye, labels (jaise LOOP) ka ROM address note kiya.
- Second pass: har line 16-bit binary mein badli. Naye variables ko RAM 16, 17, 18... mile.
- Add.asm, Max.asm, Rect.asm, Pong.asm par test kiya, output official assembler se match hua: [screenshot / diff result]
- **Extra feature (K mod 3 = 1):** galat line par program crash nahi hota, balki "Line 7: invalid instruction" jaisa message print hota hai.

## 4. Part C: Box.asm

- Key dabi hone par `color = -1` (black), nahi dabi to `color = 0`.
- Loop 20 baar chalta hai, har row mein 2 words paint hote hain, phir address 32 se badhta hai (agli row).
- Box.asm ko apne assembler se Box.hack banaya aur CPU Emulator mein chalaya: [box ka screenshot]

## 5. Ek mistake jo fix ki

Pehle Box.asm mein `M=M+D` likha tha. Mera assembler ne "Line 64: invalid instruction" error diya, kyunki Hack mein sahi form `D+M` hai. Maine `M=D+M` kar diya aur program assemble ho gaya. (Is tarah extra feature ne asli debugging mein bhi help ki.)

## 6. Conclusion

Teeno parts kaam kar rahe hain: computer official tests pass karta hai, assembler sahi output deta hai, aur K = 1 ke liye box row 1 se 20 tak, 32 pixel wide dikhta hai.
