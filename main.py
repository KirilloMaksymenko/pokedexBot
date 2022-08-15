#project - pokedexBot , Author - Maksymenko Kyrylo

#https://www.pokemon.com/ru/pokedex/

import requests
from bs4 import BeautifulSoup
import telebot

bot = telebot.TeleBot("5694918426:AAF9pjZxTaNsuMFUwqwCX96RqD8NIWQVBsc")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Enter /find (id_name)")

@bot.message_handler(commands=['find'])
def send_welcome(message):
    id_name = message.text.replace("/find ","")
    text,img_url = make_text(get_data(id_name))

    bot.send_photo(message.chat.id, img_url)
    bot.send_message(message.chat.id, text)

def get_data(name_id):
    url = f"https://www.pokemon.com/ru/pokedex/{name_id}"
    context = BeautifulSoup(requests.get(url).text,"lxml")
    name = context.find("div",class_="pokedex-pokemon-pagination-title").get_text().replace(" ","").replace("\n"," ")
    print(name)
    
    type = context.find("div",class_="dtm-type").get_text().replace("\n"," ").replace("Type","")
    print(type)

    about = context.find("p",class_="version-x").get_text().replace("\n"," ").replace("  ","")
    print(about)

    params = []
    for i in context.find_all("span",class_="attribute-value",limit=2):
        params.append(i.get_text())
    print(params)

    evolutions = []
    for i in context.find("ul",class_="evolution-profile").find_all("h3",class_="match"):
        evolutions.append(i.get_text().replace("\n"," ").replace(" ","").replace("#"," #"))
    print(evolutions)
    
    img = context.find("div",class_="profile-images").find("img").get("src")
    print(img)

    output = {
        "name":name,
        "type":type,
        "about":about,
        "params":params,
        "evolutions":evolutions,
        "img":img,
    }
    return output


def make_text(data):
    
    text = f"Name id - {data['name']}\n"
    text = f"{text} Type - {data['type']}\n"
    text = f"{text} About - {data['about']}\n"
    text = f"{text} Height - {data['params'][0]}  Weight - {data['params'][1]}\n\n"
    text = f"{text} Evolution -\n"
    for i in data["evolutions"]:
        text = f"{text} {i}\n"
    return text, data["img"]


bot.infinity_polling()
