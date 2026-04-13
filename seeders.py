from app.firebase_conf import db
from datetime import datetime

jugadors_demo = [
    {
        "id": "jugador_1",
        "nickname": "Hunter1",
        "nivell": 5,
        "banejat": False,
        "inventari": [
            {"nom_item": "Pistola Làser", "raresa": "Èpic"},
            {"nom_item": "Escut d'Energia", "raresa": "Comú"}
        ]
    },
    {
        "id": "jugador_2",
        "nickname":"Shadow Hunter",
        "nivell": 3,
        "banejat": False,
        "inventari": [
            {"nom_item": "Rifle Plasma", "raresa": "Llegendari"}
        ]
    }
]

partides_demo = [
    {
        "mapa": "Base Lunar",
        "estat": "Finalitzada",
        "puntuacions": [
            {"jugador_id": "jugador_1", "punts": 2500, "baixes": 10},
            {"jugador_id": "jugador_2", "punts": 1800, "baixes": 7}
        ]
    },
    {
        "mapa": "Estació Orbital",
        "estat": "En curs",
        "puntuacions": []
    }
]

def inicialitzar_db():
    print("Inicialitzant base de dades AStroHunters...")

    #creamos jugadores
    for jugador in jugadors_demo:
        inventari = jugador.pop("inventari")
        jugador_id = jugador["id"]

        doc_ref = db.collection("jugadors").document(jugador_id)
        doc_ref.set(jugador)

        print(f"👤 Jugador creat: {jugador['nickname']}")

        #inventario
        for item in inventari:
            doc_ref.collection("inventari").document().set(item)
    
    # crear partides
    for partida in partides_demo:
        puntuacions = partida.pop("puntuacions")

        doc_ref = db.collection("partides").document()
        partida["data_cració"] = datetime.utcnow().isoformat()
        doc_ref.set(partida)

        print(f"🎮 Partida creada: {partida['mapa']}")

        #punts
        for puntuacio in puntuacions:
            doc_ref.collection("puntacions").document().set(puntuacio)

    print("🎉 Base de dades inicialitzada correctamente!")

if __name__ == "__main__":
    inicialitzar_db()