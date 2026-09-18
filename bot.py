import telebot
import os
import time
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    LabeledPrice
)

bot = telebot.TeleBot("8616602526:AAEk0WwEeVLqrRPdnaHuAG_Vcd4FhbiXagQ")

# ===== НАСТРОЙКИ =====
ADMIN_ID = 1195946473
START_PHOTO = "https://i.imgur.com/zT9oi5q.jpeg"
CATALOG_PHOTO = "https://i.imgur.com/hjfrjya.jpeg"

# Реквизиты (копируются при нажатии)
CARD_NUMBER = "2202 2088 2391 7423"
WALLET_TON = "UQAuBieTaYe0N5fn2sR6RlNzlO_kG_Rc2V0zBvjN4NWj1fPK"

# ===== ТОВАРЫ =====
PRODUCTS = {
    "1": {"name": "Индия +91🇮🇳", "price_stars": 30, "price_rub": 37, "price_crypto": 0.35, "desc": "Отлега 2-3 года БЕЗ СПАМБЛОКА"},
    "2": {"name": "США +1🇺🇸", "price_stars": 35, "price_rub": 43, "price_crypto": 0.38, "desc": "Отлега 2 года, СО СПАМБЛОКОМ"},
    "3": {"name": "Мьянма🇲🇲", "price_stars": 29, "price_rub": 37, "price_crypto": 0.3, "desc": "Отлега 4 года, без спамблока"},
    "4": {"name": "Бангладеш +880🇧🇩", "price_stars": 40, "price_rub": 59, "price_crypto": 0.49, "desc": "Отлега 1 год"},
    "5": {"name": "Узбекистан +998🇺🇿", "price_stars": 65, "price_rub": 89, "price_crypto": 0.76, "desc": "Отлега 1 год"},
}

# ===== ФАЙЛЫ =====
USERS_FILE = "users.txt"
BLOCKED_FILE = "blocked.txt"

BLOCKED_USERS = set()

def load_blocked():
    if os.path.exists(BLOCKED_FILE):
        with open(BLOCKED_FILE, "r") as f:
            for line in f:
                if line.strip().isdigit():
                    BLOCKED_USERS.add(int(line.strip()))

def save_blocked():
    with open(BLOCKED_FILE, "w") as f:
        for uid in BLOCKED_USERS:
            f.write(str(uid) + "\n")

def save_user(uid):
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = [line.strip() for line in f if line.strip()]
    if str(uid) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(uid) + "\n")

admin_state = {}

# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🛒 Каталог"))
    markup.add(KeyboardButton("ℹ️ Помощь"), KeyboardButton("📞 Контакты"))
    return markup

# ===== /START =====
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in BLOCKED_USERS:
        bot.send_message(message.chat.id, "⛔ Вы заблокированы администратором.")
        return
    save_user(message.from_user.id)
    
    caption = (
        "👋 Добро пожаловать в *WertaShop*! ❤️\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🏪 Магазин качественных аккаунтов Telegram\n\n"
        "📌 Нажми *🛒 Каталог*, чтобы посмотреть товары\n"
        "📌 Если нужна помощь — *ℹ️ Помощь*\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ Быстрая выдача\n"
        "🛡 Честные аккаунты\n"
        "🕐 Поддержка 24/7"
    )
    try:
        bot.send_photo(message.chat.id, photo=START_PHOTO, caption=caption,
                       reply_markup=main_menu(), parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, caption, reply_markup=main_menu(), parse_mode="Markdown")

