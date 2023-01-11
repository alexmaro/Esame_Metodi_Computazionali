#spettrometro di massa con selettore di velocità BY ALESSANDRO MARINI

"""IN TUTTO IL CODICE SONO SCRITTE DIVERS PARTI E SPUNTI FRA TRIPLI APICI DOVE IPOTIZZO UN POSSIBILE CODICE ALTERNATIVO PER UNA 
SIMULAZIONE PIU COMPLETA 3-DIMENSIONALE E DETTAGLIATA, SUPPONENDO DI AVER RICEVUTO PIU DATI INIZIALI RIGUARDO AL PROBLEMA"""

import sys
import numpy as np
import scipy
import matplotlib.pyplot as plt

"""
B_ = #Campo magnetico selettore
E_ = #campo elettrico selettore
v_uscita = #dal generatore di ioni iniziale
lunghezza_selettore =
ddp = #differenza di potenziale che accellera gli ioni dopo la prima fenditura
"""

#Informazioni di Default sullo spettrometro
v_selezionata = pow(10,5) # = E_ / B_  [in m/s]
B_default = 0.1 #[in T] 
q_default = 1.602 * pow(10,-19) #[in kg]

#dimensione e posizione generatore di ioni [m]
p_alto_generatore = 0.055#0.0555
p_basso_generatore = 0.0525#0.052
pos_x_generatore = -20

#Prima Fenditura A1 ()
p_alto_A1 = 0.055 #punto piu alto 0.1
p_basso_A1 = 0.05  #punto piu basso della fenditura  0
pos_x_A1 = -10 #distanza della fenditura A1 dall origine (ho messo meno poiche è prima dell'origine)
""" se avessi avuto piu informazioni per lavorare in 3D avrei aggiunto: 
A1_depth = 0.1 #larghezza """

#Seconda Fenditura A2 (10 micrometri)
p_alto_A2 =  0.0555#0.05 
p_basso_A2 = 0.0525#0.045  #punto piu basso della fenditura
pos_x_A2 = -5 #distanza della fenditura A2 dall origine (ho messo meno poiche è prima dell'origine)
""" se avessi avuto piu informazioni per lavorare in 3D avrei aggiunto: 
A2_depth = 0.1 #larghezza """

#Dimensione schermo [m]
p_alto_Schermo = 4.5
p_basso_Schermo = 0

#formula del raggio di curvatura di una carica elettrica deviata da un campo magnetico B_curv
def eq_raggio(m,v,q,B_curv):
    r = (m*v)/(q*B_curv) 
    return r

def forza_magentica(q,v,B):
    F = q*v*B
    return F

def forza_elettrica(q,E):
    F = q*E
    return F

#definisco la formula di conversione degli angoli da gradi a radianti
def to_radianti(gradi):
    radianti = (gradi*(np.pi))/180
    return radianti 

#DEFINISCO L'OGGETTO IONE
class Ione:
    def __init__(self, numero, x, y, z, vx, vy, vz, massa):
        self.numero = numero
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.massa = massa * (1.67 * pow(10,-27))

    def __str__(self):
        s = "Ione #" + str(self.numero) + " di massa " + str(self.massa) + " e altezza " + str(self.z)
        return s

    def mostra_z(self):
        return self.z

    def mostra_massa(self):
        return str(self.massa)

    def mostra_numero(self):
        return int(self.numero)

    def modifica_posizione_x(self, new_pos):
        self.x = new_pos
        return 1

    def modifica_posizione_z(self, new_posz):
        self.z = new_posz
        return 1


#DEFINISCO L'OGGETTO FASCIO DI IONI
class Fascio:
    def __init__(self,numero_ioni):
        self.Insieme_ioni = []
        self.numero_ioni = numero_ioni
        self.lista_masse_pesi = [[0,0]] #masse / pesi

    def aggiungi_ione(self, Ione):
        self.Insieme_ioni.append(Ione)
        return 1

    def mostra_ione(self, i):
        return self.Insieme_ioni[i]
    
    def perdo_ione(self, i):
        self.Insieme_ioni[i] = 0
        self.numero_ioni = self.numero_ioni - 1
        return 1

    def attuale_num_ioni(self):
        return int(self.numero_ioni)

    def svuota_zeri(self):
        for i in reversed(range(len(self.Insieme_ioni))):
            if self.Insieme_ioni[i] == 0:
                self.Insieme_ioni.pop(i)
        return 1
                
    def aggiungi_massa_pesi(self, massa):
        massa = int(massa)
        trovato = False
        provato = False
        for i in range(len(self.lista_masse_pesi)):
            if (self.lista_masse_pesi[i][0] == massa):
                self.lista_masse_pesi[i][1] = self.lista_masse_pesi[i][1] + 1
                trovato = True
            elif (i == len(self.lista_masse_pesi)-1):
                provato = True
        if (trovato == False and provato == True):
            self.lista_masse_pesi.append([massa,1])
        return 1

    def rimuovi_peso_massa (self, massa):
        massa = int(massa)
        for i in range(len(self.lista_masse_pesi)):
            if (self.lista_masse_pesi[i][0] == massa):
                self.lista_masse_pesi[i][1] = self.lista_masse_pesi[i][1] - 1
        return 1

    def mostra_massa_pesi(self):
        return self.lista_masse_pesi


