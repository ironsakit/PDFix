import re
import uuid
from pydoc import text

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import FileResponse, StreamingResponse
import asyncio
import os

from main import ask_qwen, parsa_risposta, costruisci_documento, costruisci_blocco, compila_pdf, create_chunks, valida_blocchi
import logging
logging.basicConfig(level=logging.INFO)   # serve per poter accendere anche gli INFO (dato che warning, error, critical sono accesi di default)
logger = logging.getLogger(__name__)

class Richiesta(BaseModel):
    appunto: str
    nome_documento: str

app = FastAPI()  # crea il Server ("python -m uvicorn server:app --reload" per avviarlo)

@app.get("/")
def home():
    return {"messaggio": "Server UP!"}

@app.post("/genera")
async def genera(richesta: Richiesta):

    if len(richesta.appunto) > 50000:
        raise HTTPException(
            status_code=413,  # Error status per aver mandato troppa roba in input
            detail="Too much notes!",
        )
    appunto = richesta.appunto.strip().replace("\r\n", " ").replace("\n", " ")
    chunks = create_chunks(appunto)
    totale = len(chunks)
    risultati = [None] * totale

    async def lavora(i, chunk):
        risultati[i] = await ask_qwen(chunk)

    async def flusso():
        completati = 0
        for finito in asyncio.as_completed([lavora(i, chunk) for i, chunk in enumerate(chunks)]):
            await finito
            completati += 1
            yield f"progress {completati}/{totale}\n"

        tutti_blocchi = []
        for risposta in risultati:
            tutti_blocchi.extend(parsa_risposta(risposta))
        tutti_blocchi = valida_blocchi(tutti_blocchi)
        corpo = costruisci_blocco(tutti_blocchi)
        documento = costruisci_documento(corpo)

        os.makedirs("output", exist_ok=True)  # Crea la cartella 'output' se non esiste
        tex_path = f"output/{richesta.nome_documento.replace(".pdf", "")}.tex"

        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(documento)

        yield "Compilo il PDF...\n"

        await asyncio.to_thread(compila_pdf, tex_path)  # Visto che subprocess dobbiamo per forza aspettarla allora la mandiamo a un Thread almeno il server può rispondere ad altre richieste
        yield f"Done {tex_path}\n"

    return StreamingResponse(flusso(), media_type="text/plain")

@app.get("/scarica/{nome_documento}")
def scarica(nome_documento: str):
    if not re.fullmatch(r"[\w\- ]+", nome_documento):
        raise HTTPException(status_code=400, detail="nome non valido")

    nome_documento = nome_documento.replace(".pdf", "")

    path = f"output/{nome_documento}.pdf"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="PDF non trovato")
    return FileResponse(path, media_type="application/pdf", filename="appunti.pdf")