# ===== КАТАЛОГ =====
@bot.message_handler(func=lambda m: m.text == "🛒 Каталог")
def catalog(message):
    if message.from_user.id in BLOCKED_USERS:
        return
    save_user(message.from_user.id)
    
    text = "📦 *НАШИ АККАУНТЫ*\n"
    text += "━━━━━━━━━━━━━━━━━━━━\n\n"
    markup = InlineKeyboardMarkup()
    for key, p in PRODUCTS.items():
        text += f"{p['name']}\n"
        text += f"   {p['desc']}\n"
        text += f"   ⭐ {p['price_stars']} | 💳 {p['price_rub']} ₽ | 💎 {p['price_crypto']} TON\n"
        text += "   ➖➖➖➖➖➖➖➖➖➖\n"
        markup.add(InlineKeyboardButton(f"🛒 Купить {p['name']}", callback_data=f"buy_{key}"))
    
    try:
        bot.send_photo(message.chat.id, photo=CATALOG_PHOTO, caption=text,
                       reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# ===== ПОМОЩЬ =====
@bot.message_handler(func=lambda m: m.text == "ℹ️ Помощь")
def help_message(message):
    if message.from_user.id in BLOCKED_USERS:
        return
    bot.send_message(
        message.chat.id,
        "❓ *КАК СДЕЛАТЬ ЗАКАЗ*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "1️⃣ Нажми *🛒 Каталог*\n"
        "2️⃣ Выбери товар\n"
        "3️⃣ Оплати удобным способом\n"
        "4️⃣ Получи логин и пароль\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💬 Поддержка: @WertaSupport",
        parse_mode="Markdown"
    )

# ===== КОНТАКТЫ =====
@bot.message_handler(func=lambda m: m.text == "📞 Контакты")
def contacts(message):
    if message.from_user.id in BLOCKED_USERS:
        return
    bot.send_message(
        message.chat.id,
        "📞 *СВЯЗЬ С ПОДДЕРЖКОЙ*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "💬 Telegram: @WertaSupport\n"
        "📧 Email: WertaShopHelp@bk.ru",
        parse_mode="Markdown"
    )

# ===== ВЫБОР ТОВАРА =====
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy_callback(call):
    if call.from_user.id in BLOCKED_USERS:
        bot.answer_callback_query(call.id, "⛔ Вы заблокированы")
        return
    key = call.data.split("_")[1]
    product = PRODUCTS.get(key)
    if not product:
        bot.answer_callback_query(call.id, "❌ Товар не найден")
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⭐ Оплатить Stars", callback_data=f"pay_stars_{key}"))
    markup.add(InlineKeyboardButton("💳 Оплатить рублями", callback_data=f"pay_rub_{key}"))
    markup.add(InlineKeyboardButton("💎 Оплатить криптой (TON)", callback_data=f"pay_crypto_{key}"))
    bot.send_message(
        call.message.chat.id,
        f"🛒 *{product['name']}*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 {product['desc']}\n\n"
        f"💰 *ЦЕНА:*\n"
        f"⭐ {product['price_stars']} Stars\n"
        f"💳 {product['price_rub']} ₽\n"
        f"💎 {product['price_crypto']} TON\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        "Выбери способ оплаты:",
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

# ===== ОПЛАТА =====
@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def pay_callback(call):
    parts = call.data.split("_")
    method = parts[1]
    key = parts[2]
    product = PRODUCTS.get(key)

    if method == "stars":
        bot.send_invoice(
            chat_id=call.message.chat.id,
            title=f"Покупка {product['name']}",
            description=product['desc'],
            invoice_payload=f"stars_{key}_{call.from_user.id}",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(label=product['name'], amount=product['price_stars'])]
        )
        bot.answer_callback_query(call.id)

    elif method == "rub":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ Я оплатил(а)", callback_data=f"rub_paid_{key}"))
        bot.send_message(
            call.message.chat.id,
            f"💳 *ОПЛАТА РУБЛЯМИ*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🛒 Товар: *{product['name']}*\n"
            f"💰 Сумма: *{product['price_rub']} ₽*\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💳 *НОМЕР КАРТЫ* (нажми, чтобы скопировать):\n"
            f"`{CARD_NUMBER}`\n\n"
            f"📝 Назначение: покупка аккаунта\n"
            f"🏦 Перевод только на Сбербанк\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ После перевода нажми кнопку ниже",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        bot.answer_callback_query(call.id)

    elif method == "crypto":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ Я оплатил(а)", callback_data=f"crypto_paid_{key}"))
        bot.send_message(
            call.message.chat.id,
            f"💎 *ОПЛАТА КРИПТОЙ (TON)*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🛒 Товар: *{product['name']}*\n"
            f"💰 Сумма: *{product['price_crypto']} TON*\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💎 *АДРЕС КОШЕЛЬКА* (нажми, чтобы скопировать):\n"
            f"`{WALLET_TON}`\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ После перевода нажми кнопку ниже",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        bot.answer_callback_query(call.id)

# ===== УСПЕШНАЯ ОПЛАТА STARS =====
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    payload = message.successful_payment.invoice_payload
    parts = payload.split("_")
    key = parts[1]
    product = PRODUCTS.get(key)
    bot.send_message(
        message.chat.id,
        f"✅ *ОПЛАТА ПРОШЛА!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🛒 Товар: *{product['name']}*\n\n"
        "⏳ Ожидай подтверждения от администратора.\n"
        "💬 Если не пришло — @WertaSupport",
        parse_mode="Markdown"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Выдать аккаунт", callback_data=f"give_{key}_{message.from_user.id}"))
    bot.send_message(
        ADMIN_ID,
        f"💰 *НОВАЯ ОПЛАТА (Stars)!*\n\n"
        f"🛒 Товар: {product['name']}\n"
        f"👤 Покупатель: {message.from_user.first_name}\n"
        f"🆔 ID: `{message.from_user.id}`\n\n"
        "Нажми кнопку, чтобы выдать аккаунт:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ===== ПОДТВЕРЖДЕНИЕ РУБЛЕЙ / КРИПТЫ =====
@bot.callback_query_handler(func=lambda call: call.data.startswith("rub_paid_") or call.data.startswith("crypto_paid_"))
def manual_paid(call):
    if call.data.startswith("rub_paid_"):
        key = call.data.split("_")[2]
        method = "рублями"
    else:
        key = call.data.split("_")[2]
        method = "криптой"
    product = PRODUCTS.get(key)
    buyer_id = call.from_user.id
    buyer_name = call.from_user.first_name or "Без имени"
    bot.send_message(
        call.message.chat.id,
        f"✅ *ЗАЯВКА ПРИНЯТА!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🛒 Товар: *{product['name']}*\n\n"
        "⏳ Ожидай подтверждения от администратора.\n"
        "💬 Если не пришло — @WertaSupport",
        parse_mode="Markdown"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Выдать аккаунт", callback_data=f"give_{key}_{buyer_id}"))
    bot.send_message(
        ADMIN_ID,
        f"💰 *НОВАЯ ОПЛАТА ({method})!*\n\n"
        f"🛒 Товар: {product['name']}\n"
        f"👤 Покупатель: {buyer_name}\n"
        f"🆔 ID: `{buyer_id}`\n\n"
        "Нажми кнопку, чтобы выдать аккаунт:",
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

# ===== КНОПКА "ВЫДАТЬ" =====
@bot.callback_query_handler(func=lambda call: call.data.startswith("give_"))
def give_account_start(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⛔ Нет доступа")
        return
    parts = call.data.split("_")
    key = parts[1]
    buyer_id = int(parts[2])
    admin_state[ADMIN_ID] = {"buyer_id": buyer_id, "key": key}
    bot.send_message(
        ADMIN_ID,
        f"✍️ Введи данные аккаунта для покупателя `{buyer_id}`:\n\n"
        "Формат: `логин:пароль`\n"
        "Пример: `india_acc1:mypass123`\n\n"
        "Отмена: /cancel",
        parse_mode="Markdown"
    )
    bot.answer_callback_query(call.id)

# ===== ПРИЁМ ДАННЫХ ОТ АДМИНА =====
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and ADMIN_ID in admin_state)
def admin_send_account(message):
    data = admin_state.get(ADMIN_ID)
    if not data:
        return
    text = message.text.strip()
    if ":" not in text:
        bot.send_message(ADMIN_ID, "❌ Неверный формат! Нужно `логин:пароль`", parse_mode="Markdown")
        return
    buyer_id = data["buyer_id"]
    login, password = text.split(":", 1)
    try:
        bot.send_message(
            buyer_id,
            f"✅ *ОПЛАТА ПОДТВЕРЖДЕНА!*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🔐 Логин: `{login}`\n"
            f"🔑 Пароль: `{password}`\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ Сохрани эти данные!",
            parse_mode="Markdown"
        )
        bot.send_message(ADMIN_ID, f"✅ Аккаунт выдан покупателю `{buyer_id}`", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Не смог отправить: {e}")
    admin_state.pop(ADMIN_ID, None)

# ===== БЫСТРАЯ ВЫДАЧА =====
@bot.message_handler(commands=['give'])
def give_manual(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        parts = message.text.split(maxsplit=2)
        buyer_id = int(parts[1])
        account_data = parts[2]
        login, password = account_data.split(":", 1)
        bot.send_message(
            buyer_id,
            f"✅ *ОПЛАТА ПОДТВЕРЖДЕНА!*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🔐 Логин: `{login}`\n"
            f"🔑 Пароль: `{password}`\n\n"
            "⚠️ Сохрани эти данные!",
            parse_mode="Markdown"
        )
        bot.send_message(ADMIN_ID, f"✅ Аккаунт выдан `{buyer_id}`", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Формат: `/give ID логин:пароль`\nОшибка: {e}", parse_mode="Markdown")

# ===== ОТМЕНА =====
@bot.message_handler(commands=['cancel'])
def cancel_action(message):
    if message.from_user.id != ADMIN_ID:
        return
    admin_state.pop(ADMIN_ID, None)
    bot.send_message(ADMIN_ID, "✅ Действие отменено.")

# ===== ЗАПУСК =====
if __name__ == "__main__":
    load_blocked()
    print("✅ Бот WertaShop запущен!")
    start_time = time.time()
    while time.time() - start_time < 230:
        try:
            bot.polling(none_stop=True, timeout=10, long_polling_timeout=5)
        except Exception as e:
            print("Ошибка:", e)
            time.sleep(2)
    print("Цикл завершён")
