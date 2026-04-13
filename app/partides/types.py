from typing import Optional

import strawberry


@strawberry.type
class Partida:
	id: str
	mapa: str
	estat: str
	data_creacio: Optional[str] = None


@strawberry.input
class RegistrarPuntuacioInput:
	partida_id: str
	jugador_id: str
	punts: int
	baixes: int
