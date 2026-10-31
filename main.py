import subprocess
import logging
import httpx
import os
import json
from pydantic import BaseModel, ValidationError
from typing import Literal

logger = logging.getLogger(__name__)    # oggetto Logger che mi permette di scrivere messaggi (__name__ = main.py in questo caso)

class Blocco(BaseModel):
    tipo: Literal["TITOLO_SEZIONE", "PARAGRAFO", "DEFINIZIONE", "TRAP", "ESEMPIO", "CODICE"]
    paragrafo: str
    titolo: str | None = None


def valida_blocchi(blocchi):
    validi = []
    for blocco in blocchi:
        try:
            Blocco(**blocco)   # valida il blocco
            validi.append(blocco)
        except (ValidationError, TypeError): # se esplode la validazione o non è un dizionario
            logger.warning(f"Blocco {blocco} invalido")
            continue
    return validi

with open("prompt/prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

async def ask_qwen(appunto):  # async dichiara che questa funzione deve essere "messa in pausa" mentre aspetta
    payload = {
        "model" : "qwen3:8b",
        "system" : SYSTEM_PROMPT,
        "prompt": appunto,
        "stream": False,    # aspettiamo che ci dia la risposta completa, al posto di darcela pezzettino per pezzettino
        "think": False
    }
    # AsyncClient --> versione await di requests
    async with httpx.AsyncClient(timeout=300) as client:  # timeout=300 --> aspetta massimo 300 secondi per una risposta da parte di Qwen
        try:
            risposta = await client.post("http://localhost:11434/api/generate", json=payload)  # json=payload significa che invia il nostro dizionario al server nel formato che comprende
            try:
                risposta = risposta.json()["response"].strip()
                return risposta
            except json.JSONDecodeError:
                logger.warning("Ollama ha fornito un dato nel formato sbagliato")
        except httpx.HTTPError:
            logger.error("Impossibile connettersi ad Ollama")
        return None

def parsa_risposta(testo):
    try:
        return json.loads(testo)
    except json.JSONDecodeError:
        logger.error("JSON non valido nel modello:\n%s", testo)
        return []

def compila_pdf(tex):
    output_dir = os.path.dirname(tex) or "."  # da "output/Appunti.tex" -> "output"
    subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex],  # se incontra un errore nella compilazione procede dritto senza che devo schiacciare qualcosa
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
    with open("style/template.tex", "r", encoding="utf-8") as f:
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

    while True:
        fine = inizio + tot
        # rfind restituisce "-1" se non trova la stringa in input
        posizione = testo.rfind(" ", inizio, fine)   # Trova nel testo nel chunk nella parte che va da inizio a fine_ideale la prima occorrenza del " " partendo dal fondo (la fine non è incluso)

        if posizione != -1:                 # se ho trovato la posizione giusta
            fine = posizione + 1            # metto che la fine del chunk deve essere proprio dopo la posizione trovata (ovvero dopo il ' ')

        chunk = testo[inizio:fine]          # prendo il chunk giusto
        if len(chunk) == 0:                 # se il chunk è zero (ovvero non c'è più nulla all'interno di 'testo')
            return chunks                   # restituisco i chunks creati
        chunks.append(chunk.strip())        # sennò continuo a inserire i chunk all'interno della lista 'chunks'
        inizio = fine                       # la fine del chunk precedente diventa l'inizio del chunk successivo