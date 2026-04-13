import strawberry


@strawberry.type
class ErrorNoAutoritzat:
	message: str


@strawberry.type
class ErrorJugadorBanejat:
	message: str


@strawberry.type
class ErrorPartidaNoTrobada:
	message: str
