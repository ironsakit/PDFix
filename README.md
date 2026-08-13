# PDFix

Trasforma appunti disordinati e imprecisi in PDF ben organizzati, usando il modello Ollama [qwen3:8b](https://ollama.com/library/qwen3:8b) come "cervello" e il codice Python come le "mani" che eseguono il lavoro: l'LLM decide *cosa* dire, il codice controlla *come* viene impaginato.

![Esempio di PDF](assets/esempio.png)

## Come funziona

1. **Avvio del server** (`server.py`) -- Il server viene avviato con FastAPI e resta in ascolto di richieste HTTP sull'endpoint `/genera`. Per validare il dato in ingresso uso `pydantic`: la classe `Richiesta` (che estende `BaseModel`) ha un unico campo, `appunto`, di tipo `str, così una richiesta malformata viene rifiutata prima ancora di entrare nella pipeline.

2. **Richiesta del client** (`test_client.py`) -- Il client invia una richiesta **POST** con un JSON contenente `appunto` all'endpoint `/genera`, questo attiva la funzione `genera` in `server.py`, che restituisce il PDF impaginato.

3. **La pipeline** (`main.py`) -- Contiene tutte le funzioni: la comunicazione con Qwen, la lettura e lo smistamento del JSON, la trasformazione in blocchi LaTeX e l'assemblaggio finale con il preambolo definito in `template.tex`.


## Decisioni

1. `JSON` -- Ho deciso di trattarlo come una `lista di blocchi` (niente dizionario --> per evitare chiavi duplicate e garantire l'ordine dei blocchi).

2. `IL BLOCCO` -- Ogni blocco possiede un `tipo` che andrà a decidere i campi successivi e quali **template** (funzioni) lo stampa.

| Tipo | Resa nel PDF |
|:------|:--------------|
| `PARAGRAFO` | testo normale che scorre |
| `DEFINIZIONE` | box con titolo |
| `TRAP` | box "errore d'esame" |
| `ESEMPIO` | box esempio |
| `CODICE` | blocco a caratteri fissi |

3. `costruisci_blocco()` -- Scorre la lista di blocchi e ne estrae il tipo e a seconda del tipo verrà usato un **template diverso**, accumulando pezzi che man mano attaccati con `"\n\n".join()`.

4. `TIPO SCONOSCIUTO` -- Visto che nonostante ho strutturato un prompt molto specifico per Qwen, dobbiamo lo stesso valutare il caso in cui potrebbe restituirci dei **tipi senza senso**, per questo motivo ho creato un `template di riserva` il quale stampa i campi di questo tipo sconosciuto senza metterlo nel PDF finale (`debug attivo`)
**Escaping dei caratteri speciali.** -- Prima di finire nel LaTeX, ogni testo passa per una funzione di escaping, serve perché caratteri come `%`, `_`, `&` hanno un significato speciale in LaTeX: un `%` grezzo, ad esempio, commenterebbe il resto della riga facendo sparire del testo senza alcun errore.

5. `IL PREAMBOLO LATEX` -- Risiede in `template.tex`, separato (per renderlo più custom) con un `placeholder` al suo interno `%%contenuto%%`, in modo tale che il codice una volta letto il template lo sostituisca con la serie di pezzi precedentemente creati usando la funzione `.replace()`.

6. `LA COMPILAZIONE` -- La compilazione viene lanciata con `subprocess.run(...)` così l'intera pipeline -- dall'appunto al PDF -- è automatica.

## Requisiti

- **Python 3**
- **[Ollama](https://ollama.com/)** con il modello `qwen3:8b` scaricato (`ollama pull qwen3:8b`)
- Una distribuzione **LaTeX con XeLaTeX** (su Windows: [MiKTeX](https://miktex.org/))
- Dipendenze Python: `fastapi`, `uvicorn`, `pydantic`, `requests`

```bash
pip install "fastapi[standard]" requests
```

## Come si usa

Assicurati che Ollama sia in esecuzione, poi:

**1. Avvia il server** (in un terminale, va lasciato aperto):

```bash
fastapi dev server.py
```

**2. Invia la richiesta** (in un secondo terminale):

```bash
python client.py
```

Il PDF generato viene salvato nella cartella del progetto.

## Limiti noti

- **Formule matematiche non gestite.** Simboli, pedici e apici (es. `T_C`, `ρ`, `∆`) non vengono ancora impaginati in modalità matematica: manca un tipo di blocco dedicato (`FORMULA`) e la relativa gestione `$...$`.
- **Testi molto lunghi.** Una dispensa intera può superare la finestra di contesto del modello o degradarne la qualità. La soluzione (suddivisione del testo) è in programma.

## Possibili sviluppi

- Gestione delle formule matematiche (nuovo tipo `FORMULA`)
- Suddivisione dei testi lunghi e recupero mirato dei contenuti (RAG) da dispense
- Estrazione del testo da foto degli appunti (OCR)
- Retry automatico quando l'LLM restituisce JSON non valido
