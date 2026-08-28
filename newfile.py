import random
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# --- НАСТРОЙКИ ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "8592916495:AAE9LL0n8_pA2h3G5I7kVyistpafU9BkSNU"
# Путь к папке, где лежит сам скрипт и видео (работает и на телефоне, и на сервере)
BASE_DIR = os.getcwd()

VIDEO_DANCE = os.path.join(BASE_DIR, "dance.mp4")
VIDEO_BELIE = os.path.join(BASE_DIR, "belie.mp4")
VIDEO_BUKHET = os.path.join(BASE_DIR, "buhaet.mp4")
VIDEO_PHOTO = os.path.join(BASE_DIR, "foto.mp4")

# --- ПРОВЕРКА ФАЙЛОВ (ВЫНЕСЕНА НАВЕРХ) ---
def check_video_file(video_path: str) -> bool:
    if not os.path.exists(video_path):
        logger.warning(f"Файл не найден: {video_path}")
        return False
    return True

# --- СЛУЧАЙНЫЕ ФРАЗЫ ДЛЯ ВИДЕО ---
DANCE_PHRASES = [
    "🕺 Депутат Кирилл Бугрименко танцует! Зажигай!",
    "🕺 Это не просто танцы, это искусство!",
    "🕺 Кто сказал, что политики не умеют двигаться?"
]
BELIE_PHRASES = [
    "👕 Депутат Кирилл Бугрименко меняет бельё! Чистота — залог здоровья!",
    "👕 Операция «Чистое бельё» прошла успешно!",
    "👕 Идеальная смена белья без лишних движений!"
]
BUKHET_PHRASES = [
    "🍺 Депутат Кирилл Бугрименко бухает! Веселье!",
    "🍺 Бокал для депутата — святое дело!",
    "🍺 После такого обязательно нужно закусить!"
]
PHOTO_PHRASES = [
    "📸 Фотосессия с депутатом! Улыбаемся, снимаем!",
    "📸 Позируем как звезда!",
    "📸 Депутат в кадре — это всегда событие!"
]

def get_phrase(phrases_list):
    return random.choice(phrases_list)

# --- КНОПКА "НАЗАД" ---
def back_button():
    keyboard = [
        [InlineKeyboardButton("⬅️ Вернуться в меню", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- КНОПКИ МЕНЮ ---
def get_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("💸 Донат на нужды", callback_data="donate")],
        [InlineKeyboardButton("🕺 Танцует", callback_data="dance")],
        [InlineKeyboardButton("👕 Смена белья", callback_data="belie")],
        [InlineKeyboardButton("🍺 Бухает", callback_data="buhaet")],
        [InlineKeyboardButton("📸 Фотосессия с депутатом", callback_data="photo")],
    ]
    return InlineKeyboardMarkup(keyboard)

# --- КОМАНДА /START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "😂 Привет! Я — депутат Кирилл Бугрименко.\n\n"
        "Выбери, что хочешь посмотреть:",
        reply_markup=get_menu_keyboard()
    )

# --- ОБРАБОТЧИК НАЖАТИЙ ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "back":
        await query.message.reply_text(
            "😂 Привет! Я — депутат Кирилл Бугрименко.\n\nВыбери, что хочешь посмотреть:",
            reply_markup=get_menu_keyboard()
        )
        return

    if query.data == "donate":
        await query.message.edit_text(
            "💸 Спасибо за поддержку!\n\n"
            "Донаты принимаются продуктами питания и наличными деньгами "
            "во втором кубрике (заходишь и сразу налево).\n\n"
            "Или просто отправь стикер в ответ 🥰",
            reply_markup=back_button()
        )
        
    elif query.data == "dance":
        if check_video_file(VIDEO_DANCE):
            try:
                with open(VIDEO_DANCE, 'rb') as video:
                    await query.message.reply_video(video, caption=get_phrase(DANCE_PHRASES), reply_markup=back_button())
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                await query.message.reply_text("❌ Ошибка при отправке видео.", reply_markup=back_button())
        else:
            await query.message.reply_text("❌ Видео не найдено.", reply_markup=back_button())

    elif query.data == "belie":
        if check_video_file(VIDEO_BELIE):
            try:
                with open(VIDEO_BELIE, 'rb') as video:
                    await query.message.reply_video(video, caption=get_phrase(BELIE_PHRASES), reply_markup=back_button())
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                await query.message.reply_text("❌ Ошибка при отправке видео.", reply_markup=back_button())
        else:
            await query.message.reply_text("❌ Видео не найдено.", reply_markup=back_button())

    elif query.data == "buhaet":
        if check_video_file(VIDEO_BUKHET):
            try:
                with open(VIDEO_BUKHET, 'rb') as video:
                    await query.message.reply_video(video, caption=get_phrase(BUKHET_PHRASES), reply_markup=back_button())
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                await query.message.reply_text("❌ Ошибка при отправке видео.", reply_markup=back_button())
        else:
            await query.message.reply_text("❌ Видео не найдено.", reply_markup=back_button())

    elif query.data == "photo":
        if check_video_file(VIDEO_PHOTO):
            try:
                with open(VIDEO_PHOTO, 'rb') as video:
                    await query.message.reply_video(video, caption=get_phrase(PHOTO_PHRASES), reply_markup=back_button())
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                await query.message.reply_text("❌ Ошибка при отправке видео.", reply_markup=back_button())
        else:
            await query.message.reply_text("❌ Видео не найдено.", reply_markup=back_button())

# --- ЗАПУСК ---
if __name__ == '__main__':
    print("--- Проверка файлов ---")
    for name, path in [("Танцует", VIDEO_DANCE), ("Бельё", VIDEO_BELIE), ("Бухает", VIDEO_BUKHET), ("Фото", VIDEO_PHOTO)]:
        if check_video_file(path):
            print(f"✅ {name}: OK")
        else:
            print(f"❌ {name}: Файл не найден!")

    application = ApplicationBuilder()\
        .token(TELEGRAM_TOKEN)\
        .read_timeout(30)\
        .write_timeout(30)\
        .connect_timeout(30)\
        .build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Бот запущен!")
    application.run_polling()
