from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_ppt import router as ppt_router
from spellchecker import SpellChecker

app = FastAPI()
spell = SpellChecker()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def autocorrect_text(text: str) -> str:
    return " ".join([spell.correction(word) for word in text.split()])

@app.get("/")
def home():
    return {"message": "API is running!"}

@app.post("/autocorrect")
def autocorrect_api(text: str = Body(..., embed=True)):
    fixed_text = autocorrect_text(text)
    return {"fixed": fixed_text}

app.include_router(ppt_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
