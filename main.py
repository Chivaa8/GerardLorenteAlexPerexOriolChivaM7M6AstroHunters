import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.firebase_conf import db
from app.schema import schema

# Crear aplicación FastAPI
app = FastAPI(
    title="AstroHunters Backend API",
    description="GraphQL API for AstroHunters multiplayer game",
    version="1.0.0",
)

# Añadir middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear router GraphQL
graphql_router = GraphQLRouter(
    schema,
    path="/graphql",
)

# Incluir router GraphQL
app.include_router(graphql_router)

# Endpoint de verificación de estado (health check)
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "AstroHunters Backend is running",
        "firebase": "connected" if db else "disconnected"
    }

@app.get("/")
async def root():
    return {
        "name": "AstroHunters GOA",
        "version": "1.0.0",
        "graphql_url": "http://localhost:8000/graphql",
        "health_url": "http://localhost:8000/health",
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8000"))
    
    print(f"Iniciando AstroHunters Backend en http://{host}:{port}")
    print(f"Endpoint GraphQL: http://{host}:{port}/graphql")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )