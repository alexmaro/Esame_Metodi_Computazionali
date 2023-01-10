# Esame_Metodi_Computazionali
Repository per contenere il codice dell'esame di metodi computazionali di Alessandro Marini

Il codice è stato pensato non semplicemente come un codice monouso ma per essere interattivo, quindi dare quanta più possibilità di scelta all'utente.
Inoltre sono state predisposte alcune idee e parti di codice per eventuali futuri upgrade al progetto segnate fra tripli apici.

Il codice è diviso in 4 parti:
-la parte zero con la definizione di tutte le varie classi, funzioni e costanti
-la prima in cui si risponde alla prima e alla terza domanda (ovvero viene ottimizzato il parametro del numero di pixel e viene mostrato sia graficamente che numericamente come varia l'efficacia e la risoluzione del macchinario al variare del numero di pixel e della dimensione delle fenditure )
-la seconda in cui vengono mostrate le prestazini dello strumento con alcune funzioni aggiuntive
-la terza in cui viene simulato uno spettrometro per materiali (dove codice è predispsto per poter essere utilizzato con qualunque altro materiale, e quindi sarebbe facilmente upgradabile ad un sistema che fa scegliere in live tramite input la molecola analizzare) 



Nel dettaglio:
0) Su questa parte c'è poco da spiegare dato che è abbastanza autoesplicativa, con dichiarazioni di classi e funzioni ad hoc per facilitare il processo di simulazione ed un eventuale upgrade di questo

1) Nella prima parte parte vengono variati i parametri delle dimensioni della fenditura A2 e e del numero di pixel che conpongono lo schermo dimostrando che se il fascio non viene abbastanza collimato dalle fenditure l'incertezza sulla posizione degli ioni causa la coincidenza della posizione di arrivo sullo schermo di ioni di masse simili, e viene anche dimostrato come al contrario se vengno collimati troppo i fasci quasi nessuno ione riesce a passare attraverso le fenditure quindi si perde performatività nella capacità di acquisizione dati dello strumento ( che puo risultare problematico ad esempio nell' ultima parti di analisi di una molecola)

3) Nella seconda parte viene mostrarti il funzionamento e le prestazioni vere e porprie della macchina, in questo punto ho aggiunto er rendere il programma interattivo la possibilità di scelta della massa dello ione che viene deflesso, massa che poi subisce un processo di randomizzazione gaussiana della stessa attorno al valore centrale stabilito, cosi da mostrare come tutti gli iosotopi vengono distinti anche se sono in quantità casuale 

4) Nella terza ed ultima sezione viene simulato un analizzatore di molecole, viene data la scelta se selezionare la prima o la seconda e vengono mostrate anche le abbondanze isotopiche, il codice è inoltre predisposto per un eventuale modifica che come dicevo sopra permetterebbe all'utente di scegliere una molecola o comunque un insieme di ioni e atomi qualsiasi semplicemente scrivendo in input la formula e le quantità percentuali (dato come è sturtturato il codice basterebbe infatti scrivere qualche riga che estrapoli le singole informazioni dall'input e le metta all'interno della lista molecola che poi una volta messa nel codice presente verrebbe perfettamente analizzata)
