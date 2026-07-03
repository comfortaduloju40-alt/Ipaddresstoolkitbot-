import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

import config
from handlers import start_command, help_command, handle_message, handle_callback_query

# Configure systemic logging out output rules
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Instantiate standard telegram application state configuration
ptb_app = Application.builder().token(config.BOT_TOKEN).build()

# Connect functional route triggers to internal hooks
ptb_app.add_handler(CommandHandler("start", start_command))
ptb_app.add_handler(CommandHandler("help", help_command))
ptb_app.add_handler(CallbackQueryHandler(handle_callback_query))
ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Controls lifecycle events to guarantee graceful initialization and teardown sequences."""
    logger.info("Starting up FastAPI application instance...")
    
    # Initialize the PTB application loop requirements
    await ptb_app.initialize()
    await ptb_app.start()
    
    # Register webhooks automatically to the current environment configuration
    webhook_url = f"{config.WEBHOOK_URL.rstrip('/')}/webhook"
    logger.info(f"Registering production webhook target at: {webhook_url}")
    await ptb_app.bot.set_webhook(url=webhook_url)
    
    yield
    
    logger.info("Shutting down FastAPI context. Disposing loop handlers safely...")
    await ptb_app.stop()
    await ptb_app.shutdown()

# Instantiate runtime Web Server
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def health_check():
    """System health hook allowing Render to verify deployment status continuously."""
    return {"status": "operational", "bot_handle": "@Ipaddresstoolkitbot"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Processes asynchronous payload streams forwarded from Telegram API hubs."""
    try:
        payload = await request.json()
        update = Update.de_json(payload, ptb_app.bot)
        await ptb_app.process_update(update)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as error:
        logger.error(f"Error intercepted while processing webhook block update payload: {error}", exc_info=True)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

if __name__ == "__main__":
    import uvicorn
    # Bound to all interfaces on requested network configuration port matrix
    uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, log_level="info")
