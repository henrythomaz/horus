from database import engine

from models.base import Base

# importa os modelos
import models

Base.metadata.create_all(engine)

print("Tabelas criadas com sucesso!")
