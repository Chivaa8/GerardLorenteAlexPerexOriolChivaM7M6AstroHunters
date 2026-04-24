from typing import List, Optional

from strawberry.dataloader import DataLoader

from app.firebase_conf import db
from app.jugadors.types import Jugador


async def _load_players(player_ids: List[str]) -> List[Optional[Jugador]]:
    referencias = [db.collection("jugadors").document(player_id) for player_id in player_ids]
    docs = db.get_all(referencias)

    players_by_id = {}
    for doc in docs:
        if not doc.exists:
            players_by_id[doc.id] = None
            continue

        data = doc.to_dict() or {}
        players_by_id[doc.id] = Jugador(
            id=doc.id,
            nickname=data.get("nickname", ""),
            nivell=data.get("nivell", 1),
            banejat=data.get("banejat", False),
        )

    return [players_by_id.get(player_id) for player_id in player_ids]


def get_player_loader() -> DataLoader[str, Optional[Jugador]]:
	return DataLoader(load_fn=_load_players)
