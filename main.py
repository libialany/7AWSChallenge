from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from fastapi.responses import JSONResponse
import re    
import os
import requests
import telebot
text = ""
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL_GITHUB="https://raw.githubusercontent.com"
bot = telebot.TeleBot(BOT_TOKEN)
Base = declarative_base()
challenges = [
    "Day1.md",
    "Day2.md",      
    "Day3.md",
    "Day4.md",      
    "Day5.md"
]

class ItemSchema(BaseModel):
    repo_name: str
    gh_username: str
    content_repo: str
class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    repo_name = Column(String(256))
    gh_username = Column(String(256))
    content_repo = Column(String(256))

    def __init__(self, repo_name: str, gh_username: str, content_repo: str):
        self.repo_name = repo_name
        self.gh_username = gh_username
        self.content_repo = content_repo

app = FastAPI()

def is_content_completed(text: str):
    pattern = r'result:\s*(https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))'
    match = re.search(pattern, text)
    status = match is not None
    if status:
        return True
    else:
        return False

def is_challenge_completed(item: ItemSchema, challenge: str):
    url = f"{URL_GITHUB}/{item.repo_name}/main/{challenge}"
    response = requests.get(url)
    if response.status_code == 404:
        return False
    text = response.content.decode('utf-8')
    if not text:
        return False
    if not is_content_completed(text):
        return False
    return True
def check_content(item: ItemSchema):
    global challenges
    global text
    challenge_count = 0 
    for challenge in challenges:
        if is_challenge_completed(item, challenge):
            text = "Felicidades! Has completado el desafío " + challenge
            challenge_count += 1
        else:
            text = "No has completado el desafío " + challenge
    if challenge_count == 5:
        text = "Felicidades! Has completado todos los desafíos"
    bot.send_message(CHAT_ID, text)


def areSafeText(item: ItemSchema):
    return True

@app.get("/api/status")
def status():
    return JSONResponse(
            status_code=200,
            content={
                "content": "El servicio está activo"
            }
        )

@app.post("/api/challenge")
def addItem(item: ItemSchema):
    global text
    if areSafeText(item):
        check_content(item)
        return JSONResponse(
            status_code=200,
            content={
                "content": text
            }
        )
    return JSONResponse(
            status_code=200,
            content={
                "content": "Error en la petición"
            }
        )