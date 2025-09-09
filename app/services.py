# Данные для услуг, филиалов и описаний
SERVICES = {
    "neuro_diagnostic": "Нейродиагностика - 5000 руб.",
    "neuro_psychologist": "Занятия с нейропсихологом - 4000 руб./сессия",
    "sensory_integration": "Сенсорная интеграция - 4500 руб.",
    "speech_diagnostic": "Диагностика речевого развития - 3000 руб.",
    "logopedist": "Занятия с логопедом - 3500 руб./сессия",
    "child_psychologist": "Консультация детского психолога - 4000 руб.",
    "wechsler_test": "Тест Векслера - 6000 руб.",
    "floortime": "Флортайм - 4500 руб./сессия",
    "online": "Онлайн-развитие"
}

BRANCHES = [
    "Нахимовский проспект (Москва)",
    "Молодежная (Москва)",
    "Отрадное (Москва)",
    "ОНЛАЙН формат"
]

MULT_TABLE_BRANCHES = [
    "Отрадное (Москва)",
    "Молодежная (Москва)"
]

import json
import os

# Загрузка данных из JSON
def load_service_data():
    try:
        with open('data/service_details.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

SERVICE_DATA = load_service_data()
SERVICE_DETAILS = SERVICE_DATA.get('service_details', {})
ONLINE_DETAILS = SERVICE_DATA.get('online_details', {})

# Сохранение данных в JSON
def save_service_data():
    with open('data/service_details.json', 'w', encoding='utf-8') as f:
        json.dump({
            'service_details': SERVICE_DETAILS,
            'online_details': ONLINE_DETAILS
        }, f, ensure_ascii=False, indent=2)