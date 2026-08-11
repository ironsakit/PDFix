from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import FileResponse

from main import ask_qwen, parsa_risposta, costruisci_documento, costruisci_blocco, compila_pdf

app = FastAPI()  # crea il Server

class Richiesta(BaseModel):
    appunto: str

@app.post("/genera")
def genera(richesta: Richiesta):
    if len(richesta.appunto) > 10000:
        raise HTTPException(
            status_code=413,  # Error status per aver mandato troppa roba in input
            detail="Too much notes!",
        )
    appunto = richesta.appunto
    risposta = ask_qwen(appunto)
    blocchi = parsa_risposta(risposta)
    documento = costruisci_documento(costruisci_blocco(blocchi))
    with open("mattia.tex", "w", encoding="utf-8") as f:
        f.write(documento)
    compila_pdf("mattia.tex")
    return FileResponse("mattia.pdf", media_type="application/pdf", filename="appunti.pdf")

@app.get("/")  # decoratore per attivare la funzione sotto a quell'indirizzo
def home():
    return {"messaggio": "Server UP!"}

