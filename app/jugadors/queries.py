from typing import List, Optional
import strawberry

from app.jugadors.types import Jugador
from app.firebase_conf import db


@strawberry.type
class JugadorsQuery:

    @strawberry.field
    def perfil_jugador(self, id: str) -> Optional[Jugador]:
        doc_ref = db.collection("jugadors").document(id)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        datos = doc.to_dict()
        return Jugador(id=doc.id, **datos)

    @strawberry.field
    def llistar_jugadors(self) -> List[Jugador]:
        docs = db.collection("jugadors").stream()

        resultat = []
        for doc in docs:
            datos = doc.to_dict()
            resultat.append(Jugador(id=doc.id, **datos))

        return resultat
    
    