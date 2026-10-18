import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

# Carrega variáveis do arquivo .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL_ID = os.getenv("CANAL_ID")

# Configuração de logs no terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Lista de ofertas automáticas de exemplo (Aqui você pode puxar de uma API ou lista própria)
OFERTAS_AUTOMATICAS = [
    {
        "titulo": "Fone de Ouvido Bluetooth TWS",
        "preco_antigo": "R$ 149,90",
        "preco_novo": "R$ 59,90",
        "link": "https://shope.ee/seu-link-afiliado-aqui"
    },
    {
        "titulo": "Smartwatch Relógio Inteligente D20",
        "preco_antigo": "R$ 99,90",
        "preco_novo": "R$ 39,90",
        "link": "https://shope.ee/seu-link-afiliado-aqui"
    },
    {
        "titulo": "Suporte Veicular Magnético para Celular",
        "preco_antigo": "R$ 49,90",
        "preco_novo": "R$ 19,90",
        "link": "https://shope.ee/seu-link-afiliado-aqui"
    }
]

contador_oferta = 0

async def disparar_oferta_automatica(app):
    global contador_oferta
    if not CANAL_ID:
        logging.warning("CANAL_ID não configurado no .env!")
        return

    # Pega uma oferta da lista em ordem circular
    oferta = OFERTAS_AUTOMATICAS[contador_oferta % len(OFERTAS_AUTOMATICAS)]
    contador_oferta += 1

    texto = (
        "🔥 **ACHADINHO IMPERDÍVEL!** 🔥\n\n"
        f"📦 **{oferta['titulo']}**\n"
        f"❌ De: ~~{oferta['preco_antigo']}~~\n"
        f"✅ Por apenas: **{oferta['preco_novo']}**\n\n"
        f"🛒 [GARANTIR COM DESCONTO]({oferta['link']})\n\n"
        "⚡ *Corra que o estoque pode acabar rápido!*"
    )

    try:
        await app.bot.send_message(
            chat_id=CANAL_ID,
            text=texto,
            parse_mode='Markdown',
            disable_web_page_preview=False
        )
        logging.info("Oferta automática disparada com sucesso no canal!")
    except Exception as e:
        logging.error(f"Erro ao disparar oferta automática: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Robô de Ofertas Afiliados Ativo e Operando! 🚀")

if __name__ == '__main__':
    if not TOKEN:
        raise ValueError("Token do bot não encontrado! Verifique o arquivo .env.")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))

    # Agendador configurado para testar a cada 10 segundos
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: app.job_queue.run_once(lambda ctx: disparar_oferta_automatica(app), 0),
        'interval',
        seconds=10
    )
    scheduler.start()

    print("Bot rodando com agendador automático ativado!")
    app.run_polling()