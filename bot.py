import telebot
import os
import time
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice
)

bot = telebot.TeleBot("8616602526:AAEk0WwEeVLqrRPdnaHuAG_Vcd4FhbiXagQ", parse_mode="HTML")

# ===== НАСТРОЙКИ =====
ADMIN_ID = 1195946473
START_PHOTO = "https://i.imgur.com/zT9oi5q.jpeg"
CATALOG_PHOTO = "https://i.imgur.com/hjfrjya.jpeg"

CARD_NUMBER = "2202 2088 2391 7423"
WALLET_TON = "UQAuBieTaYe0N5fn2sR6RlNzlO_kG_Rc2V0zBvjN4NWj1fPK"

# ID премиум-эмодзи
EMOJI_CATALOG = "5877332341331857066"
EMOJI_HELP = "6039422865189638057"
EMOJI_CONTACTS = "6039605143601680423"

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

# ===== INLINE-МЕНЮ (в приветствии) =====
def main_inline_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        "Каталог",
        callback_data="open_catalog",
        icon_custom_emoji_id=EMOJI_CATALOG
    ))
    markup.add(InlineKeyboardButton(
        "Помощь",
        callback_data="open_help",
        icon_custom_emoji_id=EMOJI_HELP
    ))
    markup.add(InlineKeyboardButton(
        "Контакты",
        callback_data="open_contacts",
        icon_custom_emoji_id=EMOJI_CONTACTS
    ))
    return markup

# ===== /START =====
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in BLOCKED_USERS:
        bot.send_message(message.chat.id, "⛔ Вы заблокированы администратором.")
        return
    save_user(message.from_user.id)
    
    caption = (
        "👋 Добро пожаловать в <b>WertaShop</b>! ❤️\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🏪 Магазин качественных аккаунтов Telegram\n\n"
        "📌 Нажми кнопку ниже, чтобы посмотреть товары\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⚡ Быстрая выдача\n"
        "🛡 Честные аккаунты\n"
        "🕐 Поддержка 24/7"
    )
    try:
        bot.send_photo(message.chat.id, photo=START_PHOTO, caption=caption,
                       reply_markup=main_inline_menu())
    except:
        bot.send_message(message.chat.id, caption, reply_markup=main_inline_menu())

# ===== ОБРАБОТКА КНОПОК МЕНЮ =====
@bot.callback_query_handler(func=lambda call: call.data == "open_catalog")
def open_catalog(call):
    bot.answer_callback_query(call.id)
    show_catalog(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "open_help")
def open_help(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "❓ <b>КАК СДЕЛАТЬ ЗАКАЗ</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "1️⃣ Нажми <b>Каталог</b>\n"
        "2️⃣ Выбери товар\n"
        "3️⃣ Оплати удобным способом\n"
        "4️⃣ Получи логин и пароль\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💬 Поддержка: @WertaSupport"
    )

@bot.callback_query_handler(func=lambda call: call.data == "open_contacts")
def open_contacts(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "📞 <b>СВЯЗЬ С ПОДДЕРЖКОЙ</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "💬 Telegram: @WertaSupport\n"
        "📧 Email: WertaShopHelp@bk.ru"
    )

