from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx

router = APIRouter()

@router.get(
    "/pokemon/{nome}",
    response_class=RedirectResponse,
    responses={
        200: {
            "description": "Redireciona para imagem SVG do Pokémon",
            "content": {
                "image/svg+xml": {
                    "example": "<svg>...</svg>"
                }
            }
        },
        404: {"description": "Pokémon ou imagem não encontrado"},
    },
)
async def get_pokemon_image(nome: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Pokémon não encontrado")

        data = response.json()
        try:
            image_url = data["sprites"]["other"]["dream_world"]["front_default"]
            if not image_url:
                raise ValueError("Imagem não encontrada")
        except (KeyError, ValueError):
            raise HTTPException(status_code=404, detail="Imagem Dream World não disponível")

        return RedirectResponse(url=image_url)
