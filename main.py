import subprocess
import requests
import json
from pydantic import BaseModel, ValidationError


class Blocco(BaseModel):
    tipo: str
    paragrafo: str
    titolo: str | None = None


def valida_blocchi(blocchi):
    validi = []
    for blocco in blocchi:
        try:
            Blocco(**blocco)   # valida il blocco
            validi.append(blocco)
        except (ValidationError, TypeError): # se esplode la validazione o non è un dizionario
            print("blocco scartato: ", blocco)
            continue
    return validi

# r --> (raw string) dice che in questa stringa le lettere come backslash sono lettere normali senza doverle raddoppiare
# \usepackage[tcolorbox] --> libreria scatole colorate
# \tcbuselibrary{skins, breakable} --> bei bordi e box che vanno a capo a fine pagina
# \newtcolor{defn}[1] --> nuovo tipo di box latex --> colblack=green!5 (colore sfondo verde chiaro a 5%), colframe=green!50!black (colore bordo verde scuro), fonttile=\bfseries (titolo in grassetto)
# \newtcolor{trap}[1] --> nuovo tipo di box latex --> colblack=orange!5 (colore sfondo arancione chiaro a 5%), colframe=orange!80!black (colore bordo arancione scuro), fonttile=\bfseries (titolo in grassetto)

SYSTEM_PROMPT = """"Rispondi con il JSON e basta. Nessun testo prima, nessun testo dopo, niente ```json, nessuna spiegazione. Il primo carattere della tua risposta deve essere [ e l'ultimo ].

Il tuo unico compito è ordinare e migliorare gli appunti che vengono inseriti come input, seguendo un formato preciso.

- Devi creare un JSON contenente una lista di blocchi (dizionari), dove inserisci gli appunti migliorati e ordinati.
- Il formato di ciascun dizionario è: {tipo, [titolo], paragrafo}.
- I tipi concessi sono: "TITOLO_SEZIONE", "PARAGRAFO", "DEFINIZIONE", "TRAP", "ESEMPIO", "CODICE".
- Ogni tipo ha una chiave "paragrafo" con il testo di quel tipo.
- Solo il tipo "DEFINIZIONE" ha anche la chiave "titolo".

Funzione di ogni tipo:
- "TITOLO_SEZIONE" --> introduce un nuovo argomento principale; nel paragrafo va SOLO il nome della sezione, senza contenuto.
- "PARAGRAFO" --> un paragrafo di testo e il suo contenuto.
- "DEFINIZIONE" --> una definizione, con titolo e contenuto.
- "TRAP" --> una trappola d'esame in cui è facile cadere.
- "ESEMPIO" --> un esempio dell'argomento appena trattato.
- "CODICE" --> una porzione di codice (per le materie che lo richiedono).

COSE IMPORTANTI DA RICORDARE:
- I blocchi vanno inseriti nella lista in ordine logico, seguendo il filo degli argomenti.
- IMPORTANTE: ogni volta che il testo introduce un nuovo argomento principale, DEVI inserire PRIMA un blocco "TITOLO_SEZIONE" con il nome dell'argomento, e SOLO DOPO i paragrafi e gli altri blocchi che lo riguardano. Un documento ben strutturato inizia sempre con un TITOLO_SEZIONE.
- TRAP, ESEMPIO e CODICE sono OPZIONALI: se non hai dati sufficienti per generarli in modo pertinente, ometterli.

Esempio del formato atteso:
[
  {"tipo": "TITOLO_SEZIONE", "paragrafo": "Le grandezze fisiche"},
  {"tipo": "PARAGRAFO", "paragrafo": "Una grandezza fisica è una proprietà misurabile di un corpo o fenomeno."},
  {"tipo": "DEFINIZIONE", "titolo": "Massa", "paragrafo": "La massa è la quantità di materia di un corpo, misurata in kg."},
  {"tipo": "ESEMPIO", "paragrafo": "Un litro d'acqua ha una massa di circa 1 kg."}
]"""

