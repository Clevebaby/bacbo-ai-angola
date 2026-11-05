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
        "Bem-vindo ao nosso sistema!\n\n"
        "📸 Envia um screenshot do gráfico Bac Bo "
        "para iniciar a análise visual.\n\n"
        "⚠️ As análises são probabilísticas "
        "e não garantem resultados."
    )


async def analisar_imagem(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "📸 Screenshot recebido!\n\n"
        "🔍 A preparar a análise visual...\n\n"
        "⚠️ A análise automática ainda está em desenvolvimento."
    )


def main():

    if not TOKEN:
        raise ValueError("Token não configurado!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(filters.PHOTO, analisar_imagem)
    )

    print("BAC BO AI PRO ANGOLA iniciado!")

    # Mantém o bot a funcionar e a receber mensagens
    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
