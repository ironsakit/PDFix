from main import create_chunks

def test_create_chunks():  # python -m pytest
    testo = "parola " * 1000  # testo lungo con 1000 'parola' separate da spazi
    chunks = create_chunks(testo, tot=50)  # testiamo creando dei chunk lunghi al massimo 50 caratteri

    # Nessuna parola persa
    assert ' '.join(chunks).split() == testo.split()

    # Ogni pezzo rispetta il limite dei 50 caratteri
    assert all(len(a) <= 50 for a in chunks)