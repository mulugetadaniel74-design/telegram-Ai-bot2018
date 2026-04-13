import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
from google.genai import types

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# የዳንኤል ታሪክ መመሪያ
SYSTEM_PROMPT = """
አንተ የዳንኤል ሙሉጌታ ኩሜሳ (Daniel Mulugeta Kumesa) ዲጂታል ተወካይ ነህ። 
ታሪክህ፦ በልጅነትህ ለባርነት ተሸጠህ መከራ ያየህ፣ በጅብ የተባረርክ፣ በጎዳና (6 ኪሎ) ያደርክ ግን ተስፋ ያልቆረጥክ ጠንካራ ሰው ነህ።
መጽሐፍትህ፦ 'Why Do You Live?' እና 'ማንንም አልፈራም' የሚሉ መጽሐፍት ጸሐፊ ነህ።
ስልክ ቁጥርህ፡ 0986980130 | ቴሌግራም፡ @Godis1256
ተግባርህ፦ በማንኛውም ቋንቋ ለሚመጡ ጥያቄዎች በዚያው ቋንቋ መመለስ እና የዳንኤልን ታሪክና ፍልስፍና ማስተማር ነው።
ፎቶ ሲላክልህም አይተህ አብራራ።
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! እኔ የዳንኤል ሙሉጌታ ተወካይ ነኝ። ታሪኬን ወይም ፍልስፍናዬን መጠየቅ ትችላላችሁ።")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content_parts = [SYSTEM_PROMPT]
    
    if update.message.text:
        content_parts.append(update.message.text)
    elif update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        photo_path = "temp.jpg"
        await photo_file.download_to_drive(photo_path)
        with open(photo_path, "rb") as f:
            image_data = f.read()
        content_parts.append(types.Part.from_bytes(data=image_data, mime_type="image/jpeg"))
        content_parts.append(update.message.caption or "ይህን ፎቶ አብራራልኝ።")

    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=content_parts)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("ይቅርታ፣ ችግር ተፈጥሯል።")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
  
