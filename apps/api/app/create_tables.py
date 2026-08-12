from .database import engine
from .models import Base

# Importa todos os modelos para que eles sejam registrados no metadata.
from . import models  # noqa: F401


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")