# ===== КАТАЛОГ =====
def show_catalog(chat_id):
    if chat_id in BLOCKED_USERS:
        return
    save_user(chat_id)
    
    text = "📦 <b>НАШИ АККАУНТЫ</b>\n"
    text += "━━━━━━━━━━━━━━━━━━━━\n\n"
    markup = InlineKeyboardMarkup()
    for key, p in PRODUCTS.items():
        text += f"{p['name']}\n"
        text += f"   {p['desc']}\n"
        text += f"   ⭐ {p['price_stars']} | 💳 {p['price_rub']} ₽ | 💎 {p['price_crypto']} TON\n"
        text += "   ➖➖➖➖➖➖➖➖➖➖\n"
        markup.add(InlineKeyboardButton(f"🛒 Купить {p['name']}", callback_data=f"buy_{key}"))
    
    try:
        bot.send_photo(chat_id, photo=CATALOG_PHOTO, caption=text, reply_markup=markup)
    except:
        bot.send_message(chat_id, text, reply_markup=markup)

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
        f"🛒 <b>{product['name']}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📝 {product['desc']}\n\n"
        f"💰 <b>ЦЕНА:</b>\n"
        f"⭐ {product['price_stars']} Stars\n"
        f"💳 {product['price_rub']} ₽\n"
        f"💎 {product['price_crypto']} TON\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        "Выбери способ оплаты:",
        reply_markup=markup
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
            f"💳 <b>ОПЛАТА РУБЛЯМИ</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🛒 Товар: <b>{product['name']}</b>\n"
            f"💰 Сумма: <b>{product['price_rub']} ₽</b>\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💳 <b>НОМЕР КАРТЫ</b> (нажми, чтобы скопировать):\n"
            f"<code>{CARD_NUMBER}</code>\n\n"
            f"📝 Назначение: покупка аккаунта\n"
            f"🏦 Перевод только на Сбербанк\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ После перевода нажми кнопку ниже",
            reply_markup=markup
        )
        bot.answer_callback_query(call.id)

    elif method == "crypto":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ Я оплатил(а)", callback_data=f"crypto_paid_{key}"))
        bot.send_message(
            call.message.chat.id,
            f"💎 <b>ОПЛАТА КРИПТОЙ (TON)</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🛒 Товар: <b>{product['name']}</b>\n"
            f"💰 Сумма: <b>{product['price_crypto']} TON</b>\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💎 <b>АДРЕС КОШЕЛЬКА</b> (нажми, чтобы скопировать):\n"
            f"<code>{WALLET_TON}</code>\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ После перевода нажми кнопку ниже",
            reply_markup=markup
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
        f"✅ <b>ОПЛАТА ПРОШЛА!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🛒 Товар: <b>{product['name']}</b>\n\n"
        "⏳ Ожидай подтверждения от администратора.\n"
        "💬 Если не пришло — @WertaSupport"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Выдать аккаунт", callback_data=f"give_{key}_{message.from_user.id}"))
    bot.send_message(
        ADMIN_ID,
        f"💰 <b>НОВАЯ ОПЛАТА (Stars)!</b>\n\n"
        f"🛒 Товар: {product['name']}\n"
        f"👤 Покупатель: {message.from_user.first_name}\n"
        f"🆔 ID: <code>{message.from_user.id}</code>\n\n"
        "Нажми кнопку, чтобы выдать аккаунт:",
        reply_markup=markup
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
        f"✅ <b>ЗАЯВКА ПРИНЯТА!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🛒 Товар: <b>{product['name']}</b>\n\n"
        "⏳ Ожидай подтверждения от администратора.\n"
        "💬 Если не пришло — @WertaSupport"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Выдать аккаунт", callback_data=f"give_{key}_{buyer_id}"))
    bot.send_message(
        ADMIN_ID,
        f"💰 <b>НОВАЯ ОПЛАТА ({method})!</b>\n\n"
        f"🛒 Товар: {product['name']}\n"
        f"👤 Покупатель: {buyer_name}\n"
        f"🆔 ID: <code>{buyer_id}</code>\n\n"
        "Нажми кнопку, чтобы выдать аккаунт:",
        reply_markup=markup
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
        f"✍️ Введи данные аккаунта для покупателя <code>{buyer_id}</code>:\n\n"
        "Формат: <code>логин:пароль</code>\n"
        "Пример: <code>india_acc1:mypass123</code>\n\n"
        "Отмена: /cancel"
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
        bot.send_message(ADMIN_ID, "❌ Неверный формат! Нужно <code>логин:пароль</code>")
        return
    buyer_id = data["buyer_id"]
    login, password = text.split(":", 1)
    try:
        bot.send_message(
            buyer_id,
            f"✅ <b>ОПЛАТА ПОДТВЕРЖДЕНА!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🔐 Логин: <code>{login}</code>\n"
            f"🔑 Пароль: <code>{password}</code>\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ Сохрани эти данные!"
        )
        bot.send_message(ADMIN_ID, f"✅ Аккаунт выдан покупателю <code>{buyer_id}</code>")
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
            f"✅ <b>ОПЛАТА ПОДТВЕРЖДЕНА!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🔐 Логин: <code>{login}</code>\n"
            f"🔑 Пароль: <code>{password}</code>\n\n"
            "⚠️ Сохрани эти данные!"
        )
        bot.send_message(ADMIN_ID, f"✅ Аккаунт выдан <code>{buyer_id}</code>")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Формат: <code>/give ID логин:пароль</code>\nОшибка: {e}")

# ===== ОТМЕНА =====
@bot.message_handler(commands=['cancel'])
def cancel_action(message):
    if message.from_user.id != ADMIN_ID:
        return
    admin_state.pop(ADMIN_ID, None)
    bot.send_message(ADMIN_ID, "✅ Действие отменено.")

# ===== АДМИН-ПАНЕЛЬ =====
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ У тебя нет доступа к админке.")
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"))
    bot.send_message(
        message.chat.id,
        "🔧 <b>Админ-панель WertaShop</b>\n\n"
        "Команды:\n"
        "<code>/give ID логин:пароль</code> — выдать аккаунт\n"
        "<code>/block ID</code> — заблокировать\n"
        "<code>/unblock ID</code> — разблокировать\n"
        "<code>/broadcast Текст</code> — рассылка\n"
        "<code>/cancel</code> — отменить ввод\n\n"
        "Или нажми кнопку:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def admin_stats(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⛔ Нет доступа")
        return
    users_count = 0
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f:
            users_count = len([l for l in f if l.strip()])
    bot.send_message(
        call.message.chat.id,
        f"📊 <b>Статистика:</b>\n\n"
        f"👥 Пользователей: {users_count}\n"
        f"⛔ Заблокировано: {len(BLOCKED_USERS)}"
    )
    bot.answer_callback_query(call.id)

# ===== БЛОКИРОВКА =====
@bot.message_handler(commands=['block'])
def block_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        uid = int(message.text.split()[1])
        BLOCKED_USERS.add(uid)
        save_blocked()
        bot.send_message(message.chat.id, f"✅ Пользователь {uid} заблокирован.")
    except:
        bot.send_message(message.chat.id, "❌ Формат: /block ID_пользователя")

@bot.message_handler(commands=['unblock'])
def unblock_user(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        uid = int(message.text.split()[1])
        BLOCKED_USERS.discard(uid)
        save_blocked()
        bot.send_message(message.chat.id, f"✅ Пользователь {uid} разблокирован.")
    except:
        bot.send_message(message.chat.id, "❌ Формат: /unblock ID_пользователя")

# ===== РАССЫЛКА =====
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        bot.send_message(message.chat.id, "❌ Напиши: <code>/broadcast Твой текст</code>")
        return
    if not os.path.exists(USERS_FILE):
        bot.send_message(message.chat.id, "❌ Нет файла users.txt")
        return
    with open(USERS_FILE, "r") as f:
        users = [int(line.strip()) for line in f if line.strip().isdigit()]
    sent = 0
    for uid in users:
        try:
            bot.send_message(uid, text)
            sent += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ Рассылка отправлена {sent} пользователям.")

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
