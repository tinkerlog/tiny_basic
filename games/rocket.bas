1 REM rocket.bas, adapted to run on tiny basic. 
2 REM Origin: https://github.com/coding-horror/basic-computer-games
10 PRINT TAB(30); "ROCKET"
20 PRINT TAB(15);"CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY"
30 PRINT ""
31 PRINT ""
32 PRINT ""
70 PRINT "LUNAR LANDING SIMULATION"
80 PRINT "----- ------- ----------"
81 PRINT ""
100 PRINT "DO YOU WANT INSTRUCTIONS (1=YES OR 2=NO)",
101 INPUT A
110 IF A=2 THEN GOTO 390
160 PRINT""
200 PRINT"YOU ARE LANDING ON THE MOON AND AND HAVE TAKEN OVER MANUAL"
210 PRINT"CONTROL 1000 FEET ABOVE A GOOD LANDING SPOT. YOU HAVE A DOWN-"
220 PRINT"WARD VELOCITY OF 50 FEET/SEC. 150 UNITS OF FUEL REMAIN."
225 PRINT""
230 PRINT"HERE ARE THE RULES THAT GOVERN YOUR APOLLO SPACE-CRAFT:"
231 PRINT""
240 PRINT"(1) AFTER EACH SECOND THE HEIGHT, VELOCITY, AND REMAINING FUEL"
250 PRINT"    WILL BE REPORTED VIA DIGBY YOUR ON-BOARD COMPUTER."
260 PRINT"(2) AFTER THE REPORT A '?' WILL APPEAR. ENTER THE NUMBER"
270 PRINT"    OF UNITS OF FUEL YOU WISH TO BURN DURING THE NEXT"
280 PRINT"    SECOND. EACH UNIT OF FUEL WILL SLOW YOUR DESCENT BY"
290 PRINT"    1 FOOT/SEC."
310 PRINT"(3) THE MAXIMUM THRUST OF YOUR ENGINE IS 30 FEET/SEC/SEC"
320 PRINT"    OR 30 UNITS OF FUEL PER SECOND."
330 PRINT"(4) WHEN YOU CONTACT THE LUNAR SURFACE. YOUR DESCENT ENGINE"
340 PRINT"    WILL AUTOMATICALLY SHUT DOWN AND YOU WILL BE GIVEN A"
350 PRINT"    REPORT OF YOUR LANDING SPEED AND REMAINING FUEL."
360 PRINT"(5) IF YOU RUN OUT OF FUEL THE '?' WILL NO LONGER APPEAR"
370 PRINT"    BUT YOUR SECOND BY SECOND REPORT WILL CONTINUE UNTIL"
380 PRINT"    YOU CONTACT THE LUNAR SURFACE."
381 PRINT""
390 PRINT"BEGINNING LANDING PROCEDURE.........."
391 PRINT""
400 PRINT"G O O D  L U C K ! ! !"
420 PRINT""
421 PRINT""
430 PRINT"SEC  FEET      SPEED     FUEL     PLOT OF DISTANCE"
450 PRINT""
455 LET T=0
456 LET H=1000
457 LET V=50
458 LET F=150
490 PRINT T;TAB(6);H;TAB(16);V;TAB(26);F;TAB(35);"I";TAB(H/15+35);"*"
500 INPUT B
510 IF B<0 THEN GOTO 650
520 IF B>30 THEN LET B=30
530 IF B>F THEN LET B=F
540 LET W=V-B+5
560 LET F=F-B
570 LET H=H-0.5*(V+W)
580 IF H<=0 THEN GOTO 670
590 LET T=T+1
600 LET V=W
610 IF F>0 THEN GOTO 490
615 IF B=0 THEN GOTO 640
620 PRINT"**** OUT OF FUEL ****"
640 PRINT T;TAB(4);H;TAB(12);V;TAB(20);F;TAB(29);"I";TAB(H/12+29);"*"
650 LET B=0
660 GOTO 540
670 PRINT"***** CONTACT *****"
680 LET H=H+0.5*(W+V)
690 IF B=5 THEN GOTO 720
700 LET D=(-V+SQR(V*V+H*(10-2*B)))/(5-B)
710 GOTO 730
720 LET D=H/V
730 LET W=V+(5-B)*D
760 PRINT"TOUCHDOWN AT";T+D;"SECONDS."
770 PRINT"LANDING VELOCITY=";W;"FEET/SEC."
780 PRINT F;"UNITS OF FUEL REMAINING."
790 IF W<>0 THEN GOTO 810
800 PRINT"CONGRATULATIONS! A PERFECT LANDING!!"
805 PRINT"YOUR LICENSE WILL BE RENEWED.......LATER."
810 IF ABS(W)<2 THEN GOTO 840
820 PRINT"***** SORRY, BUT YOU BLEW IT!!!!"
830 PRINT"APPROPRIATE CONDOLENCES WILL BE SENT TO YOUR NEXT OF KIN."
840 PRINT""
841 PRINT""
842 PRINT""
850 PRINT"ANOTHER MISSION",
851 INPUT A
860 IF A=1 THEN GOTO 390
870 PRINT"" 
871 PRINT "CONTROL OUT."
872 PRINT""
999 END