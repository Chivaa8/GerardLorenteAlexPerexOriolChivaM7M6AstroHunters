import strawberry
from typing import List, Optional, TYPE_CHECKING

from app.firebase_conf import db

if TYPE_CHECKING:
    from app.jugadors.types import Jugador as JugadorType
else:
    JugadorType = strawberry.LazyType("Jugador", "app.jugadors.types")


@strawberry.type
class Puntuacio:
    id: str
    jugador_id: str
    punts: int
    baixes: int

    @strawberry.field
    async def jugador(self, info: strawberry.Info) -> Optional[JugadorType]:
        return await info.context.player_loader.load(self.jugador_id)


@strawberry.type
class Partida:
    id: str
    mapa: str
    estat: str
    data_creacio: str

    @strawberry.field
    def puntuacions(self) -> List[Puntuacio]:
        docs = (
            db.collection("partides")
            .document(self.id)
            .collection("puntuacions")
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


@strawberry.input
class CrearPartidaInput:
    mapa: str


@strawberry.input
class RegistrarPuntuacioInput:
    id_partida: str
    jugador_id: str
    punts: int
    baixes: int