# DEFINISCO L'OGGETTO SCHERMO
class Schermo:
    def __init__(self,numero_pixel, high, low):
        self.numero_pixel = numero_pixel
        self.high = high #punto piu in alto dello schermo
        self.low = low #punto piu in basso dello schermo
        self.lista_pixel = []
        self.lista_rivelazioni = []

    def aggiungi_ls_rivel(self, rivelato):
        self.lista_rivelazioni.append(rivelato)
        return 1

    def mostra_ls_rivel(self):
        return self.lista_rivelazioni

    def mostra_num_pixel(self):
        return(int(self.numero_pixel))

    def aggiungi_pixel(self, pixel):
        self.lista_pixel.append(pixel)
        return 1

    def mostra_pixel(self, i):
        return self.lista_pixel[i]

    def modifica_num_pixel (self, nuovo_num_pixel):
        self.numero_pixel = int(nuovo_num_pixel)
        return 1

    def mostra_altezza (self): #mostra la dimensione dello schermo
        return (float(self.high) - float(self.low))

    def arriva_ione (self, Ione_n, num_ione):
        #itera tutti i pixel fino a trovare quello giusto e modifica il numero di rilevazioni di quel pixel
        for j in range(1,self.mostra_num_pixel(),1):
            if((self.low + (self.lista_pixel[j].mostra_dimensione() * (j+1))) > Ione_n) and ((self.low+(self.lista_pixel[j].mostra_dimensione() * (j))) <= Ione_n): #se il raggio di deflessione dell i esimo ione è compreso fra il pixel j-1 esimo e il j esimo lo conta sul j esimo pixel           
                self.lista_pixel[j].ione_rilevato()
                print(f"Ione #{num_ione} rilevato nel sensore {j}")
        return 1

    def arriva_ione_no_output (self, Ione_n, num_ione):
        #itera tutti i pixel fino a trovare quello giusto e modifica il numero di rilevazioni di quel pixel
        for j in range(1,self.mostra_num_pixel(),1):
            if((self.low + (self.lista_pixel[j].mostra_dimensione() * (j+1))) > Ione_n) and ((self.low+(self.lista_pixel[j].mostra_dimensione() * (j))) <= Ione_n): #se il raggio di deflessione dell i esimo ione è compreso fra il pixel j-1 esimo e il j esimo lo conta sul j esimo pixel           
                self.lista_pixel[j].ione_rilevato()
        return 1

    def totale_rilevazioni(self):#restituisce il numero totale di rilevazioni dello schermo
        somma = 0
        for i in self.lista_pixel:
            somma = somma + int(i.mostra_num_rilevazioni())
        return somma

#DEFINISCO L'OGGETTO PIXEL
class Pixel:
    def __init__(self, numero, dimesnione_pixel, num_rilevazioni):
        self.num_rilevazioni = num_rilevazioni
        self.dimesnione_pixel = dimesnione_pixel
        self.numero = numero

    def ione_rilevato(self):
        self.num_rilevazioni = int(self.num_rilevazioni) + 1
        return 1

    def mostra_dimensione(self):
        return float(self.dimesnione_pixel)

    def modifica_dimensione(self, nuove_dimensione):
        self.dimesnione_pixel = float(nuove_dimensione)
        return 1

    def mostra_num_rilevazioni(self):
        return int(self.num_rilevazioni)

# LOOP CODICE ATTIVO FINO A RICHIESTA SPEGNIMENTO
Acceso = True
while Acceso == True:

### Finestra di dialogo iniziale e SCELTA
    azione = input(""" ###################################################################################################\n\n
    Benvenuti nel software di simulazione di uno spettrometro di massa con selettore di velocità, cosa si desidera fare? \n
    1) Simulazioni per isotopi a scelta del macchinario con numero di pixel e larghezza della fenditura variabile per osservare l'influenza di questi parametri sulla qualità e sulla risoluzione e quindi determinare le impostazioni efficaci \n
    2) Dimostrazione con il metodo Montecarlo della deflessione nel macchinario ottimizzato di N (a scelta) ioni con massa a scelta fra 1 e 210 (variabile secondo una distribuzione Gaussiana), e grafico che dimostra la risoluzione A = 1\n 
    3) Produzione del grafico per una simulazione del macchinario con materiali a scelta (con relativa abbondanza isotopica) \n\n 
    0) ESCI \n\n""")

