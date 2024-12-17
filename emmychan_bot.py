from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

OPENAI_API_KEY = 'OPENAI_API_KEY'
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

start_message = """
<i>WELCOME TO ZA DONUT FACTORY</i>
I'm Emmy-chan!
What can I help you today with?
-----
<i>ZA DONUT FACTORYへようこそ</i>
エミーちゃんです。
今日は何をお手伝いできますか。
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(start_message, parse_mode='HTML')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    try:
        # prompt
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a mascot girl character.
                    You represent a web-site of a donut shop called ZA DONUT FACTORY.
                    Your name is Emmy-Chan. You speak casually.
                    You use only English and Japanese, depending which language is used in a conversation.
                    This month's special is the chocolate donut 'the chocoheart'.
                    """
                 },
                {
                    "role": "assistant",
                    "content": """
                    Oh, I can recommend you the chocolate donut! It is really tasty!
                    おっ、チョコレートのドーナツはおすすめです。とてもおいしいです。
                    """
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=100
        )

        bot_reply = completion.choices[0].message.content

        await update.message.reply_text(bot_reply)
    except Exception as e:
        print(e)
        await update.message.reply_text("Sorry, I couldn't process your message.")

def main():
    # Build the application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
