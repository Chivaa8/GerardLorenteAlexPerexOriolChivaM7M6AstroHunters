import strawberry
from typing import List, TYPE_CHECKING
from app.firebase_conf import db

if TYPE_CHECKING:
    from app.partides.types import Partida as PartidaType
else:
    PartidaType = strawberry.LazyType("Partida", "app.partides.types")


@strawberry.type
class Item:
    id: str
    nom_item: str
    raresa: str


@strawberry.type
class Jugador:
    id: str
    nickname: str
    nivell: int
    banejat: bool

    @strawberry.field
    def inventari(self) -> List[Item]:
        docs = db.collection("jugadors").document(self.id).collection("inventari").stream()

        llista_items = []
        for doc in docs:
            datos = doc.to_dict()
            llista_items.append(Item(id=doc.id, **datos))

        return llista_items

    @strawberry.field
    def partides(self) -> List[PartidaType]:
        docs = (
            db.collection("jugadors")
            .document(self.id)
            .collection("partides")
            .stream()
        )

        from app.partides.types import Partida

        partides = []
        for doc in docs:
            partida_id = doc.id
            partida_doc = db.collection("partides").document(partida_id).get()
            if not partida_doc.exists:
                continue

            dades = partida_doc.to_dict() or {}
            partides.append(
                Partida(
                    id=partida_doc.id,
                    mapa=dades.get("mapa", ""),
                    estat=dades.get("estat", "En curs"),
                    data_creacio=str(dades.get("data_creacio", "")),
                )
            )

        return partides


@strawberry.input
class RegistrarJugadorInput:
    nickname: str


@strawberry.input
class AtorgarItemInput:
    jugador_id: str
    nom_item: str
    raresa: str
    

@strawberry.type
class ErrorNoAutoritzat:
    message: str

@strawberry.type
class ErrorJugadorNoTrobat:
    message: str

@strawberry.type
class ErrorJugadorBanejat:
    message: str