################################################ SCELTA 1 ##########################################################################
    if (azione == "1"):
        #Finestra di dialogo per scelta numero di massa, con filtraggio input non validi
        massa_valida = False
        while massa_valida == False:
            try:
                num_massa = input(f'Quale massa ha lo ione che si desidera simulare? [da 1 a 210] \t')
                num_massa = int(num_massa)
                if (num_massa > 0) and (num_massa <= 210):
                    num_massa = int(num_massa)   #io l ho provato random con 2, 55, 111, 160, 200, 210
                    massa_valida = True
                else:
                    print("Numero non valido")
            except:
                print('Non è un numero, riprova\n')

        decidi = False
        while decidi == False:
            try:
                scel = input(f'Opzioni: \n 1) Vuoi andare direttamente ai risultati\n 2) Vuoi vedere una ad una tutte le simulazioni (sono 48!)\n\n\t')
                scel = int(scel)
                if (scel == 1) :   #io l ho provato random con 2, 55, 111, 160, 200, 210
                    decidi = True
                elif(scel == 2):
                    decidi = True
                else:
                    print("Numero non valido")
            except:
                print('Non è un numero, riprova\n')

        lista_altezze_fenditura2 = [0.0001,0.00025,0.0005,0.001,0.0025,0.005,0.025,]
        lista_num_pixel = [220,211,213,215,220,225,230] 
        p_alto_generatore_0 = 0.1
        p_basso_generatore_0 = 0
        
        PROVO = []
        risultati = []
        for alt_fendit in range(len(lista_altezze_fenditura2)):
            for num_pixel_prova in lista_num_pixel:
                Fascio1 = Fascio(4000)
                for j in range(1000):
                    altezza = np.random.uniform(low = p_basso_generatore_0 ,high = p_alto_generatore_0, size = 1) #genero posizione casuale
                    altezza_z = float(altezza)
                    Fascio1.aggiungi_ione(Ione(j,pos_x_generatore,0,altezza,v_selezionata,0,0, num_massa-1)) #ho messo solo la velocità su x dato che non ho abbastanza informazioni per fare il programma piu completo
                    Fascio1.aggiungi_massa_pesi(num_massa-1)
                    for i in range(2):
                        Fascio1.aggiungi_ione(Ione(i,pos_x_generatore,0,altezza,v_selezionata,0,0, num_massa)) #ho messo solo la velocità su x dato che non ho abbastanza informazioni per fare il programma piu completo
                        Fascio1.aggiungi_massa_pesi(num_massa)
                    Fascio1.aggiungi_ione(Ione(j+1,pos_x_generatore,0,altezza,v_selezionata,0,0, num_massa+1)) #ho messo solo la velocità su x dato che non ho abbastanza informazioni per fare il programma piu completo
                    Fascio1.aggiungi_massa_pesi(num_massa+1)

                print(f"\n\n############## NUOVA RUN CON FENDITURE ALTE {lista_altezze_fenditura2[alt_fendit]} E {num_pixel_prova} PIXEL ##############  \n")
                print(f"\nAttualmente ci sono: {Fascio1.mostra_massa_pesi()} dove [massa ione, numero ioni presenti]\n")
                print(Fascio1.attuale_num_ioni())

                lista_non_pas2 = []
                if (scel == 1):
                    print(f"Arrivati sulla seconda fenditura quindi vediamo in base alle dimensioni della seconda fenditurà quali passano e quali no ")
                else:
                    letto3 = input(f"Arrivati sulla seconda fenditura quindi vediamo in base alle dimensioni della seconda fenditurà quali passano e quali no \n\nAVANTI\n")
                for i in range(Fascio1.attuale_num_ioni()):
                    if (Fascio1.mostra_ione(i) != 0): #siccome la distribuzione sul generatore di ioni è equiprobabile modifico solo la posizione di un estremo della fenditura l'altro lo lascio a zero
                        if ((Fascio1.mostra_ione(i).mostra_z() < 0) or (Fascio1.mostra_ione(i).mostra_z() > lista_altezze_fenditura2[alt_fendit])): #ione sbatte sulla fenditura
                            lista_non_pas2.append(i)
                            Fascio1.rimuovi_peso_massa(round(float(Fascio1.mostra_ione(i).mostra_massa())/(1.67 * pow(10,-27))))    
                            Fascio1.perdo_ione(i)
                        else:
                            Fascio1.mostra_ione(i).modifica_posizione_x(pos_x_A2) #ho aggiornato la posizione x dello ione alla seconda fenditura
                
                print(f"sono passati attraverso la fenditura A2 { Fascio1.attuale_num_ioni() } ioni su { Fascio1.attuale_num_ioni() + len(lista_non_pas2)}")      
                Fascio1.svuota_zeri() #devo rimuovere gli zeri dato che prima per non perdere il ciclo avevo sostituito gli elementi con degli zeri
                print(Fascio1.mostra_massa_pesi())
               
                Schermo1 = Schermo(num_pixel_prova,p_alto_Schermo,p_basso_Schermo) #genero lo schermo di dimensione (schermo_high - schermo_low)
                dim_pixel = Schermo1.mostra_altezza() / Schermo1.mostra_num_pixel()

                #aggiungo tutti i pixel allo schermo
                for i in range(Schermo1.numero_pixel):
                    Schermo1.aggiungi_pixel(Pixel(i,dim_pixel,0)) 

                #IONI SBATTONO SULLO SCHERMO
                for i in range( Fascio1.attuale_num_ioni() ):
                    raggio_curva = eq_raggio( float(Fascio1.mostra_ione(i).mostra_massa()) , v_selezionata, q_default, B_default) #calcolo la curvatura di questo ione
                    diametro = 2 * raggio_curva
                    Fascio1.mostra_ione(i).modifica_posizione_z(Fascio1.mostra_ione(i).mostra_z() + diametro) #modifico la posizione post curvatura
                    Schermo1.arriva_ione_no_output(Fascio1.mostra_ione(i).mostra_z(), Fascio1.mostra_ione(i).mostra_numero()) #lo ione sbatte sullo schermo

                numeri_ordinati = []
                for i in range(Schermo1.mostra_num_pixel()):
                    Schermo1.aggiungi_ls_rivel(Schermo1.lista_pixel[i].mostra_num_rilevazioni())
                    numeri_ordinati.append(i-2)

                print(f"\n \nCon #{num_pixel_prova} pixel sullo schermo ho rilevato {Schermo1.totale_rilevazioni()} su {Fascio1.attuale_num_ioni()} arrivati allo schermo")
                setup = [lista_altezze_fenditura2[alt_fendit],num_pixel_prova,Schermo1.totale_rilevazioni()]

                print(f" In teoria erano {Fascio1.mostra_massa_pesi()} e io ho rilevato :")
                setup.append(Fascio1.mostra_massa_pesi())

                for i in range(len(Schermo1.mostra_ls_rivel())):
                    if (Schermo1.mostra_ls_rivel()[i] != 0):
                        print(f"{Schermo1.mostra_ls_rivel()[i]} ioni sul pixel {i}")
                        risposte = [i+1,Schermo1.mostra_ls_rivel()[i]]
                        setup.append(risposte)
                print(f"reminder: fenditura alta {lista_altezze_fenditura2[alt_fendit]} e {num_pixel_prova} pixel")
                risultati.append(setup)
                Fascio1.svuota_zeri()
                PROVO.append(Schermo1.mostra_ls_rivel())
                #GRAFICO DEI RISULTATI
    
        print(f"\n\n\n ####################### Quindi i risultati delle simulazioni con i vari setup sono: #######################\n ")
        for k in range(len(risultati)):
            print(f"Nella simulazione {k} con {risultati[k][1]} pixel e fenditure alte {risultati[k][0]} ho trovato:")
            print(f"{risultati[k][2]} ioni su 4000, nello specifico sono arrivati (sopra teorici sotto rilevati):")
            risultati[k][3].pop(0)
            print(risultati[k][3])
            print("\n")

        print("###################################################################################################\n\n")
        print("COME SARÀ POSSIBILE VISUALIZZARE DAI GRAFICI\n")
        print("Le prime righe con grandezze delle fenditure molto piccole danno pochi risultati ")
        print("Mentre le ultime colonne sulla destra danno risultati numericamente errati a causa dei troppi pixel")
        print("Allo stesso modo però fenditure troppo larghe spesso non consentono di distinguere due ioni\n\n")
        print("DA SINISTRA A DESTRA -> Numero crescente di pixel")
        print("DA SOPRA A SOTTO ->Grandezza crescente della fenditura (verso il basso)\n\n")
        print("CARICANDO I 48 GRAFICI")
        
        numeri = [] #creazione delle liste numerate per numeri assi x dei grafici
        for a in range(49):
            sezione = []
            for b in range(len(PROVO[a])):
                sezione.append(int(b))
            numeri.append(sezione)

        #CREAZIONE DI 48 GRAFICI
        fig, axs = plt.subplots(7,7)
        axs[0,0].hist( numeri[0], weights =PROVO[0], bins=Schermo1.mostra_num_pixel(), color='black' , alpha = 0.5, label = k)
        axs[0,1].hist( numeri[1], weights =PROVO[1], bins=Schermo1.mostra_num_pixel(), color='black' , alpha = 0.5, label = k)
        axs[0,2].hist( numeri[2], weights =PROVO[2], bins=Schermo1.mostra_num_pixel(), color='black' , alpha = 0.5, label = k)
        axs[0,3].hist( numeri[3], weights =PROVO[3], bins=Schermo1.mostra_num_pixel(), color='black' , alpha = 0.5, label = k)
        axs[0,4].hist( numeri[4], weights =PROVO[4], bins=Schermo1.mostra_num_pixel(), color='black' , alpha = 0.5, label = k)
        axs[0,5].hist( numeri[5], weights =PROVO[5], bins=Schermo1.mostra_num_pixel(), color='black' , alpha = 0.5, label = k)
        axs[0,6].hist( numeri[6], weights =PROVO[6], bins=Schermo1.mostra_num_pixel(), color='black' , alpha = 0.5, label = k)
        axs[1,0].hist( numeri[7], weights =PROVO[7], bins=Schermo1.mostra_num_pixel(), color='orange' , alpha = 0.5, label = k)
        axs[1,1].hist( numeri[8], weights =PROVO[8], bins=Schermo1.mostra_num_pixel(), color='orange' , alpha = 0.5, label = k)
        axs[1,2].hist( numeri[9], weights =PROVO[9], bins=Schermo1.mostra_num_pixel(), color='orange' , alpha = 0.5, label = k)
        axs[1,3].hist( numeri[10], weights =PROVO[10], bins=Schermo1.mostra_num_pixel(), color='orange' , alpha = 0.5, label = k)
        axs[1,4].hist( numeri[11], weights =PROVO[11], bins=Schermo1.mostra_num_pixel(), color='orange' , alpha = 0.5, label = k)
        axs[1,5].hist( numeri[12], weights =PROVO[12], bins=Schermo1.mostra_num_pixel(), color='orange' , alpha = 0.5, label = k)
        axs[1,6].hist( numeri[13], weights =PROVO[13], bins=Schermo1.mostra_num_pixel(), color='orange' , alpha = 0.5, label = k)
        axs[2,0].hist( numeri[14], weights =PROVO[14], bins=Schermo1.mostra_num_pixel(), color='purple' , alpha = 0.5, label = k)
        axs[2,1].hist( numeri[15], weights =PROVO[15], bins=Schermo1.mostra_num_pixel(), color='purple' , alpha = 0.5, label = k)
        axs[2,2].hist( numeri[16], weights =PROVO[16], bins=Schermo1.mostra_num_pixel(), color='purple' , alpha = 0.5, label = k)
        axs[2,3].hist( numeri[17], weights =PROVO[17], bins=Schermo1.mostra_num_pixel(), color='purple' , alpha = 0.5, label = k)
        axs[2,4].hist( numeri[18], weights =PROVO[18], bins=Schermo1.mostra_num_pixel(), color='purple' , alpha = 0.5, label = k)
        axs[2,5].hist( numeri[19], weights =PROVO[19], bins=Schermo1.mostra_num_pixel(), color='purple' , alpha = 0.5, label = k)
        axs[2,6].hist( numeri[20], weights =PROVO[20], bins=Schermo1.mostra_num_pixel(), color='purple' , alpha = 0.5, label = k)
        axs[3,0].hist( numeri[21], weights =PROVO[21], bins=Schermo1.mostra_num_pixel(), color='lime' , alpha = 0.5, label = k)
        axs[3,1].hist( numeri[22], weights =PROVO[22], bins=Schermo1.mostra_num_pixel(), color='lime' , alpha = 0.5, label = k)
        axs[3,2].hist( numeri[23], weights =PROVO[23], bins=Schermo1.mostra_num_pixel(), color='lime' , alpha = 0.5, label = k)
        axs[3,3].hist( numeri[24], weights =PROVO[24], bins=Schermo1.mostra_num_pixel(), color='lime' , alpha = 0.5, label = k)
        axs[3,4].hist( numeri[25], weights =PROVO[25], bins=Schermo1.mostra_num_pixel(), color='lime' , alpha = 0.5, label = k)
        axs[3,5].hist( numeri[26], weights =PROVO[26], bins=Schermo1.mostra_num_pixel(), color='lime' , alpha = 0.5, label = k)
        axs[3,6].hist( numeri[27], weights =PROVO[27], bins=Schermo1.mostra_num_pixel(), color='lime' , alpha = 0.5, label = k)
        axs[4,0].hist( numeri[28], weights =PROVO[28], bins=Schermo1.mostra_num_pixel(), color='red' , alpha = 0.5, label = k)
        axs[4,1].hist( numeri[29], weights =PROVO[29], bins=Schermo1.mostra_num_pixel(), color='red' , alpha = 0.5, label = k)
        axs[4,2].hist( numeri[30], weights =PROVO[30], bins=Schermo1.mostra_num_pixel(), color='red' , alpha = 0.5, label = k)
        axs[4,3].hist( numeri[31], weights =PROVO[31], bins=Schermo1.mostra_num_pixel(), color='red' , alpha = 0.5, label = k)
        axs[4,4].hist( numeri[32], weights =PROVO[32], bins=Schermo1.mostra_num_pixel(), color='red' , alpha = 0.5, label = k)
        axs[4,5].hist( numeri[33], weights =PROVO[33], bins=Schermo1.mostra_num_pixel(), color='red' , alpha = 0.5, label = k)
        axs[4,6].hist( numeri[34], weights =PROVO[34], bins=Schermo1.mostra_num_pixel(), color='red' , alpha = 0.5, label = k)
        axs[5,0].hist( numeri[35], weights =PROVO[35], bins=Schermo1.mostra_num_pixel(), color='blue' , alpha = 0.5, label = k)
        axs[5,1].hist( numeri[36], weights =PROVO[36], bins=Schermo1.mostra_num_pixel(), color='blue' , alpha = 0.5, label = k)
        axs[5,2].hist( numeri[37], weights =PROVO[37], bins=Schermo1.mostra_num_pixel(), color='blue' , alpha = 0.5, label = k)
        axs[5,3].hist( numeri[38], weights =PROVO[38], bins=Schermo1.mostra_num_pixel(), color='blue' , alpha = 0.5, label = k)
        axs[5,4].hist( numeri[39], weights =PROVO[39], bins=Schermo1.mostra_num_pixel(), color='blue' , alpha = 0.5, label = k)
        axs[5,5].hist( numeri[40], weights =PROVO[40], bins=Schermo1.mostra_num_pixel(), color='blue' , alpha = 0.5, label = k)
        axs[5,6].hist( numeri[41], weights =PROVO[41], bins=Schermo1.mostra_num_pixel(), color='blue' , alpha = 0.5, label = k)
        axs[6,0].hist( numeri[42], weights =PROVO[42], bins=Schermo1.mostra_num_pixel(), color='green' , alpha = 0.5, label = k)
        axs[6,1].hist( numeri[43], weights =PROVO[43], bins=Schermo1.mostra_num_pixel(), color='green' , alpha = 0.5, label = k)
        axs[6,2].hist( numeri[44], weights =PROVO[44], bins=Schermo1.mostra_num_pixel(), color='green' , alpha = 0.5, label = k)
        axs[6,3].hist( numeri[45], weights =PROVO[45], bins=Schermo1.mostra_num_pixel(), color='green' , alpha = 0.5, label = k)
        axs[6,4].hist( numeri[46], weights =PROVO[46], bins=Schermo1.mostra_num_pixel(), color='green' , alpha = 0.5, label = k)
        axs[6,5].hist( numeri[47], weights =PROVO[47], bins=Schermo1.mostra_num_pixel(), color='green' , alpha = 0.5, label = k)
        axs[6,6].hist( numeri[48], weights =PROVO[48], bins=Schermo1.mostra_num_pixel(), color='green' , alpha = 0.5, label = k)

        #plt.xlabel("Numero crescente di pixel")
        #plt.ylabel("Grandezza crescente della fenditura (verso il basso)") (LE LABEL non vanno )
        plt.show()
        print("###################################################################################################\n\n")
        print("Dai risultati dei setup analizzati al variare di alcuni isotopi è risultato che la configurazione migliore per: numero minore di pixel con risoluziona A = 1, senza perdere troppi ioni a ogni run è data da ")
        print(" 213 PIXEL E LARGHEZZA DELLA FENDITURA 0.0025 m (2.5mm)\n")

