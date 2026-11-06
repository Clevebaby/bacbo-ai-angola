import os
import logging
import asyncio

from google import genai
from google.genai import types

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# CONFIGURAÇÕES
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# CLIENTE GEMINI
client = None


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🚀 BAC BO AI PRO ANGOLA\n\n"
        "Bem-vindo ao sistema de análise visual!\n\n"
        "📸 Envia um screenshot do gráfico Bac Bo.\n\n"
        "🧠 A inteligência artificial irá analisar:\n"
        "🔵 Player\n"
        "🔴 Banker\n"
        "🟡 Tie\n\n"
        "📊 Estatísticas e padrões visíveis.\n\n"
        "⚠️ Os resultados são aleatórios. "
        "A análise não prevê resultados futuros "
        "nem garante ganhos."
    )


def analisar_com_gemini(image_bytes):

    prompt = """
    És um assistente especializado na leitura visual
    de gráficos históricos do jogo Bac Bo.

    Analisa cuidadosamente a imagem recebida.

    TAREFAS:

    1. Identifica os resultados históricos visíveis.
    2. Identifica Player (azul).
    3. Identifica Banker (vermelho).
    4. Identifica Tie (empate).
    5. Conta os resultados que consegues identificar.
    6. Identifica sequências visíveis.
    7. Indica se existem partes ilegíveis.

    APRESENTA O RELATÓRIO:

    📊 BAC BO AI PRO

    🔵 Player: quantidade identificada
    🔴 Banker: quantidade identificada
    🟡 Tie: quantidade identificada

    📈 Padrões observados:
    Descreve as sequências visíveis.

    🔍 Qualidade da imagem:
    Boa, média ou baixa.

    ⚠️ IMPORTANTE:

    Não inventes resultados que não consegues ler.
    Não confundas padrões históricos com previsões.
    Não afirmes que um resultado futuro é garantido.
    Bac Bo é um jogo de resultados aleatórios.

    Se não conseguires interpretar a imagem,
    explica claramente o motivo.
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            ),
            prompt
        ]
    )

    return response.text


async def analisar_imagem(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message

    await message.reply_text(
        "📸 Screenshot recebido!\n\n"
        "🧠 A inteligência artificial está "
        "a analisar a imagem...\n\n"
        "⏳ Aguarda um momento."
    )

    try:

        photo = message.photo[-1]

        telegram_file = await photo.get_file()

        image_bytes = await telegram_file.download_as_bytearray()

        resultado = await asyncio.to_thread(
            analisar_com_gemini,
            bytes(image_bytes)
        )

        if not resultado:
            resultado = "Não foi possível interpretar a imagem."

        await message.reply_text(
            "✅ ANÁLISE CONCLUÍDA!\n\n" + resultado
        )

    except Exception:

        logger.exception("Erro durante a análise da imagem")

        await message.reply_text(
            "❌ Não foi possível analisar a imagem.\n\n"
            "Verifica a ligação à API Gemini e tenta novamente."
        )


def main():

    global client

    if not TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN não configurado!"
        )

    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY não configurada!"
        )

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            analisar_imagem
        )
    )

    print("🚀 BAC BO AI PRO ANGOLA iniciado!")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
