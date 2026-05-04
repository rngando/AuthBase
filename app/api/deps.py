
from app.db.session import SessionLocal

def get_db():
    # Cria uma sessão do banco de dados para cada requisição e garante que ela seja fechada após o uso.
    db = SessionLocal()
    try:
        # O `yield` permite que a função seja usada como um gerador.
        yield db
    finally:
        db.close()