################################################ SCELTA 2 ##########################################################################
    elif (azione == "2"):
        #Considerazioni iniziali (aspetto che siano lette prima di andare avanti)
        letto = input("Considero uno spettrometro di massa posizionato come segue:\n\n -Asse x: asse lungo cui si muove lo ione (da sinistra a destra) \n -Asse y: entrante nello schermo (stessa dirazione campo magnetico B \n -Asse z: dal basso verso l'alto (verso opposto al campo elettico) \n -Origine degli assi X: sulla seconda fenditura (A2) \n -Origine degli assi Y: sulla parte più bassa della fenditura A2 \n\n PREMI QUALUNQUE TASTO PER ANDARE AVANTI\n")

        #Finestra di dialogo per scelta numero di massa, con filtraggio input non validi
        massa_valida = False
        while massa_valida == False:
            try:
                num_massa = input(f'Quale massa ha lo ione che si desidera simulare? [da 1 a 210] \t')
                num_massa = int(num_massa)
                if (num_massa > 0) and (num_massa <= 210):
                    num_massa = int(num_massa) 
                    massa_valida = True
                else:
                    print("Numero non valido")
            except:
                print('Non è un numero, riprova\n')

        #Finestra di dialogo per scelta numero ioni, con filtraggio input non validi
        valido_num_ioni = False
        while valido_num_ioni == False:
            try:
                num_ioni_iniziale = input(f'Quanti ioni si desidera simulare? \t')
                num_ioni_iniziale = int(num_ioni_iniziale) 
                if (num_ioni_iniziale > 0):
                    valido_num_ioni = True
                else:
                    print("Numero non valido\n")
            except:
                print('Non è un numero, riprova\n')
    

        #GENERO UN FASCIO CON NUMERO DI IONI SCELTO PRIMA
        Fascio1 = Fascio(num_ioni_iniziale)
        #GENERAZIONE DI IONI (mi limito a generare ioni con posizione variabile sul generatore di ioni (ipotizzato bi dimensionale su xz ))
        #numeri generati pseudorandomicamente per la posizione delle particelle low = posizione punto piu basso fenditura A1, high punto piu alto 
        print(f"\n\nGenero { Fascio1.attuale_num_ioni() } sul generatore, con posizione casuale e massa casuale secondo una Gaussiana con centro massa = {num_massa} e sulle code isotopi.\n")
        for i in range( Fascio1.attuale_num_ioni() ):
            altezza = np.random.uniform(low = p_basso_generatore ,high = p_alto_generatore, size = 1) #genero posizione casuale
            altezza_z = float(altezza)
            massa_iosotopica = np.random.normal(num_massa, 0.5, 1) #genero probabilità isotopi (centro campana, deviazione standard)
            nuova_massa = round(float(massa_iosotopica)) #arrotondo la massa ad un numero intero
            Fascio1.aggiungi_ione(Ione(i,pos_x_generatore,0,altezza_z,v_selezionata,0,0, nuova_massa)) #ho messo solo la velocità su x dato che non ho abbastanza informazioni per fare il programma piu completo
            Fascio1.aggiungi_massa_pesi(nuova_massa)
        print(f"\nAttualmente ci sono: {Fascio1.mostra_massa_pesi()} dove [massa ione, numero ioni presenti]\n")

        """NEL CASO DI PIU DATI POTREI RANDOMIZZARE LE FLUTTUAZIONI SULLA VELOCITÀ DI USCITA DAL GENERATORE DI IONI"""
        """POTREI INOLTRE RANDOMIZZARE GLI ANGOLI XY E XZ DELLA VELOCITÀ VEDERE QUALI IONI PASSANO ATTRAVERSO LA PRIMA FENDIUTRA 
        SU TRE ASSI 
            v_axy = np.random.uniform(low = 0 ,high = 360) #randomizzo un angolo sul piano xy
            v_axz = np.random.uniform(low = 0 ,high = 360) #randomizzo un angolo sul piano yz
        """
        #print(Fascio1.mostra_masse())
        #PRIMA FENDITURA vedo quali ioni passsano e quali no
        lista_non_pas1 = []
        letto2 = input(f"Gli ioni appena generati stanno passando attraverso la prima fenditura quindi vediamo in base alla loro posizione di generazione quali passano e quali no \n\nAVANTI\n")
        for i in range(Fascio1.attuale_num_ioni()):
            if ((Fascio1.mostra_ione(i).mostra_z() < p_basso_A1) or (Fascio1.mostra_ione(i).mostra_z() > p_alto_A1)): #ione sbatte sulla fenditura
                lista_non_pas1.append(i)
                Fascio1.rimuovi_peso_massa(round(float(Fascio1.mostra_ione(i).mostra_massa())/(1.67 * pow(10,-27))))    
                Fascio1.perdo_ione(i)
            else:
                Fascio1.mostra_ione(i).modifica_posizione_x(pos_x_A1) #ho aggiornato la posizione x dello ione alla prima fenditura
                
        print(f"Gli ioni nuemro #{ lista_non_pas1 } non sono passati sulla fenditura A1")
        print(f"sono passati attraverso la fenditura A1 { Fascio1.attuale_num_ioni() } ioni su { Fascio1.attuale_num_ioni() + len(lista_non_pas1)}")
        Fascio1.svuota_zeri() #devo rimuovere gli zeri dato che prima per non perdere il ciclo avevo sostituito gli elementi con degli zeri

        """ 
        #ACCELERAZIONE DDP 
        CONOSCENDO LA DDP POTREI CALCOLARE LE COMPONENTI DELLA VELOCITÀ SU TRE ASSI DOPO L'ACCELLERAZIONE SUBITA DALLA DIFFERENZA DI POTENZIALE 
        """
        #DEFLESSIONE DEGLI IONI NEL SELETTORE DI VELOCITÀ
        #non c'è nessun filtraggio dato che di default tutti gli ioni hanno gia velocità 10^5 se avessi avuto più dati, quindi velocità random avrei fatto come scritto sotto
        print("\n\nGli ioni prodotti e sparati uno alla volta subiscono una deflessione nel selettore di velocità , infatti sono sottoposti ad un campo elettro magentico che lascia arrivare solo le velocità uguali a 10^5 m/s")
        """
        CONOSCENDO CAMPO ELETTRICO E MAGNETICO DEL SELETTORE POTREI CALCOLARE LE DEFLESSIONI E VEDERE QUALI IONI PASSANO E QUALI NO NEL SELETTORE ANCHE IN BASE ALLA LUNGHEZZA DEL SELETTORE E DELLA DISTANZA DI QUESTO DALLA SECONDA FENDITURA
        POTREI AGGIUNGERE SOPRA AL POSTO DI "ad un campo elettromagnetico..." ->  "sono sottoposti a \nForza elettica = -q*E \nForza magentica = q*v*B "
        E POTREI AGGIUNGERE 
        #calcolo la deflessione dovuta al campo elettico sull'asse Z
        print(f"La deflessione del selettore di velocità è solo sull'asse Z ed è data dalla forza del campo magnetico che vale: { forza_magentica(q_default,v_selezionata,B_)} e dalla forza del campo elettirco che vale { forza_elettrica(q_default, E_)}, quindi la risultante è { forza_magentica(q_default,v_selezionata,B_) + forza_elettrica(q_default, E_) }, a seguito di queste deflessioni passano solo ioni alla velocità di 10^5 m/s")
        da questa divido fratto la massa dello ione per trovare l'accelerazione a = { (forza_magentica(q_default,v_selezionata,B_) + forza_elettrica(q_default, E_))/ float(Fascio1.mostra_ione(1).mostra_massa()) }, e da qui calcolare con il tempo di volo = {(v_accelerata/lunghezza_selettore)} la deflessione sull'asse z tramite la formula z = z0 + 1/2 * accelerazione * t_volo")
        # cosi potrei simulare esattamenti di quanto sono deflessi gli ioni con determinate caratteristiche e potrei vedere se anche se da deflessi riescono a passare nella seconda fenditura (in base anche alle dimensioni di questa, alle componenti del vettore tridimenzionale velocità e alla lunghezza del selettore)
        """
        #SECONDA FENDITURA
        print(f"\nAttualmente ci sono: {Fascio1.mostra_massa_pesi()} dove [massa ione, numero ioni presenti]\n")
        lista_non_pas2 = []
        letto3 = input(f"Arrivati sulla seconda fenditura quindi vediamo in base alle dimensioni della seconda fenditurà quali passano e quali no \n\nAVANTI\n")
        for i in range(Fascio1.attuale_num_ioni()):
            if (Fascio1.mostra_ione(i) != 0):
                if ((Fascio1.mostra_ione(i).mostra_z() < p_basso_A2) or (Fascio1.mostra_ione(i).mostra_z() > p_alto_A2)): #ione sbatte sulla fenditura
                    lista_non_pas2.append(i)
                    Fascio1.rimuovi_peso_massa(round(float(Fascio1.mostra_ione(i).mostra_massa())/(1.67 * pow(10,-27))))    
                    Fascio1.perdo_ione(i)
                else:
                    Fascio1.mostra_ione(i).modifica_posizione_x(pos_x_A2) #ho aggiornato la posizione x dello ione alla seconda fenditura
        
        print(f"Gli ioni nuemro #{ lista_non_pas2 } non sono passati sulla fenditura A2")
        print(f"sono passati attraverso la fenditura A2 { Fascio1.attuale_num_ioni() } ioni su { Fascio1.attuale_num_ioni() + len(lista_non_pas2)}")      
        Fascio1.svuota_zeri() #devo rimuovere gli zeri dato che prima per non perdere il ciclo avevo sostituito gli elementi con degli zeri
        print(Fascio1.mostra_massa_pesi())

        #CAMPO MAGNETICO   
        letto4 = input(f"Gli ioni stanno venendo ruotati da un campo magnetico di intensità { B_default} tesla e vanno a sbattere contro lo schermo \n\nAVANTI\n")
        #Creo schermo
        k= 213 #numero pixel ottimizzato
        Schermo1 = Schermo(k,p_alto_Schermo,p_basso_Schermo) #genero lo schermo di dimensione (schermo_high - schermo_low)
        dim_pixel = Schermo1.mostra_altezza() / Schermo1.mostra_num_pixel()

        #aggiungo tutti i pixel allo schermo
        for i in range(Schermo1.numero_pixel):
            Schermo1.aggiungi_pixel(Pixel(i,dim_pixel,0)) 

        #IONI SBATTONO SULLO SCHERMO
        for i in range( Fascio1.attuale_num_ioni() ):
            raggio_curva = eq_raggio( float(Fascio1.mostra_ione(i).mostra_massa()) , v_selezionata, q_default, B_default) #calcolo la curvatura di questo ione
            diametro = 2 * raggio_curva
            Fascio1.mostra_ione(i).modifica_posizione_z(Fascio1.mostra_ione(i).mostra_z() + diametro) #modifico la posizione post curvatura
            Schermo1.arriva_ione(Fascio1.mostra_ione(i).mostra_z(), Fascio1.mostra_ione(i).mostra_numero()) #lo ione sbatte sullo schermo

        numeri_ordinati = []
        for i in range(Schermo1.mostra_num_pixel()):
            Schermo1.aggiungi_ls_rivel(Schermo1.lista_pixel[i].mostra_num_rilevazioni())
            if num_massa <= 43:
                numeri_ordinati.append(i-2)
            elif num_massa>43 and num_massa <= 86:
                numeri_ordinati.append(i-1)
            elif num_massa>86 and num_massa <= 129:
                numeri_ordinati.append(i+0)
            elif num_massa>129 and num_massa <= 172:
                numeri_ordinati.append(i+1)
            else:
                numeri_ordinati.append(i+2)

        print(f"\n \nCon #{k} pixel sullo schermo ho rilevato {Schermo1.totale_rilevazioni()} su {Fascio1.attuale_num_ioni()}")
        print(f"\nAl momento dello scontro con lo schemo avevo: {Fascio1.mostra_massa_pesi()} dove [massa ione, numero ioni presenti]\n")

        #GRAFICO DEI RISULTATI
        plt.hist( numeri_ordinati, weights =Schermo1.mostra_ls_rivel(), bins=Schermo1.mostra_num_pixel(), color='orange' )
        plt.xlabel('Pixel Numero')
        plt.ylabel('Num Rilevazioni')
        plt.show()

