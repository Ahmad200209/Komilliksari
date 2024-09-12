from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
from datetime import datetime, time
from hijri_converter import convert
import pytz
from telegram import Update
from PIL import Image,ImageFont,ImageDraw
import os

tir = False
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Assalomu alaykum va rahmatullohi va baralatuh {update.effective_user.first_name}')
sanoq = 5
async def rasmlar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global tir 
    tir = True
    await update.message.reply_text('rasm yuborishingiz mumkin')
async def salomlashuv(context: ContextTypes.DEFAULT_TYPE) -> None:
    rasmlar=os.listdir("rasmlar")
    global sanoq
    sanoq += 1
    hijri_months = [
    "Muharram", "Safar", "Rabi'ul-avval", "Rabi'ul-akhir",
    "Jumada al-awwal", "Jumada al-akhir", "Rajab", "Sha'ban",
    "Ramazon", "Shavval", "Zul-Qi'dah", "Zul-Hijjah"
    ]
    hafta_kunlari = {
        'Monday': 'Dushanba',
        'Tuesday': 'Seshanba',
        'Wednesday': 'Chorshanba',
        'Thursday': 'Payshanba',
        'Friday': 'Juma',
        'Saturday': 'Shanba',
        'Sunday': 'Yakshanba'
    }
    
    oylar = {
        'January': 'Yanvar',
        'February': 'Fevral',
        'March': 'Mart',
        'April': 'Aprel',
        'May': 'May',
        'June': 'Iyun',
        'July': 'Iyul',
        'August': 'Avgust',
        'September': 'Sentabr',
        'October': 'Oktabr',
        'November': 'Noyabr',
        'December': 'Dekabr'
    }
    rasmlar_soni = len(rasmlar)
    hozir = datetime.now()
    hafta = hafta_kunlari[hozir.strftime('%A')]
    kun = hozir.day
    oy = oylar[hozir.strftime('%B')]
    yil = hozir.year
    gregorian_date = hozir
    link = '@Komillikuz'
    hijri_date = convert.Gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day).to_hijri()
    salomlash = f"Assalomu alaykum va rahmatullohi va barakatuh!\n<b>Bugun haftaning {hafta} kuni, {kun}-{oy} {yil}-yil.\nHijriy: {hijri_date.day} - {hijri_months[hijri_date.month - 1]} {hijri_date.year}-yil.</b>\n\nKuningiz xayrli o'tsin!\n\nKomillik sari kanali:\n<a href='https://t.me/Komillikuz'>📲 Telegram</a> | <a href='https://www.instagram.com/komillikuz'>📷 Instagram</a> | <a href='https://youtube.com/@komillikuz'>🔴 YouTube</a>"
    
    with open('rasmlar/ram{}.png'.format(sanoq), 'rb') as rasm:
        await context.bot.send_photo(link, photo=rasm, caption=salomlash, parse_mode='HTML')
    if sanoq > rasmlar_soni:
        sanoq = 0
    return sanoq
async def rasm_tutuvchi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    son = len(os.listdir("rasmlar"))
    son +=1
    global tir
    if tir:
        if update.message.photo:
            photo_file_id = update.message.photo[-1].file_id
            file = await context.bot.get_file(photo_file_id)
            await file.download_to_drive('rasmlar\\ram{}.png'.format(son))
            await update.message.reply_text("Rasm muvaffaqiyatli yuklab olindi!")
            is_active = False
        else:
            await update.message.reply_text('rasm yubormadingiz iltimos rasm yuboring')
    else:
        await update.message.reply_text('rasm yuborishingiz mumkin')




app = ApplicationBuilder().token("7424736107:AAFdMjo0IR8hY9Nk-WIX5gko-dp9KNMsYMw").build()
tashkent_tz = pytz.timezone('Asia/Tashkent')
target_time1 = tashkent_tz.localize(datetime.combine(datetime.today(), time(hour=6, minute=5)))
jon = app.job_queue
jon.run_daily(salomlashuv, target_time1)


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rasm", rasmlar))
app.add_handler(MessageHandler(filters.PHOTO, rasm_tutuvchi))

app.run_polling()
