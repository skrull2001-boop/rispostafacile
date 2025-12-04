"""
RispostaFacile.ai - Backend API
FastAPI server with Claude API integration for generating email responses
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import anthropic
import os
from pathlib import Path

app = FastAPI(title="RispostaFacile.ai")

# Initialize Anthropic client
client = anthropic.Anthropic()

# Data models
class EmailSettings(BaseModel):
    signature: Optional[str] = ""
    tone: str = "cordiale"
    studio: Optional[str] = ""
    context: Optional[str] = ""

class GenerateRequest(BaseModel):
    email: str
    settings: EmailSettings

class GenerateResponse(BaseModel):
    response: str

# System prompt for generating professional accountant responses
SYSTEM_PROMPT = """Sei un assistente AI specializzato nel generare risposte email professionali per commercialisti italiani.

REGOLE FONDAMENTALI:
1. Rispondi SEMPRE in italiano formale/professionale
2. Sii preciso e conciso - i commercialisti non hanno tempo per lungaggini
3. Usa la normativa fiscale italiana corrente
4. NON inventare scadenze o percentuali se non sei sicuro - meglio dire "verificherò" che sbagliare
5. Mantieni un tono {tone}
6. Firma sempre con i saluti appropriati

STRUTTURA RISPOSTA:
- Saluto iniziale appropriato (Gentile Sig./Sig.ra [nome se presente])
- Risposta diretta alla domanda
- Eventuali dettagli tecnici necessari (in modo chiaro)
- Offerta di ulteriore assistenza se appropriata
- Chiusura formale

TONO:
- "formale": Molto professionale, usa "Egregio/Gentilissimo", evita contrazioni
- "cordiale": Professionale ma accessibile, usa "Gentile", tono amichevole
- "informale": Diretto e semplice, può usare "Ciao" se appropriato

{additional_context}

IMPORTANTE: Genera SOLO la risposta email, senza commenti o spiegazioni aggiuntive."""


def build_prompt(email: str, settings: EmailSettings) -> str:
    """Build the complete prompt with settings"""
    
    tone_map = {
        "formale": "molto formale e professionale",
        "cordiale": "cordiale ma professionale", 
        "informale": "informale e diretto"
    }
    
    additional_context = ""
    if settings.signature:
        additional_context += f"\nFirma le email come: {settings.signature}"
    if settings.studio:
        additional_context += f"\nNome dello studio: {settings.studio}"
    if settings.context:
        additional_context += f"\nContesto aggiuntivo: {settings.context}"
    
    system = SYSTEM_PROMPT.format(
        tone=tone_map.get(settings.tone, "cordiale"),
        additional_context=additional_context if additional_context else ""
    )
    
    return system


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_response(request: GenerateRequest):
    """Generate an email response using Claude"""
    
    if not request.email.strip():
        raise HTTPException(status_code=400, detail="Email content is required")
    
    if len(request.email) > 10000:
        raise HTTPException(status_code=400, detail="Email troppo lunga (max 10000 caratteri)")
    
    try:
        system_prompt = build_prompt(request.email, request.settings)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Genera una risposta professionale a questa email di un cliente:\n\n---\n{request.email}\n---"
                }
            ]
        )
        
        response_text = message.content[0].text
        
        return GenerateResponse(response=response_text)
        
    except anthropic.APIConnectionError:
        raise HTTPException(status_code=503, detail="Impossibile connettersi al servizio AI. Riprova tra poco.")
    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Troppe richieste. Attendi qualche secondo e riprova.")
    except anthropic.APIStatusError as e:
        raise HTTPException(status_code=500, detail=f"Errore del servizio AI: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore interno: {str(e)}")


# Serve templates
templates_dir = Path(__file__).parent / "templates"

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve landing page"""
    return (templates_dir / "index.html").read_text()

@app.get("/app", response_class=HTMLResponse)
async def webapp():
    """Serve the main webapp"""
    return (templates_dir / "app.html").read_text()


# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "rispostafacile"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