def ask_qwen(appunto):
    payload = {
        "model" : "qwen3:8b",
        "system" : SYSTEM_PROMPT,
        "prompt": appunto,
        "stream": False,    # aspettiamo che ci dia la risposta completa, al posto di darcela pezzettino per pezzettino
        "think": False
    }
    risposta = requests.post("http://localhost:11434/api/generate", json=payload)  # json=payload significa che invia il nostro dizionario al server nel formato che comprende
    dati = risposta.json()
    return dati["response"]

def parsa_risposta(testo):
    try:
        return json.loads(testo)
    except json.JSONDecodeError:
        print("JSON invalido")
        print(testo)
        return []

def compila_pdf(tex):
    subprocess.run(
        ["xelatex", "-interaction=nonstopmode", tex],  # se incontra un errore nella compilazione procede dritto senza che devo schiacciare qualcosa
        check=True  # fa sollevare un errore Python se la compilazione fallisce così ce ne accorgiamo
    )

def escape(text):
    text = text.replace("\\", "\\textbackslash{}")
    text = text.replace("%", "\\%")
    text = text.replace("&", "\\&")
    text = text.replace("$", "\\$")
    text = text.replace("#", "\\#")
    text = text.replace("_", "\\_")
    return text

def costruisci_documento(corpo):
    with open("template.tex", "r", encoding="utf-8") as f:
        template = f.read()

    documento = template.replace("%%CONTENUTO%%", corpo)
    return documento

def template_paragrafo(blocco):
    return f"{escape(blocco['paragrafo'].strip())}\n"

def template_definizione(blocco):
    titolo = blocco.get("titolo", "Definizione")   # se manca, usa "Definizione"
    return (f"\\begin{{defn}}{{{escape(titolo)}}}\n"
            f"{escape(blocco['paragrafo'])}\n"
            f"\\end{{defn}}\n")

def template_codice(blocco):
    return (f"\\begin{{verbatim}}\n"
            f"{blocco['paragrafo']}\n"
            f"\\end{{verbatim}}\n")

def template_trap(blocco):
    return (f"\\begin{{trap}}{{Errori da evitare}}\n"
            f"{escape(blocco['paragrafo'])}\n"
            f"\\end{{trap}}\n")

def template_esempio(blocco):
    return (f"\\begin{{ex}}{{Esempio}}\n"
            f"{escape(blocco['paragrafo'])}\n"
            f"\\end{{ex}}\n")

def template_riserva(blocco):
    righe = []
    for chiave, valore in blocco.items():
        riga = f"{chiave}: {escape(valore)}"
        righe.append(riga)
    return "\\\\".join(righe)


def template_titolo_sezione(blocco):
    return f"\\section{{{escape(blocco['paragrafo'])}}}\n"


def costruisci_blocco(blocchi):
    pezzi = []
    for blocco in blocchi:
        if not isinstance(blocco, dict):
            continue
        tipo = blocco.get("tipo")
        if tipo is None:
            continue
        tipo = tipo.upper()
        if tipo == 'TITOLO_SEZIONE':
            pezzi.append(template_titolo_sezione(blocco))
        elif tipo == "DEFINIZIONE":
            pezzi.append(template_definizione(blocco))
        elif tipo == "PARAGRAFO":
            pezzi.append(template_paragrafo(blocco))
        elif tipo == "TRAP":
            pezzi.append(template_trap(blocco))
        elif tipo == "CODICE":
            pezzi.append(template_codice(blocco))
        elif tipo == "ESEMPIO":
            pezzi.append(template_esempio(blocco))
        else:
            continue
    return "\n\n".join(pezzi)

def create_chunks(testo, tot = 4000):
    chunks = []
    inizio = 0
    while inizio < len(testo):
        fine_ideale = inizio + tot
        posizione = testo.rfind(".", inizio, fine_ideale)
        fine = fine_ideale if posizione == -1 else posizione + 1
        chunk = testo[inizio:fine]
        if len(chunk) == 0:
            return chunks
        chunks.append(chunk)
        inizio = fine
    return chunks