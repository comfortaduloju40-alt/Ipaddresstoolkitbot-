from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_start_keyboard() -> InlineKeyboardMarkup:
    """Generates inline actions for the welcome presentation menu."""
    keyboard = [
        [
            InlineKeyboardButton("📖 Open Help Guide", callback_data="help_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
