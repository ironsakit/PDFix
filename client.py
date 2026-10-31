import httpx
import logging
logger = logging.getLogger(__name__)

with open("input/notes.txt", "r", encoding="utf-8") as f:
    appunto = f.read()

nome_documento = input("Che nome vuoi nominare i tuoi appunti?\n")

try:
    with httpx.stream("POST", "http://127.0.0.1:8000/genera", json={"appunto":appunto, "nome_documento":nome_documento}, timeout=None) as r:
        for l in r.iter_lines():
            if not l: continue
            print(l)
            if l.startswith("Done"):
                pdf = httpx.get(f"http://127.0.0.1:8000/scarica/{nome_documento}")
                with open("scaricato.pdf", "wb") as f:
                    f.write(pdf.content)
                print("PDF salvato.")
except Exception as e:
    logger.error("Errore interno al server.")