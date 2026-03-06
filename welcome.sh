#!/bin/bash
stato="$HOME/.zenith_visited"
if [ ! -f "$stato" ]; then
	echo -E " __      				__       .__                              
/  \    /  \ ____ |  |   ____  ____   _____   ____  
\   \/\/   // __ \|  | _/ ___\/  _ \ /     \_/ __ \ 
 \        /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/ 
  \__/\  /  \___  >____/\___  >____/|__|_|  /\___  >
       \/       \/          \/            \/     \/ 
       Welcome to Zenith by ZenithDevss"
	touch "$stato"
else
	CITAZIONI=(
		"\"I computer sono incredibilmente veloci, accurati e stupidi. Gli uomini sono incredibilmente lenti, inaccurati e intelligenti. L'insieme dei due costituisce una forza incalcolabile\" - Albert Einstein"
		"\"La parte più difficile nella vita di un programmatore è quando si da la caccia ad un bug per una settimana, si trova il codice che genera il bug, si offende l'autore del codice ed infine ci si accorge di essere l'autore del codice maledetto.\" - Alepane"
		"\"La Microsoft non è male, fa solo dei sistemi operativi davvero merdosi.\" - Linus Torvalds"
		"\"Quando dici: Ho scritto un programma che manda in crash Windows, la gente ti guarda stupita e ti dice: Hey, ce l'ho nel sistema, *gratis*\" - Linus Torvalds"
		"\"Ricorda che se funziona e non sai il motivo, non toccare più quella cosa\" - Linux Community"
		)
	echo "${CITAZIONI[$RANDOM % ${#CITAZIONI[@]}]}"
fi
	
