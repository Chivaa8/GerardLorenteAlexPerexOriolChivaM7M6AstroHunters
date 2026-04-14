from typing import List, Optional
import strawberry

from app.firebase_conf import db
from app.partides.types import Partida, Puntuacio


@strawberry.type
class PartidesQuery:

    @strawberry.field
    def llistar_partides(
        self,
        estat: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Partida]:
        docs = db.collection("partides").stream()

        llista_partides = []
        for doc in docs:
            dades = doc.to_dict()

            if estat is not None and dades.get("estat") != estat:
                continue

            llista_partides.append(
                Partida(
                    id=doc.id,
                    mapa=dades["mapa"],
                    estat=dades["estat"],
                    data_creacio=str(dades["data_creacio"])
                )
            )

        return llista_partides[offset: offset + limit]

    @strawberry.field
    def taula_classificacio(self, id_partida: str) -> List[Puntuacio]:
        partida_ref = db.collection("partides").document(id_partida)
        partida_doc = partida_ref.get()

        if not partida_doc.exists:
            return []

        dades_partida = partida_doc.to_dict()

        if dades_partida.get("estat") != "Finalitzada":
            return []

        docs = (
            partida_ref
            .collection("puntuacions")
            .order_by("punts", direction="DESCENDING")
            .stream()
        )

        resultat = []
        for doc in docs:
            dades = doc.to_dict()
            resultat.append(
                Puntuacio(
                    id=doc.id,
                    jugador_id=dades["jugador_id"],
                    punts=dades["punts"],
                    baixes=dades["baixes"]
                )
            )

        return resultat