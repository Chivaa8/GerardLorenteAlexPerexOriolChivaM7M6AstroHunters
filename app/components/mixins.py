from app.jugadors.mutations import JugadorsMutation
from app.jugadors.queries import JugadorsQuery
from app.partides.mutations import PartidesMutation
from app.partides.queries import PartidesQuery


class QueriesMixin(JugadorsQuery, PartidesQuery):
	pass


class MutationsMixin(JugadorsMutation, PartidesMutation):
	pass
