from fastapi import Header
from firebase_admin import auth 
from typing import Optional, Dict, Any

def obtener_usuario_actual(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    if not authorization or not authorization.startswith("Bearer "):
        return None # verificamos que no haya ausencia de credenciales o un mal formato
    
    token = authorization.removeprefix("Bearer ") # quitamos  Bearer si sale

    try:
        usuario_decodificado = auth.verify_id_token(token)

        email = usuario_decodificado.get("email", "")
        uid = usuario_decodificado.get("uid")

        return {
            "uid": uid,
            "email": email,
            "is_admin": email.endswith("@astrohunters.com"), # para poder verificar si es admin
            "token_data": usuario_decodificado
        }
    
    except Exception as e:
        print(f"Intento de acceso no autorizado o token experiado: {e}")
        return None 