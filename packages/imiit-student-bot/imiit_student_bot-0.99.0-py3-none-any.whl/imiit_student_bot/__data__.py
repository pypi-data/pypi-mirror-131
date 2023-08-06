"""Reads data for student bot."""
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

RESPONSE = {
    "en": {
        "Start": "👋 Sup {user}! I am a telegram bot for IMIIT students, you can use me to get class schedule, "
        "that you can add to your calendar, a map and links to university information resources 🎓",
        "About": {
            "Website": "https://imiit.ru",
            "Contacts": "https://imiit.ru/contacts",
            "VK": "https://vk.com/imdtrut",
            "Instagram": "https://www.instagram.com/imdt_rut/",
            "Youtube": "https://www.youtube.com/channel/UCqKcmSQ2onutsAxyouiV8Dg",
        },
        "Timetable": "To get the timetable, send me a message with the name of your group in the format "
        "“<b>утц-111</b>”",
        "send_timetable": "<a href='https://miit.ru/timetable?query={group}'>Click here and choose {group}</a>",
        "Map": "I suppose you need a map...",
        "Unknown": "Whoops... I cannot understand you",
        "Keyboard": [["IMIIT", "Map"], ["Timetable"]],
    },
    "ru": {
        "Start": "👋 Привет {user}! Я телеграм бот для студентов ИУЦТ, с помощью меня ты можешь получить рассписание "
        "занятий, которое можно добавить себе в календарь, карту и ссылки на информационные ресурсы "
        "университета 🎓",
        "About": {
            "Сайт": "https://imiit.ru",
            "Контакты": "https://imiit.ru/contacts",
            "ВКонтакте": "https://vk.com/imdtrut",
            "Инстаграм": "https://www.instagram.com/imdt_rut/",
            "Ютуб": "https://www.youtube.com/channel/UCqKcmSQ2onutsAxyouiV8Dg",
        },
        "Timetable": "Чтобы получить расписание занятий отпраь мне сообщение с названием своей группы в формате "
        "“<b>утц-111</b>”",
        "send_timetable": "<a href='https://miit.ru/timetable?query={group}'>Нажми сюда и выбери {group}</a>",
        "Map": "Полагаю, вам нужна карта...",
        "Unknown": "Упс... Я не могу вас понять",
        "Keyboard": [["Об ИУЦТ", "Карта"], ["Расписание"]],
    },
    "Error": "Пожалуйста, выберите язык интерфейса бота /lang<br>Please select the bot's interface language /lang",
    "Sticker": {
        "Lang": "CAACAgIAAxkBAAOyYZ8VmefmdiWW-tvTrhNjHwoeKaMAAgoQAAIGw_lIaz2ySmFEEIsiBA",
        "Start": "CAACAgIAAxkBAAO2YZ8Wimg_8TAkOxjC5-0AAUF4eU7qAAIUEgACcJ9ISxMYE_KU6GJ4IgQ",
        "About": "CAACAgIAAxkBAAOyYZ8VmefmdiWW-tvTrhNjHwoeKaMAAgoQAAIGw_lIaz2ySmFEEIsiBA",
        "Timetable": "CAACAgIAAxkBAAOkYZ740rXtHFPfNP_GdbfbzJkNjV8AAssTAAK0fNhLcv9-ge1zHI4iBA",
        "Map": "CAACAgIAAxkBAAOmYZ748YyokOEtNoqSDHK7OHABbQ0AAhMRAAJIvYhL90mDPXJLLOEiBA",
        "Unknown": "CAACAgIAAxkBAAOoYZ75EPROM0KZV7l9dwJHG6pDuPQAAtoUAAJ_dllLgmbRdWj7bQIiBA",
    },
}


def get_groups() -> dict:
    group_list = requests.get("https://miit.ru/timetable/", allow_redirects=True).text
    soup = BeautifulSoup(group_list, "html.parser")
    return {
        group.string.strip().lower(): group["href"].strip("/timetable/")
        for group in soup.find_all("a", href=re.compile("\/timetable\/\d*"))
    }


def get_timetable(group_id):
    timetables_df = pd.read_html(f"https://miit.ru/timetable/{group_id}", index_col=0)
    timetables = []
    for timetable in timetables_df:
        timetable.dropna(axis=1, how="all", inplace=True)
        timetables.append(timetable.to_dict(orient="dict"))
    return timetables
