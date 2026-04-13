import strawberry
from typing import List, Optional
from app.firebase_conf import db

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
    def partides(self) -> List[strawberry.LazyType["Partida", "app.partides.types"]]:
        from app.partides.types import Partida

        resultat = []
        for doc in db.collection("partides").stream():
            partida_data = doc.to_dict() or {}
            puntuacions = doc.reference.collection("puntuacions").where("jugador_id", "==", self.id).limit(1).stream()
            if next(puntuacions, None) is not None:
                resultat.append(Partida.from_firestore(doc.id, partida_data))

        return resultat

@strawberry.input
class RegistrarJugadorInput:
    nickname: str
   
@strawberry.input
class AtorgarItemInput:
    jugador_id: str
    nom_item: str
    raresa: str