################################################ SCELTA 3 ################################################################################À
    elif (azione == "3"):
        """CON QUESTO GENERATORE E FENDITURE PIU LARGHE VIENE PERFETTO
        p_alto_generatore = 0.055
        p_basso_generatore = 0.0525"""
        """HO SCRITTO QUESTA PARTE CON L'IDEA DI CREARE ANCHE UN'ALTRA OPZIONE CHE TI PERMETTESSE DI SCHEGLIERE IN DIRETTA LA MOLECOLA DA ANALIZZARE
        tavola_periodica = {"H": 1, "He" : 4, "Li" : 7, "Be" : 9, "B" : 11, "C" : 12, "N" : 14, "O" : 16, "F" : 19, "Ne" : 20, "Na" : 23, "Mg" : 24, "Al" : 27, "Si" : 28, "P" : 31, "S": 32, "Cl":36, "Ar":39, "K":40, "Ca":41, "Sc":45, "Ti":48, "V":51, "Cr": 52, "Mn":55, "Fe":56, "Co":59, "Ni":58, "Cu" : 63, "Zn" : 65, "Ga" : 70, "Ge" : 72	,"As" : 75	,"Se" : 79	,"Br" : 80	,"Kr" : 84	,"Rb" : 85	,"Sr" : 88	,"Y" :  89	,"Zr" : 91, "Nb" : 93,"Mo" : 96	,"Tc" : 98	,"Ru" : 101	,"Rh" : 103	,"Pd" : 106	,"Ag" : 108	,"Cd" : 113	,"In" : 115	,"Sn" : 119	,"Sb" :  122	,"Te" : 128	,"I" :  127	,"Xe" : 131	,"Cs" : 133	,"Ba" : 137	,"La" : 139	,"Ce" : 140	,"Pr" : 141	,"Nd" : 144	,"Pm" : 145	,"Sm" : 150	,"Eu" : 152	,"Gd" : 157	,"Tb" : 159	,"Dy" : 162	,"Ho" : 165	,"Er" : 167	,"Tm" : 169	,"Yb" : 173, "Lu" : 175 ,"Hf" : 178 ,"Ta" : 181	,"W" :  183	,"Re" : 186	,"Os" : 190	,"Ir" : 192	,"Pt" : 195	,"Au" : 197	,"Hg" : 200	,"Tl" : 204	,"Pb" : 207  ,"Bi" : 208	,"Po" : 209	,"At" : 210	,"Rn" : 86	,"Fr" : 87	,"Ra" : 88	,"Ac" : 89	,"Th" : 90	,"Pa" : 91	,"U" :  92	,"Np" : 93	,"Pu" : 94	,"Am" : 95	,"Cm" : 96	,"Bk" : 97	,"Cf" : 98	,"Es" : 99	,"Fm" : 100		,"Md" : 101	,"No" : 102	,"Lr" : 103	,"Rf" : 104	,"Db" : 105		,"Sg" : 106	  ,"Bh" : 107	,"Hs" : 108	,"Mt" : 109	,"Ds" : 110	,"Rg" : 111	,"Cn" : 112	,"Nh" : 113	 ,"Fl" : 114	,"Mc" : 115	,"Lv" : 116	,"Ts" : 117	,"Og" : 118}
        """
        def calcola_abbondanza_isotopica(massa_isotopo, massa_tot):
            return(float(massa_isotopo/massa_tot))

        valido_input = False
        while valido_input == False:
            try:
                scelta  = input("Quale molecola vuoi visualizzare: \n 1) 20 % (10)B , 80% (11)B \n 2) 10 % (9)Be, 62% (16)O, 7% (27)Al, 19% (28)Si, 1% 29(Si), 0.6% (30)Si, 0,36% (52)Cr, 0.04% (53)Cr \n \n")
                if (scelta == str(1) or scelta == str(2)):
                    valido_input = True
                else:
                    print("Numero non valido\n")
            except:
                print('Non è un numero, riprova\n')
      
