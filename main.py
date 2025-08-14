import telebot
import requests

# --- 1. تعريف البوت وإضافة مفتاح الـ API الجديد ---
bot = telebot.TeleBot("8248975275:AAFh46KmTPe6pOA7h8m2i3aEEw3GVan8JmM")
PIXABAY_API_KEY = "51776008-108cfd18070566ac7a699ca6e"

@bot.message_handler(commands=['start'])
def start(message):
    # --- 2. تم حذف زر المصمم من هنا ---
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    tag = f'<a href="tg://user?id={user_id}">{first_name}</a>'
    
    # رسالة ترحيبية بدون أي أزرار خارجية
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
        # --- 3. البحث باستخدام API موقع Pixabay ---
        search_query = message.text
        
        # رابط الـ API مع إضافة المفتاح والكلمة البحثية
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={search_query}&image_type=photo&per_page=10"
        
        response = requests.get(url).json()
        
        # استخراج الصور من النتائج
        images = response.get('hits', [])
        
        bot.delete_message(wait_msg.chat.id, wait_msg.message_id)

        if not images:
            bot.send_message(message.chat.id, f"❌ لم أجد أي صور باسم '{search_query}'، حاول البحث بكلمة أخرى.")
            return

        # إرسال الصور التي تم العثور عليها
        for image in images:
            # استخراج رابط الصورة بجودة عالية
            image_url = image['largeImageURL']
            bot.send_photo(message.chat.id, image_url)
    
    except Exception as e:
        print(f"حدث خطأ: {e}")
        bot.delete_message(wait_msg.chat.id, wait_msg.message_id)
        bot.send_message(message.chat.id, "حدث خطأ غير متوقع أثناء البحث. الرجاء المحاولة مرة أخرى.")

print("البوت يعمل الآن...")
bot.infinity_polling()
