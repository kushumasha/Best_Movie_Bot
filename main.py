from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, CallbackContext, CallbackQueryHandler
)

from config import BOT_TOKEN
from language import get_language_keyboard, languages
from search import search_movie

user_lang = {}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🌐 Select your preferred language:",
        reply_markup=get_language_keyboard()
    )

async def handle_language(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("lang_"):
        lang_code = query.data.split("_")[1]
        user_lang[query.from_user.id] = lang_code
        await query.edit_message_text(f"✅ Language set to: {languages.get(lang_code, 'Unknown')}")
    else:
        await query.edit_message_text("✅ Skipped language selection.")

async def search_handler(update: Update, context: CallbackContext):
    query = update.message.text
    await update.message.reply_text("🔍 Searching...")

    results = await search_movie(query)
    if results:
        for msg in results[:3]:  # limit to 3 results
            await update.message.reply_document(msg.document.file_id)
    else:
        lang = user_lang.get(update.message.from_user.id, "en")
        msg = {
            "en": f"❌ Not found.\n🔎 Try searching on Google: https://www.google.com/search?q={query}",
            "hi": f"❌ फ़ाइल नहीं मिली।\n🔎 Google पर खोजें: https://www.google.com/search?q={query}",
            "bn": f"❌ ফাইল পাওয়া যায়নি।\n🔎 Google-এ খুঁজুন: https://www.google.com/search?q={query}",
            "ta": f"❌ கோப்பு கிடைக்கவில்லை.\n🔎 கூகிளில் தேடுங்கள்: https://www.google.com/search?q={query}",
            "te": f"❌ ఫైలు కనుగొనబడలేదు.\n🔎 గూగుల్‌లో వెతకండి: https://www.google.com/search?q={query}",
        }.get(lang, f"❌ Not found. Search: https://www.google.com/search?q={query}")

        await update.message.reply_text(msg)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_language, pattern="lang_.*|lang_skip"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
