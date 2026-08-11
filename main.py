import subprocess
import requests
import json

# r --> (raw string) dice che in questa stringa le lettere come backslash sono lettere normali senza doverle raddoppiare
# \usepackage[tcolorbox] --> libreria scatole colorate
# \tcbuselibrary{skins, breakable} --> bei bordi e box che vanno a capo a fine pagina
# \newtcolor{defn}[1] --> nuovo tipo di box latex --> colblack=green!5 (colore sfondo verde chiaro a 5%), colframe=green!50!black (colore bordo verde scuro), fonttile=\bfseries (titolo in grassetto)
# \newtcolor{trap}[1] --> nuovo tipo di box latex --> colblack=orange!5 (colore sfondo arancione chiaro a 5%), colframe=orange!80!black (colore bordo arancione scuro), fonttile=\bfseries (titolo in grassetto)

SYSTEM_PROMPT = """"Rispondi con il JSON e basta. Nessun testo prima, nessun testo dopo, niente ``json, nessuna spiegazione. Il primo carattere della tua risposta deve essere [ e l'ultimo ]`.
Il tuo unico compito è quello di ordinare e migliorare gli appunti che vengono inseriti come input, seguendo un certo criterio:

Devi creare un JSON con al suo interno una lista di blocchi (a loro volta dei dizionari) come risposta, dove inserirai gli appunti migliorati e ordinati seguendo un formato ben preciso.
Il formato di ciascun dizionario è il seguente: {tipo, [titolo], paragrafo}.
I tipi concessi sono: "PARAGRAFO", "DEFINIZIONE", "TRAP", "ESEMPIO" e "CODICE".
Ogni tipo ha una chiave "paragrafo" che contiene il testo di quel tipo.
Solo il tipo "DEFINIZIONE" contiene la chiave titolo.
Ogni tipo ha una sua funzionalità che dovrai rispettare:

"PARAGRAFO" --> indica un paragrafo e il suo contenuto.
"DEFINIZIONE" --> indica una definizione da fornire con titolo.
"TRAP" --> indica una trappola d'esame che molto spesso ci si può imbattere.
"CODICE" --> indica una possibile porzione di codice (se si parla di materie che ne richiedono)
"ESEMPIO" --> indica un esempio dell'argomento appena trattato.
COSE IMPORTANTI DA RICORDARE:
I blocchi di dizionari devono essere inseriti nella lista con ordine logico in base agli argomenti da trattare.
Inoltre se non riesci a generare TRAP, CODICE o ESEMPIO pertinenti perché non hai dati sufficienti puoi anche evitarli di scriverli, sono considerati OPZIONALI."""

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
    return (f"\\begin{{defn}}{{{blocco['titolo']}}}\n"
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

def costruisci_blocco(blocchi):
    pezzi = []
    for blocco in blocchi:
        tipo = blocco["tipo"].upper()
        if tipo == "DEFINIZIONE":
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
            pezzi.append(template_riserva(blocco))
    return "\n\n".join(pezzi)