########PRIMA MOLECOLA        
        if (scelta == "1"):
            elemento1 = ["B",10,0.80] #nome, numero di massa, percenturale
            elemento2 = ["B",11,0.20]

            molecola = [elemento1, elemento2]

########SECONDA MOLECOLA
        elif (scelta == "2"):
             #10 % % (27)Al, 19% (28)Si, 1% 29(Si), 0.6% (30)Si, 0,36% (52)Cr, 0.04% (53)Cr
            elemento1 = ["Be",9,0.10] #nome, numero di massa, percenturale
            elemento2 = ["O",16,0.62]
            elemento3 = ["Al",27,0.07] 
            elemento4 = ["Si",28,0.19]
            elemento5 = ["Si",29,0.01] 
            elemento6 = ["Si",30,0.006] 
            elemento7 = ["Cr",52,0.0036]
            elemento8 = ["Cr",53,0.0004]

            molecola = [elemento1,elemento2,elemento3,elemento4,elemento5,elemento6,elemento7,elemento8]

        valido_num_ioni = False
        while valido_num_ioni == False:
            try:
                num_ioni_iniziale = input(f'Quanti ioni si desidera simulare? \t')
                num_ioni_iniziale = int(num_ioni_iniziale) 
                if (num_ioni_iniziale > 0):
                    valido_num_ioni = True
                else:
                    print("Numero non valido\n")
            except:
                print('Non è un numero, riprova\n')
    

        #GENERO UN FASCIO CON NUMERO DI IONI SCELTO PRIMA
        Fascio2 = Fascio(num_ioni_iniziale)
        #len(molecola)
        for j in range(len(molecola)):
            for i in range( round(num_ioni_iniziale * molecola[j][2]) ):
                #print(i)
                altezza = np.random.uniform(low = p_basso_generatore ,high = p_alto_generatore, size = 1) #genero posizione casuale
                altezza_z = float(altezza)
                Fascio2.aggiungi_ione(Ione(i,pos_x_generatore,0,altezza_z,v_selezionata,0,0,int(molecola[j][1]))) #ho messo solo la velocità su x dato che non ho abbastanza informazioni per fare il programma piu completo
                Fascio2.aggiungi_massa_pesi(int(molecola[j][1]))
            print(f"Ci sono: { Fascio2.attuale_num_ioni() * (molecola[j][2]) } atomi di {int(molecola[j][1])}{molecola[j][0]} \n")

        #FENDITURA 1
        lista_non_pas1 = []
        letto2 = input(f"Gli ioni appena generati stanno passando attraverso la prima fenditura quindi vediamo in base alla loro posizione di generazione quali passano e quali no \n\nAVANTI\n")
        for i in range(Fascio2.attuale_num_ioni()):
            if ((Fascio2.mostra_ione(i).mostra_z() < p_basso_A1) or (Fascio2.mostra_ione(i).mostra_z() > p_alto_A1)): #ione sbatte sulla fenditura
                lista_non_pas1.append(i)
                Fascio2.rimuovi_peso_massa(round(float(Fascio2.mostra_ione(i).mostra_massa())/(1.67 * pow(10,-27))))    
                Fascio2.perdo_ione(i)
            else:
                Fascio2.mostra_ione(i).modifica_posizione_x(pos_x_A1) #ho aggiornato la posizione x dello ione alla prima fenditura
                
        print(f"\n\nGli ioni nuemro #{ lista_non_pas1 } non sono passati sulla fenditura A1")
        print(f"sono passati attraverso la fenditura A1 { Fascio2.attuale_num_ioni() } ioni su { Fascio2.attuale_num_ioni() + len(lista_non_pas1)}")
        Fascio2.svuota_zeri() #devo rimuovere gli zeri dato che prima per non perdere il ciclo avevo sostituito gli elementi con degli zeri

        #FENDITURA 2
        lista_non_pas2 = []
        letto3 = input(f"\n\nGli ioni stanno passando attraverso la seconda fenditura quindi vediamo in base alla loro posizione di generazione quali passano e quali no \n\nAVANTI\n")
        for i in range(Fascio2.attuale_num_ioni()):
            if ((Fascio2.mostra_ione(i).mostra_z() < p_basso_A2) or (Fascio2.mostra_ione(i).mostra_z() > p_alto_A2)): #ione sbatte sulla fenditura
                lista_non_pas2.append(i)
                Fascio2.rimuovi_peso_massa(round(float(Fascio2.mostra_ione(i).mostra_massa())/(1.67 * pow(10,-27))))    
                Fascio2.perdo_ione(i)
            else:
                Fascio2.mostra_ione(i).modifica_posizione_x(pos_x_A2) #ho aggiornato la posizione x dello ione alla prima fenditura
                
        print(f"Gli ioni nuemro #{ lista_non_pas2 } non sono passati sulla fenditura A2")
        print(f"sono passati attraverso la fenditura A2 { Fascio2.attuale_num_ioni() } ioni su { Fascio2.attuale_num_ioni() + len(lista_non_pas2)}")
        Fascio2.svuota_zeri() #devo rimuovere gli zeri dato che prima per non perdere il ciclo avevo sostituito gli elementi con degli zeri

        #CAMPO MAGNETICO
        letto4 = input(f"\n\nGli ioni stanno venendo ruotati da un campo magnetico di intensità { B_default} tesla e vanno a sbattere contro lo schermo \n\nAVANTI\n")

        #Creo schermo
        k= 213 
        Schermo2 = Schermo(k,p_alto_Schermo,p_basso_Schermo) #genero lo schermo
        #lo schermo ha dimensione (schermo_high - schermo_low)
        dim_pixel = Schermo2.mostra_altezza() / Schermo2.mostra_num_pixel()

        #aggiungo tutti i pixel allo schermo
        for i in range(Schermo2.numero_pixel):
            Schermo2.aggiungi_pixel(Pixel(i,dim_pixel,0)) 

        #IONI SBATTONO SULLO SCHERMO
        for i in range( Fascio2.attuale_num_ioni() ):
            raggio_curva = eq_raggio( float(Fascio2.mostra_ione(i).mostra_massa()) , v_selezionata, q_default, B_default) #calcolo la curvatura di questo ione
            diametro = 2 * raggio_curva
            Fascio2.mostra_ione(i).modifica_posizione_z(Fascio2.mostra_ione(i).mostra_z() + diametro) #modifico la posizione post curvatura
            Schermo2.arriva_ione(Fascio2.mostra_ione(i).mostra_z(), Fascio2.mostra_ione(i).mostra_numero()) #lo ione sbatte sullo schermo

        numeri_ordinati = []
        for i in range(k): 
            Schermo2.aggiungi_ls_rivel(Schermo2.lista_pixel[i].mostra_num_rilevazioni())
            numeri_ordinati.append(i-2)
        print(f"\n \nCon #{k} pixel sullo schermo ho rilevato {Schermo2.totale_rilevazioni()} su {Fascio2.attuale_num_ioni()}")
        print(f"\nAl momento dello scontro con lo schemo ho: {Fascio2.mostra_massa_pesi()} dove [massa ione, numero ioni presenti]\n")
        print("Quindi calcolando le ABBONDANZE ISOTOPICHE HO")
        for i in range(len(Fascio2.mostra_massa_pesi())):
            print(f" {(calcola_abbondanza_isotopica(int(Fascio2.mostra_massa_pesi()[i][1]), int(Fascio2.attuale_num_ioni()))*100)}% abbondanza isotopica di ioni con massa {Fascio2.mostra_massa_pesi()[i][0]}")

        #GRAFICO DEL RISULTATO
        plt.hist( numeri_ordinati, weights =Schermo2.mostra_ls_rivel(), bins=Schermo2.mostra_num_pixel(), color='orange' )
        plt.xlabel('Pixel Numero')
        plt.ylabel('Num Rilevazioni')
        plt.show()
            
##################################### SCELTA 0 ########################################################################################À
    elif(azione == "0"):
        Acceso = False #spengo l'applicazione
        
    else:
        print("Inserire un numero valido\n\n\n")




       
