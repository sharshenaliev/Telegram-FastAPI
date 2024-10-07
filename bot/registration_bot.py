from telegram import Update, ReplyKeyboardRemove
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler
from sqlalchemy import insert
from src.database import async_session_maker
from src.models import User
from src.config import TOKEN


BIO = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Напиши свое имя",
        reply_markup=ReplyKeyboardRemove(),
    )
    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    session = async_session_maker()
    user = insert(User).values(chat_id=update.effective_user.id,
                           username=update.effective_user.username,
                           name=update.message.text)
    await session.execute(user)
    await session.commit()
    await update.message.reply_text("Спасибо, регистрация завершена!")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Пока! Жду тебя снова.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    
    application.run_polling()
