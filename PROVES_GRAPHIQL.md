# Proves GraphiQL (4 operacions)

Nota important:
- Els noms van en `camelCase` (com Strawberry els exposa per defecte).
- Abans de provar `registrarPuntuacio` i `finalitzarPartida`, crea una partida a Firestore (`partides/{id}`).
- L'objectiu d'aquestes proves es validar: query basica, mutacions, relacio LazyType i error tipat.



## 1) Query: perfil de jugador + inventari + partides (LazyType)

```graphql
query PerfilJugador {
  perfilJugador(id: "jugador_1") {
    id
    nickname
    nivell
    banejat
    inventari {
      id
      nomItem
      raresa
    }
    partides {
      id
      mapa
      estat
      dataCreacio
    }
  }
}
```

## 2) Mutation: atorgar item a inventari

```graphql
mutation AtorgarItem {
  atorgarItem(
    datos: {
      jugadorId: "jugador_1"
      nomItem: "Escut d'Energia"
      raresa: "Epic"
    }
  ) {
    id
    nomItem
    raresa
  }
}
```

## 3) Mutation: registrar puntuacio en una partida

```graphql
mutation RegistrarPuntuacio {
  registrarPuntuacio(
    dades: {
      idPartida: "PARTIDA_ID_AQUI"
      jugadorId: "jugador_1"
      punts: 2500
      baixes: 10
    }
  ) {
    id
    mapa
    estat
    dataCreacio
  }
}
```

## 4) Mutation: finalitzar partida (Partida o ErrorPartidaNoTrobada)

```graphql
mutation FinalitzarPartida {
  finalitzarPartida(idPartida: "PARTIDA_ID_AQUI") {
    __typename
    ... on Partida {
      id
      mapa
      estat
      dataCreacio
    }
    ... on ErrorPartidaNoTrobada {
      message
    }
  }
}
```


