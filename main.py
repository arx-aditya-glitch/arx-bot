import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

TOKEN = os.environ.get("TOKEN")
GROUP_LINK = "https://t.me/ArxAdityaff12"
GROUP_ID = -1003582740952
API_URL = "https://api-info-ff.vercel.app/info?uid={uid}&region=ind"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 JOIN GROUP", url=GROUP_LINK)],
        [InlineKeyboardButton("✅ DONE", callback_data="done")]
    ]
    await update.message.reply_text(
        "🔥 *WELCOME TO ARX INFO BOT* 🔥\n\n"
        "👋 PLEASE JOIN THE GROUP AND CLICK BELOW DONE ✅",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def done_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    try:
        member = await context.bot.get_chat_member(GROUP_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            await query.answer("Welcome!")
            await query.message.reply_text(
                "✅ *YOU ARE JOINED THE SUCCESSFULLY* ✅\n\n"
                "*USE THIS ARX INFO BOT SEND*\n\n"
                "`/arxinfo12 UID`\n"
                "`/arxget12 UID`\n"
                "`/arx12 UID`\n\n"
                "Example: `/arxinfo12 2530017529`",
                parse_mode="Markdown"
            )
        else:
            await query.answer("Please Join Group First!", show_alert=True)
    except:
        await query.message.reply_text("❌ Please Make Bot Admin In Group!")

async def info_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Example: `/arxinfo12 2530017529`", parse_mode="Markdown")
        return
    uid = context.args[0]
    await update.message.reply_text(f"🔍 Fetching Info For `{uid}`... Please Wait", parse_mode="Markdown")
    try:
        res = requests.get(API_URL.format(uid=uid), timeout=20).json()
        data = res.get("data", res)
        basic = data.get("basicInfo", {})
        profile = data.get("profileInfo", {})
        guild = data.get("guildInfo", {})
        text = (
            f"*Player Information:*\n"
            f"┌ *Basic Information:*\n"
            f"├─ Name: {basic.get('nickname', 'Not Found')}\n"
            f"├─ Uid: {uid}\n"
            f"├─ Region: {basic.get('region', 'IND')}\n"
            f"├─ Likes: {basic.get('liked', 'Not Found')}\n"
            f"├─ Level: {basic.get('level', 'Not Found')}\n"
            f"└─ Signature: {profile.get('signature', 'Not Found')}\n\n"
            f"┌ *Guild Information:*\n"
            f"├─ Guild ID: {guild.get('id', 'Not Found')}\n"
            f"├─ Guild Name: {guild.get('name', 'Not Found')}\n"
            f"└─ Guild Level: {guild.get('level', 'Not Found')}\n\n"
            f"👑 *OWNER:* @ArxAdityaff"
        )
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error Aaya Bhai!\n`{e}`", parse_mode="Markdown")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(done_click, pattern="done"))
app.add_handler(CommandHandler("arxinfo12", info_cmd))
app.add_handler(CommandHandler("arxget12", info_cmd))
app.add_handler(CommandHandler("arx12", info_cmd))
app.run_polling()
