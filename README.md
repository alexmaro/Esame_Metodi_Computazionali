# Esame_Metodi_Computazionali
Repository per contenere il codice dell'esame di metodi computazionali di Alessandro Marini

Il codice è stato pensato per essere interattivo, quindi dare quanta più possibilità di scelta all'utente, e non semplicemente come un codice monouso.
Proprio per questo motivo, sono state inoltre predisposte alcune idee e parti di codice per eventuali futuri upgrade al progetto.

Il codice è diviso in 5 parti:
-la parte zero con la definizione di tutte le varie classi, funzioni e costanti
-la prima in cui si risponde alla prima domanda (ovvero viene ottimizzato il parametro del numero di pixel)
-la seconda in cui viene mostrato come al variare della dimensione del filtro più piccolo vari la qualità della risoluzione del macchinario
-la terza in cui vengono mostrate le prestazini dello strumento con alcune funzioni aggiuntive
-la quarta in cui viene simulato uno spettrometro per materiali (dove codice è predispsto per poter essere utilizzato con qualunque altro materiale, e quindi sarebbe facilmente upgradabile ad un sistema che fa scegliere in live tramite input la molecola analizzare) 



Nel dettaglio:
0) Su questa parte c'è poco da spiegare dato che è abbastanza autoesplicativa, con dichiarazioni di classi e funzioni ad hoc per facilitare il processo di simulazione ed un eventuale upgrade di questo

1) Nella prima parte viene utilizzato un processo di minimizzazione sul numero di pixel necessari a distinguere gli isotopi con massa variabile da 1 a 210 con risoluzione 1, processo che dimostra come per questa risoluzione basta avere 210 pixel, dato che, a causa dell'incertezza sulla posizione iniziale del pixel quello che fa la differenza sulla qualità delle rilevazioni non sarà tanto questo numero, ma quanto è collimato il fascio di ioni nel momento in cui entra nel campo magnetico.

2) Nella seconda parte vengono variati i parametri delle dimensioni del generatore iniziale di ioni, e delle successive due fenditure dimostrando sia quanto citato sopra, ovvero che se il fascio non viene abbastanza collimato l'incertezza sulla posizione dello ione causa la coincidenza della posizione di arrivo sullo schermo di ioni di masse simili, e viene anche dimostrato come al contrario se vengno collimati troppo i fasci quasi nessuno ione riesce a passare attraverso entrambe le fenditure quindi si perde la qualità della funzione di acquisizione dati dello strumento (ad esempio nell'analisi di una molecola)

3) Nella terza parte viene mostrarti il funzionamento e le prestazioni vere e porprie della macchina, in questo punto ho aggiunto di mia volontà per rendere il programma interattivo la possibilità di scelta della massa dello ione che viene deflesso, massa che poi subisce un processo di randomizzazione gaussiana della stessa attorno al valore centrale stabilito, cosi da mostrare come tutti gli iosotopi vengono distinti anche se sono in quantità casuale 

4) Nella quarta ed ultima sezione viene simulato un analizzatore di molecole, viene data la scelta se selezionare la prima o la seconda e vengono mostrate anche le abbondanze isotopiche, il codice è inoltre predisposto per un eventuale modifica che come dicevo sopra permetterebbe all'utente di scegliere una molecola o comunque un insieme di ioni e atomi qualsiasi semplicemente scrivendo in input la formula e le quantità percentuali (dato come è sturtturato il codice basterebbe infatti scrivere qualche riga che estrapoli le singole informazioni dall'input e le metta all'interno della lista molecola che poi una volta messa nel codice presente verrebbe perfettamente analizzata)
