import strawberry
from app.components.mixins import QueriesMixin, MutationsMixin
from strawberry.dataloader import DataLoader
from .firebase_conf import db
import asyncio
from typing import List, Optional

from strawberry.dataloader import DataLoader

from app.firebase_conf import db
from app.jugadors.types import Jugador


@strawberry.type
class Query(QueriesMixin):
    pass

@strawberry.type
class Mutation(MutationsMixin):
    pass

# Para crear el esquema GraphQL, combinamos las consultas y las mutaciones
schema = strawberry.Schema(query=Query, mutation=Mutation)

async def _load_players(player_ids: List[str]) -> List[Optional[Jugador]]:
    """
    Recibe una lista de IDs de jugador, por ejemplo: ['jugador_1', 'jugador_2', 'jugador_1']
    y devuelve los Jugador en ese mismo orden exacto (sin duplicados innecesarios en Firestore).
    """
    # 1. Convertimos los IDs en referencias de documento de Firestore
    referencias = [db.collection("jugadors").document(player_id) for player_id in player_ids]

    # 2. Usamos db.get_all() para recuperar múltiples documentos en una sola transacción de red
    docs = db.get_all(referencias)

    # 3. Mapeamos la respuesta asegurando que devolvemos un None si el jugador fue eliminado
    jugadors_by_id = {}
    for doc in docs:
        if doc.exists:
            data = doc.to_dict() or {}
            jugadors_by_id[doc.id] = Jugador(
                id=doc.id,
                nickname=data.get("nickname", ""),
                nivell=data.get("nivell", 1),
                banejat=data.get("banejat", False),
            )
        else:
            jugadors_by_id[doc.id] = None

    # 4. Retornamos en el mismo orden exacto que llegaron los IDs
    return [jugadors_by_id.get(player_id) for player_id in player_ids]


def get_player_loader() -> DataLoader[str, Optional[Jugador]]:
    return DataLoader(load_fn=_load_players)