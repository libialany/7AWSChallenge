from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import os
import telebot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(BOT_TOKEN)
Base = declarative_base()


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

def check_content(item: ItemSchema):
    text= f"Repo name: {item.repo_name}\nGH username: {item.gh_username}\nContent repo: {item.content_repo}"
    bot.send_message(CHAT_ID, text)


def areSafeText(item: ItemSchema):
    return True

@app.post("/api/todo")
def addItem(item: ItemSchema):
    todoitem = Item(repo_name=item.repo_name,gh_username=item.gh_username, content_repo=item.content_repo)
    if areSafeText(item):
        check_content(item)
        return todoitem
    return {"error": "Invalid input"}