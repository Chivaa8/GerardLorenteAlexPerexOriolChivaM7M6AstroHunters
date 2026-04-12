from typing import Union
import strawberry

from app.firebase_conf import db
from app.jugadors.types import Jugador, RegistrarJugadorInput, Item, AtorgarItemInput
from app.errors.types import ErrorNoAutoritzat, ErrorJugadorBanejat


PujarNivellResult = strawberry.union(
    "PujarNivellResult",
    (Jugador, ErrorNoAutoritzat, ErrorJugadorBanejat)
)


@strawberry.type
class JugadorsMutation:
    @strawberry.mutation
    def registrar_jugador(self, info: strawberry.Info, datos: RegistrarJugadorInput) -> Jugador:
        usuario = info.context.usuario
        if not usuario:
            raise Exception("Operació rebutjada: sessió no autenticada.")

        uid = usuario.get("uid")

        datos_dict = strawberry.asdict(datos)

        db.collection("jugadors").document(uid).set({
            "nickname": datos_dict["nickname"],
            "nivell": 1,
            "banejat": False
        })

        return Jugador(
            id=uid,
            nickname=datos_dict["nickname"],
            nivell=1,
            banejat=False
        )

    @strawberry.mutation
    def atorgar_item(self, datos: AtorgarItemInput) -> Item:
        doc_ref = (
            db.collection("jugadors")
            .document(datos.jugador_id)
            .collection("inventari")
            .document()
        )

        doc_ref.set({
            "nom_item": datos.nom_item,
            "raresa": datos.raresa
        })

        return Item(
            id=doc_ref.id,
            nom_item=datos.nom_item,
            raresa=datos.raresa
        )

    @strawberry.mutation
    def pujar_nivell(self, info: strawberry.Info, id_jugador: str) -> PujarNivellResult:
        usuario = info.context.usuario
        if not usuario:
            return ErrorNoAutoritzat(message="Sessió no autenticada")

        email = usuario.get("email", "")
        if not email.endswith("@astrohunters.com"):
            return ErrorNoAutoritzat(message="Només un admin o servidor pot pujar nivell")

        doc_ref = db.collection("jugadors").document(id_jugador)
        doc = doc_ref.get()

        if not doc.exists:
            return ErrorNoAutoritzat(message="Jugador no trobat")

        data = doc.to_dict()

        if data.get("banejat", False):
            return ErrorJugadorBanejat(message="El jugador està banejat")

        nou_nivell = data.get("nivell", 1) + 1
        doc_ref.update({"nivell": nou_nivell})

        return Jugador(
            id=doc.id,
            nickname=data["nickname"],
            nivell=nou_nivell,
            banejat=data["banejat"]
        )