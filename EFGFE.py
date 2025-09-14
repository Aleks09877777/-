import os
import logging
import random
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
BOT_TOKEN = "8210437899:AAHjY8StVawee4XJ-jeBebdzI_vHy4WZEsU"

# Состояния пользователя
USER_STATES = {}


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    USER_STATES[user.id] = {"step": 1, "screenshots_count": 0, "completed_tasks": []}

    # Приветственное сообщение
    welcome_text = f"🎉 Привет, {user.mention_html()}!\n\nВ этом боте ты можешь получить эксклюзивный NFT подарок совершенно бесплатно! 🎁"

    # Кнопка "ПОЛУЧИТЬ ПОДАРОК"
    keyboard = [
        [InlineKeyboardButton("🎁 ПОЛУЧИТЬ ПОДАРОК", callback_data="get_gift")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


# Обработка нажатия кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    await query.answer()

    if user.id not in USER_STATES:
        USER_STATES[user.id] = {"step": 1, "screenshots_count": 0, "completed_tasks": []}

    if query.data == "get_gift":
        # Этап 1: Выбираем подарок...
        await query.edit_message_text("🎁 Выбираем подарок...")
        await asyncio.sleep(2)

        # Этап 2: Ещё чуть-чуть...
        await query.edit_message_text("⏳ Ещё чуть-чуть...")
        await asyncio.sleep(2)

        # Этап 3: Почти готово...
        await query.edit_message_text("✨ Почти готово...")
        await asyncio.sleep(2)

        # Поздравление с подарком
        gift_text  = "🎉 Поздравляем! Вам выпал эксклюзивный NFT - http://t.me/nft/TopHat-19884 !\n\n"
        gift_text += "Чтобы получить NFT, выполните простые задания ниже 👇\n\n"
        gift_text += "Наши отзывы\nhttps://t.me/Rosa13823"

        keyboard = [
            [InlineKeyboardButton("📋 ПОКАЗАТЬ ЗАДАНИЯ", callback_data="show_tasks")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            gift_text,
            reply_markup=reply_markup
        )

    elif query.data == "show_tasks":
        # Показываем задания
        task_text = "🎯 ЗАДАНИЯ ДЛЯ ПОЛУЧЕНИЯ NFT\n\n"

        task_text += "🔹 ЗАДАНИЕ 1/3:\n"
        task_text += "📱 Напишите 30 комментариев в TikTok/Likee с текстом:\n"
        task_text += "'прикиньте мне в боте @Rosa155_bot дали 3000 звезд'\n\n"
        task_text += "✅ Обязательно:\n"
        task_text += "• Лайкайте свои комментарии\n"
        task_text += "• Комментируйте разные видео\n"
        task_text += "• Отправьте минимум 30 скриншотов\n\n"
        task_text += "📸 Отправьте скриншоты выполнения задания"

        keyboard = [
            [InlineKeyboardButton("📷 ОТПРАВИТЬ СКРИНШОТЫ", callback_data="send_screenshots")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            task_text,
            reply_markup=reply_markup
        )
        USER_STATES[user.id]["step"] = 2

    elif query.data == "send_screenshots":
        instruction_text = "📸 Отправьте скриншоты комментариев из TikTok/Likee\n\n"
        instruction_text += "⚠️ Требования:\n"
        instruction_text += "• Минимум 30 скриншотов\n"
        instruction_text += "• На каждом скриншоте виден ваш комментарий\n"
        instruction_text += "• Видно лайк под комментарием\n\n"
        instruction_text += "📎 Можно отправлять по одному или несколько сразу"

        await query.edit_message_text(instruction_text)
        USER_STATES[user.id]["step"] = 3

    elif query.data == "next_task":
        # Второе задание - регистрация на сайте
        task_text = "🎯 ЗАДАНИЕ 2/3 ВЫПОЛНЕНО!\n\n"
        task_text += "🔹 ЗАДАНИЕ 3/3:\n"
        task_text += "💰 Пополните баланс на сайте и сыграйте пару игр\n\n"
        task_text += "💳 Минимальный депозит: 1000 рублей\n"
        task_text += "После пополнения:\n"
        task_text += "1. Сделайте скриншот пополнения аккаунта\n"
        task_text += "2. Отправьте скриншот сюда\n"
        task_text += "3. Получите NFT мгновенно!"

        keyboard = [
            [InlineKeyboardButton("🌐 ПЕРЕЙТИ НА САЙт", url="https://1wilib.life/v3/3159/cards-promo?p=9pry")],
            [InlineKeyboardButton("📷 ОТПРАВИТЬ СКРИНШОТ ПОПОЛНЕНИЯ", callback_data="send_deposit_proof")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(task_text, reply_markup=reply_markup)
        USER_STATES[user.id]["step"] = 5

    elif query.data == "send_deposit_proof":
        instruction_text = "📸 Отправьте скриншот пополнения баланса\n\n"
        instruction_text += "На скриншоте должно быть видно:\n"
        instruction_text += "• Сумму пополнения\n"
        instruction_text += "• Адрес кошелька\n"
        instruction_text += "• Статус транзакции\n"
        instruction_text += "• Дата и время"

        await query.edit_message_text(instruction_text)
        USER_STATES[user.id]["step"] = 6


# Обработка скриншотов
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in USER_STATES:
        USER_STATES[user.id] = {"step": 1, "screenshots_count": 0, "completed_tasks": []}

    current_state = USER_STATES[user.id]

    # Обработка скриншотов для задания 1
    if current_state["step"] == 3 and update.message.photo:
        current_state["screenshots_count"] += 1
        screenshots_left = 30 - current_state["screenshots_count"]

        if screenshots_left > 0:
            await update.message.reply_text(
                f"📸 Скриншот принят! Осталось отправить: {screenshots_left}\n\n"
                f"✅ Принято: {current_state['screenshots_count']}/30"
            )
        else:
            # Задание выполнено
            current_state["completed_tasks"].append("tiktok_comments")
            current_state["step"] = 4

            # Второе задание - регистрация на сайте
            task_text = "🎉 ЗАДАНИЕ 1/3 ВЫПОЛНЕНО!\n\n"
            task_text += "🔹 ЗАДАНИЕ 2/3:\n"
            task_text += "🌐 Зарегистрируйтесь на сайте нашего партнера\n\n"
            task_text += "📋 Что нужно сделать:\n"
            task_text += "1. Перейдите по ссылке ниже\n"
            task_text += "2. Заполните форму регистрации\n"

            keyboard = [
                [InlineKeyboardButton("🌐 ПЕРЕЙТИ К РЕГИСТРАЦИИ", url="https://1wilib.life/v3/3159/cards-promo?p=9pry")],
                [InlineKeyboardButton("✅ Я ЗАРЕГИСТРИРОВАЛСЯ", callback_data="next_task")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(task_text, reply_markup=reply_markup)

    # Обработка скриншотов пополнения баланса
    elif current_state["step"] == 6 and update.message.photo:
        # Задание выполнено - выдача NFT
        current_state["completed_tasks"].append("deposit_made")
        current_state["step"] = 7

        success_text = "🎉 ПОЗДРАВЛЯЕМ! ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ!\n\n"
        success_text += "✅ Ваш NFT http://t.me/nft/TopHat-19884 будет отправлен в течении 24 часов!\n\n"
        success_text += "Наши отзывы\nhttps://t.me/Rosa13823"

        await update.message.reply_text(success_text)

    # Если пользователь отправляет текст вместо скриншотов
    elif update.message.text and current_state["step"] in [3, 6]:
        await update.message.reply_text("⚠️ Пожалуйста, отправьте скриншот выполнения задания")

    # Если пользователь на неправильном шаге
    elif current_state["step"] not in [3, 6] and (update.message.photo or update.message.text):
        await update.message.reply_text("⚠️ Сначала выполните текущее задание")


# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

    # Запускаем бота
    print("🤖 Бот запускается...")
    print(f"📍 Токен: {BOT_TOKEN}")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("🎯 Бот готов принимать задания!")

    application.run_polling()


if __name__ == "__main__":
    main()