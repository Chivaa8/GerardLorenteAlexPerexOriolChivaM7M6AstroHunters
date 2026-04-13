import strawberry

from app.errors.types import ErrorPartidaNoTrobada
from app.firebase_conf import db
from app.partides.types import Partida, RegistrarPuntuacioInput


@strawberry.type
class PartidesMutation:
	@strawberry.mutation
	def registrar_puntuacio(self, dades: RegistrarPuntuacioInput) -> Partida:
		partida_ref = db.collection("partides").document(dades.partida_id)
		doc = partida_ref.get()
		if not doc.exists:
			raise Exception("La partida no existeix")

		partida_ref.collection("puntuacions").document(dades.jugador_id).set(
			{
				"jugador_id": dades.jugador_id,
				"punts": dades.punts,
				"baixes": dades.baixes,
			}
		)

		data = doc.to_dict() or {}
		return Partida(id=doc.id, mapa=data.get("mapa", ""), estat=data.get("estat", "En curs"), data_creacio=data.get("data_creacio"))

	@strawberry.mutation
	def finalitzar_partida(self, id_partida: str) -> Partida | ErrorPartidaNoTrobada:
		partida_ref = db.collection("partides").document(id_partida)
		doc = partida_ref.get()

		if not doc.exists:
			return ErrorPartidaNoTrobada(message="La partida no s'ha trobat")

		partida_ref.update({"estat": "Finalitzada"})
		data = doc.to_dict() or {}
		data["estat"] = "Finalitzada"
		return Partida(id=doc.id, mapa=data.get("mapa", ""), estat=data["estat"], data_creacio=data.get("data_creacio"))
