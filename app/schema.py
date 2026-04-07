import strawberry
from app.components.mixins import QueriesMixin, MutationsMixin

@strawberry.type
class Query(QueriesMixin):
    pass

@strawberry.type
class Mutation(MutationsMixin):
    pass

# Para crear el esquema GraphQL, combinamos las consultas y las mutaciones
schema = strawberry.Schema(query=Query, mutation=Mutation)
