import strawberry
from typing import List, Optional
from app.firebase_conf import db

@strawberry.type
class Item:
    id: str
    nom: str
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

@strawberry.input
class RegistrarJugadorInput:
    nickname: str
   
@strawberry.input
class AtorgarItemInput:
    jugador_id: str
    nom_item: str
    raresa: str