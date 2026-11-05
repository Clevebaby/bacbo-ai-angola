import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 BAC BO AI PRO ANGOLA\n\n"
        "Bem-vindo!\n"
        "Envia um screenshot do gráfico Bac Bo "
        "para iniciar a análise visual.\n\n"
        "⚠️ As análises são probabilísticas, "
        "não garantem resultados."
    )

async def analisar_imagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]

    await update.message.reply_text(
        "📸 Screenshot recebido!\n\n"
        "🔍 Imagem preparada para análise.\n"
        "A análise automática ainda está em desenvolvimento."
    )

async def main():
    if not TOKEN:
        raise ValueError("Token do Telegram não configurado!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, analisar_imagem))

    print("BAC BO AI PRO iniciado!")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
