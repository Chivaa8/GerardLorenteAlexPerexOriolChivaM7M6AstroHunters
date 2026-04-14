from typing import List, Optional

from strawberry.dataloader import DataLoader

from app.firebase_conf import db
from app.partides.types import Partida


async def _load_matches(match_ids: List[str]) -> List[Optional[Partida]]:
	matches_by_id = {}

	for match_id in match_ids:
		doc = db.collection("partides").document(match_id).get()
		if not doc.exists:
			matches_by_id[match_id] = None
			continue

		data = doc.to_dict() or {}
		matches_by_id[match_id] = Partida(
			id=doc.id,
			mapa=data.get("mapa", ""),
			estat=data.get("estat", "En curs"),
			data_creacio=str(data.get("data_creacio", "")),
		)

	return [matches_by_id.get(match_id) for match_id in match_ids]


def get_partida_loader() -> DataLoader[str, Optional[Partida]]:
	return DataLoader(load_fn=_load_matches)
