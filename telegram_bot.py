import telebot
import requests
import os # --- 1. تم استيراد مكتبة 'os' للتعامل مع متغيرات البيئة

# --- 2. قراءة مفاتيح الـ API من متغيرات البيئة بدلاً من كتابتها مباشرة ---
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
PIXABAY_API_KEY = os.environ.get('PIXABAY_API_KEY')

# التأكد من أن المفاتيح موجودة قبل تشغيل البوت
if not TELEGRAM_BOT_TOKEN or not PIXABAY_API_KEY:
    print("خطأ: لم يتم العثور على مفاتيح الـ API في متغيرات البيئة.")
    exit()

# --- 3. تعريف البوت باستخدام المفتاح الذي تم جلبه من البيئة ---
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    tag = f'<a href="tg://user?id={user_id}">{first_name}</a>'
    
    text = f'<b>• أهلاً بك عزيزي:</b> {tag}\n<b>• أرسل أي كلمة للبحث عن صور عالية الجودة.</b>'
    
    bot.send_message(
        message.chat.id, 
        text, 
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda message: True)
def main(message):
    wait_msg = bot.send_message(message.chat.id, "🖼️ لحظات... جاري البحث عن الصور")
    
    try:
        search_query = message.text
        
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={search_query}&image_type=photo&per_page=10"
        
        response = requests.get(url).json()
        
        images = response.get('hits', [])
        
        bot.delete_message(wait_msg.chat.id, wait_msg.message_id)

        if not images:
            bot.send_message(message.chat.id, f"❌ لم أجد أي صور باسم '{search_query}'، حاول البحث بكلمة أخرى.")
            return

        for image in images:
            image_url = image['largeImageURL']
            bot.send_photo(message.chat.id, image_url)
    
    except Exception as e:
        print(f"حدث خطأ: {e}")
        # قد يكون من الأفضل عدم حذف رسالة الانتظار إذا حدث خطأ، ليعرف المستخدم أن شيئًا ما قد حدث
        bot.send_message(message.chat.id, "حدث خطأ غير متوقع أثناء البحث. الرجاء المحاولة مرة أخرى.")

print("البوت يعمل الآن...")
bot.infinity_polling()
