# app/db/base.py

from sqlalchemy.orm import declarative_base

# Base é a classe base para os modelos do SQLAlchemy. Todos os modelos devem herdar desta classe.
Base = declarative_base()
