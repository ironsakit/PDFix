
import requests

appunto = """Circa 50 anni fa, durante un famoso seminario al Dartmouth College, veni
va ufficialmente introdotto il termine “Intelligenza Artificiale”. Vi era allora
un’atmosfera di euforia tecnologica indotta dall’avvento del computer, una
macchina in grado di manipolare simboli, e l’intelligenza artificiale sembra
va a portata di mano. Che cosa è successo dopo? L’articolo presenta al
cuni momenti particolarmente significativi della storia dell’IA,le principali
aree di ricerca e le prospettive applicative.
1. UN NOME FORSE TROPPO
IMPEGNATIVO
Ogni disciplina scientifica è animata da
sogni e motivata da grandi progetti. Gra
zie ad essi si procede, conseguendo risultati
forse differenti rispetto a quelli immaginati,
ma spesso utili e in grado di conferire all’inte
ro programma un significato che sovente va
al di là delle speranze e degli obiettivi origi
nali. Accade anche di conseguire, talora, ri
sultati inaspettati e originariamente impre
vedibili.
Qual è il sogno dei ricercatori di intelligenza
artificiale? Nella maggior parte dei casi si so
gna, cosa piuttosto ambiziosa in verità, di
realizzare quello che di certo appare come il
più inaccessibile tra i progetti scientifici: capi
re i principi e i meccanismi del funzionamento
della mente umana allo scopo di riprodurre
l’intelligenza umana su una macchina.
L’espressione “Intelligenza Artificiale” (IA)
descrive accuratamente questo sogno tradu
cendo correttamente l’obiettivo finale. Ma,
forse, se gravati da un nome meno impegna
tivo, i ricercatori di IA si sarebbero imbattuti
in minori difficoltà lungo il loro cammino. In
effetti, l’espressione “Intelligenza Artificiale”
ha innescato paure irrazionali, alimentate da
certa letteratura e cinematografia fanta
scientifiche. Anche il sarcasmo proveniente
da alcuni ambienti antiscientifici non ha gio
vato. Forse il campo avrebbe incontrato me
no ostilità se per esso fosse stata scelta la di
zione britannica – derivata da A. Turing - di
“Intelligenza delle Macchine” (IM), in quanto
essa rammenta costantemente che, per
quanto intelligenti, pur sempre di macchine
si tratta. Forse, invece, un forte dibattito era
ed è inevitabile in quanto costantemente l’IA
(o IM) mette in ballo quella che è ritenuta la
più esclusiva prerogativa degli esseri umani:
l’intelligenza.
Va aggiunto che la scelta di un’espressione
tanto forte come “Intelligenza Artificiale”
ha di certo generato aspettative eccessive,
in particolare considerando le limitazioni
della tecnologia con la quale gli artefatti in
telligenti andavano via via realizzati. D’al
tronde, qualcuno ha giustamente osservato
che ogni volta che l’IA raggiunge un nuovo
Luigia Carlucci Aiello
Maurizio Dapor
3.6
MONDO D I G I TA L E • n . 2 - g i u g n o 2 0 0 4
3
traguardo questo non è più annoverato tra i
suoi risultati ma si trasforma in un prodotto
dell’informatica tradizionale: un destino in
grato per una disciplina che, in realtà, ha
conseguito molti successi e ha facilitato la
vita di ognuno di noi. Una spiegazione di ta
le circostanza risiede nella constatazione
che l’IA parte da problemi scientifici che
vengono affrontati, risolti e, quindi, inge
gnerizzati con gli strumenti dell’informatica.
Un esempio abbastanza noto è costituito
dai sintetizzatori vocali con cui si interagi
sce telefonicamente quando si chiama un
call center, per esempio, se si deve segnala
re i valori del contatore alla società fornitri
ce di elettricità. Oggi si considerano tali sin
tetizzatori come un utile prodotto dell’infor
matica. In passato, tuttavia, quello dei sin
tetizzatori vocali e, più in generale, della
elaborazione del segnale vocale, era un pro
blema di interazione uomo-macchina a ra
gione collocato nella ricerca in IA.
Il programma di fondo dell’IA, quello di co
struire macchine in grado di comportarsi co
me gli esseri umani, non è mai stato abban
donato e il test di Turing, basato sull’idea
secondo cui se il comportamento di una
macchina è indistinguibile da quello di un
essere umano allora quella macchina può
essere considerata intelligente, viene oggi
quotidianamente superato in molte circo
stanze, almeno in determinati e ben precisi
ambiti cognitivi. A semplificare (o complica
re?) le cose oggi interviene Internet. Le
informazioni, grazie a Internet, si trasferi
scono da un capo all’altro del pianeta in
tempo reale: quando si interagisce con uno
sconosciuto giocando a scacchi in rete, non
si è in grado di stabilire se l’interlocutore sia
un programma softwareo un essere umano.
Così il test di Turing, nel particolare ambito
cognitivo costituito dal gioco degli scacchi,
appare perfettamente superato. In effetti,
rete o no, per quanto riguarda il gioco degli
scacchi ci sono programmi che riescono og
gi a battere i campioni del mondo. Nel 1997,
Deep Blue, un sistema sviluppato dalla
IBM, riuscì a sconfiggere l’allora campione
del mondo di scacchi, G. Kasparov, in un tor
neo regolare di sei incontri. Si trattò di un
successo clamoroso dell’IA. L’osservazione
dello stile di gioco di Deep Blue già aveva
fatto constatare a Kasparov, l’anno prece
dente, quanto segue: “Posso percepire, ne
sento persino l’odore, un nuovo tipo di in
telligenza dall’altra parte del tavolo”. Una
dichiarazione che farebbe credere di essere
andati ben oltre il semplice superamento
del test di Turing.
Nella situazione specifica, la supremazia dei
calcolatori riguarda una data capacità cogniti
va: gli scacchi. Ma è chiaro che un computer
esperto in quel gioco incontrerebbe difficoltà
insormontabili se si pretendesse che si cimen
tasse in un compito per noi assai semplice co
me quello di friggere un uovo. O se si tentasse
di sostenere con lui un’amabile conversazione.
Per limitarsi alle conversazioni con i compu
ter condotte in linguaggio naturale, le diffi
coltà sono effettivamente notevoli. Si può ri
cordare in proposito un famoso programma
degli anni Sessanta, ELIZA (scritto nel 1965
da J. Weizenbaum), che simulava una seduta
dallo psicanalista. Ecco un tipico dialogo tra
il programma e una ragazza:
UTENTE:Gli uomini sono tutti uguali.
ELIZA: In che senso? 
UTENTE:Ci rompono sempre le scatole per
una cosa o per l’altra. 
ELIZA: Ti viene in mente un esempio spe
cifico? 
UTENTE: Il mio ragazzo mi ha fatto venire qui. 
ELIZA: Il tuo ragazzo ti ha fatto venire qui? 
UTENTE:Dice che sono sempre depressa. 
ELIZA: Mi spiace che tu sia depressa. 
E così via, senza fine. La strategia utilizzata
da ELIZA per rispondere all’utente è talmente
ingenua da non richiedere ulteriori commen
ti: anche se, va precisato a onor del vero,
molti di noi sono inclini a sospettare che talo
ra gli psicanalisti veri si comportino allo stes
so modo. A parte gli scherzi, abbiamo certo
sorriso con condiscendenza a fronte di dialo
ghi come questo tra un computer e un utente
umano. Ma dalla metà degli anni Sessanta
ad oggi molto lavoro è stato fatto e si sono
conseguiti risultati assai più interessanti di
questo. ELIZA riveste, ormai, un interesse pu
ramente storico, perché oggi l’elaborazione
del linguaggio naturale scritto e parlato è di
ventata un’area matura e con molteplici ap
plicazioni"""

r = requests.post("http://127.0.0.1:8000/genera", json={"appunto": appunto})
print(r.status_code)
# se torna il PDF, salvalo:
with open("scaricato.pdf", "wb") as f:
    f.write(r.content)