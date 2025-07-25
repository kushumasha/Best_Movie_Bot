from telegram import InlineKeyboardButton, InlineKeyboardMarkup

languages = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
}

def get_language_keyboard():
    buttons = [
        [InlineKeyboardButton(name, callback_data=f"lang_{code}")]
        for code, name in languages.items()
    ]
    buttons.append([InlineKeyboardButton("Skip", callback_data="lang_skip")])
    return InlineKeyboardMarkup(buttons)
