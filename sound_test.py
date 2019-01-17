import os
from subprocess import call 
SeatNo=5
test="Emergency at Seat numnber "
test+=str(SeatNo)
f= open("Emer.txt","w")
f.write(test)
f.close
call(["espeak", "-f", "Emer.txt", "-w emergency.wav"])

