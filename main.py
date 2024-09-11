from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime, time
from hijri_converter import convert
import pytz
import os


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def salomlashuv(context: ContextTypes.DEFAULT_TYPE) -> None:
    rasmlar = os.listdir("rasmlar\\")
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

    hozir = datetime.now()
    hafta = hafta_kunlari[hozir.strftime('%A')]
    kun = hozir.day
    oy = oylar[hozir.strftime('%B')]
    yil = hozir.year
    hijri_date = convert.Gregorian(hozir.year, hozir.month, hozir.day).to_hijri()

    salomlash = f"Assalomu alaykum va rahmatullohi va barakatuh!\nBugun haftaning {hafta} kuni, {kun}-{oy} {yil}-yil.\nHijriy: {hijri_date.day} - {hijri_months[hijri_date.month - 1]} {hijri_date.year}-yil.\n\nKuningiz xayrli o'tsin!\n\nKomillik sari kanali:\n<a href='https://t.me/Komillikuz'>📲 Telegram</a> | <a href='https://www.instagram.com/komillikuz'>📷 Instagram</a> | <a href='https://youtube.com/@komillikuz'>🔴 YouTube</a>"

    # `context.job.data` orqali sanoqni boshqaramiz
    sanoq = context.job.data.get('sanoq', 0)

    with open(f'rasmlar\\\\ram{sanoq}.png', 'rb') as rasm:
        await context.bot.send_photo(chat_id="@zx_lives", photo=rasm, caption=salomlash)

    # Rasmlar sonini tekshirish va sanoqni yangilash
    sanoq = (sanoq + 1) % len(rasmlar)
    context.job.data['sanoq'] = sanoq


app = ApplicationBuilder().token("7424736107:AAFdMjo0IR8hY9Nk-WIX5gko-dp9KNMsYMwEN").build()

# Vaqtni `run_daily` da to'g'ri o'rnatamiz
tashkent_tz = pytz.timezone('Asia/Tashkent')
target_time1 = time(hour=12, minute=50)
app.job_queue.run_daily(salomlashuv, time=target_time1, job_kwargs={'sanoq': 0})

app.add_handler(CommandHandler("start", start))
app.run_polling()
