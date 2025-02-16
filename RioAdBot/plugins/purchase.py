import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# ðŸ”¹ Your CryptoBot API Key
CRYPTOBOT_SECRET = "335393:AAdkGGk4TEr8Hna2sWFGDhveyhXe6nSUbM2"

# ðŸ”¹ Function to Create Invoice
def create_invoice(amount, currency, user_id):
    url = "https://pay.crypt.bot/api/createInvoice"
    headers = {"Crypto-Pay-API-Token": CRYPTOBOT_SECRET, "Content-Type": "application/json"}
    
    payload = {
        "asset": currency,  # e.g., "USDT", "BTC"
        "amount": amount,
        "description": "Your Plan Purchase",
        "hidden_message": "Thanks for your payment!",
        "paid_btn_name": "View Order",
        "paid_btn_url": "https://yourwebsite.com/order_status",
        "payload": str(user_id),
        "allow_comments": False,
        "allow_anonymous": False,
        "expires_in": 3600  # Invoice expires in 1 hour
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["result"]["pay_url"]

# ðŸ”¹ Purchase Command
def purchase(update: Update, context: CallbackContext) -> None:
    message = (
        "> **Choose Your Plan!!**\n\n"
        "â–  **Basic Plan**\n"
        "**â”” Accounts: 1**\n"
        "**â”” Intervals: 5 min**\n"
        "**â€¢|  Price: $40/week | $100/month |â€¢**\n\n"
        "**â–  Premium Plan**\n"
        "**â”” Accounts: 4**\n"
        "**â”” Intervals: 30 sec**\n"
        "**â€¢| Price: $250/week | $500/month |â€¢**\n\n"
        "**â–  Immortal Plan**\n"
        "**â”” Accounts: 10**\n"
        "**â”” Intervals: 60 sec**\n"
        "**â€¢| Price: $500/week | $1000/month |â€¢**\n\n"
        "---\n\n"
        "> Select a Plan to Continue Via Below Buttons!\n\n"
        "For support, contact @Boostadvert."
    )

    keyboard = [
        [InlineKeyboardButton("Basic Plan", callback_data='basic_plan')],
        [InlineKeyboardButton("Premium Plan", callback_data='premium_plan')],
        [InlineKeyboardButton("Immortal Plan", callback_data='immortal_plan')],
        [InlineKeyboardButton("Back", callback_data='back_to_start')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup, parse_mode="Markdown")

# ðŸ”¹ Handle Button Clicks
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id  # Get Telegram user ID

    if query.data == "basic_plan":
        keyboard = [
            [InlineKeyboardButton("Monthly ($100)", callback_data='basic_monthly')],
            [InlineKeyboardButton("Weekly ($40)", callback_data='basic_weekly')],
            [InlineKeyboardButton("Back", callback_data='purchase')],
        ]
        query.edit_message_text("Select duration:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "premium_plan":
        keyboard = [
            [InlineKeyboardButton("Monthly ($500)", callback_data='premium_monthly')],
            [InlineKeyboardButton("Weekly ($250)", callback_data='premium_weekly')],
            [InlineKeyboardButton("Back", callback_data='purchase')],
        ]
        query.edit_message_text("Select duration:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "immortal_plan":
        keyboard = [
            [InlineKeyboardButton("Monthly ($1000)", callback_data='immortal_monthly')],
            [InlineKeyboardButton("Weekly ($500)", callback_data='immortal_weekly')],
            [InlineKeyboardButton("Back", callback_data='purchase')],
        ]
        query.edit_message_text("Select duration:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data in ["basic_monthly", "basic_weekly", "premium_monthly", "premium_weekly", "immortal_monthly", "immortal_weekly"]:
        plan_prices = {
            "basic_monthly": 100, "basic_weekly": 40,
            "premium_monthly": 500, "premium_weekly": 250,
            "immortal_monthly": 1000, "immortal_weekly": 500
        }
        amount = plan_prices[query.data]
        pay_url = create_invoice(amount, "USDT", user_id)
        query.edit_message_text(f"âœ… Click below to pay:\n{pay_url}")

    elif query.data == "purchase":
        purchase(update, context)  # Go back to plan selection
