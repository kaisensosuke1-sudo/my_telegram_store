import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import random
import time

# ═══════════════════════════════════════════
#             الإعدادات الأساسية
# ═══════════════════════════════════════════
TOKEN = '8962786006:AAHg6nPy0zlHbK7M2_ZkTLKMON8fjcf5E4M'   # ضع التوكن الخاص بك هنا
ADMIN_ID = 5968344409                             # ضع معرّفك الرقمي (ID الخاص بك) للتحكم بالنقاط
LOG_CHANNEL = '-1003760548477'                      # آيدي قناة الإثباتات الخاصة (يبدأ بـ -100)
REQUIRED_CHANNELS = ['@MediaDownloaderchannel', '@kaisencommunity', '@kaisenxmlandedits'] # قنوات الاشتراك الإجباري الثلاث

bot = telebot.TeleBot(TOKEN)
DB_FILE = 'bot_database.db'

# ═══════════════════════════════════════════
#             قاعدة البيانات (SQLite)
# ═══════════════════════════════════════════
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                points INTEGER DEFAULT 0,
                referrals INTEGER DEFAULT 0,
                lang TEXT DEFAULT NULL,
                last_spin REAL DEFAULT 0,
                referrer_id INTEGER DEFAULT NULL
            )
        ''')
        conn.commit()

def get_user(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

def update_lang(user_id, lang):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET lang = ? WHERE user_id = ?', (lang, user_id))
        conn.commit()

init_db()

# ═══════════════════════════════════════════
#             النصوص والزخرفة
# ═══════════════════════════════════════════
TEXTS = {
    'ar': {
        'welcome': (
            "╭━━━━━━━━━━━━━━━━━━━━━╮\n"
            "   ✦ مَـتـجَـر KAISEN لِـنـجُـوم تِـلـيـجـرَام ✦\n"
            "╰━━━━━━━━━━━━━━━━━━━━━╯\n\n"
            "مرحباً بك في المنصة الرسمية لربح وشراء نجوم تليجرام مجاناً!\n\n"
            "◈ **كيف يعمل البوت؟**\n"
            "1. شارك رابط الإحالة الخاص بك مع أصدقائك.\n"
            "2. كل صديق ينضم عبر رابطك يمنحك **+1 نقطة**.\n"
            "3. استبدل نقاطك مباشرة بنجوم تليجرام وهدايا فورية.\n"
            "4. جرّب حظك يومياً في عجلة الحظ!\n\n"
            "👇 *استخدم الأزرار أدناه للتنقل داخل البوت:* "
        ),
        'btn_link': "🔗 رابطي وإحالاتي",
        'btn_store': "🛒 متجر النجوم",
        'btn_wheel': "🎡 لفة الحظ",
        'btn_lang': "🌐 تغيير اللغة",
        'btn_contact': "📞 تواصل معي",
        'btn_social': "📱 حساباتي الرسمية",
        'btn_help': "❓ المساعدة والتعليمات",
        'link_msg': (
            "╭─── ◈ **نظام الإحالات** ◈ ───╮\n\n"
            "🔗 **رابط الدعوة الخاص بك:**\n"
            "`https://t.me/{}?start={}`\n\n"
            "👤 عدد إحالاتك: **{}**\n"
            "⭐️ رصيدك الحالي: **{} نقطة**\n\n"
            "💡 *انشر الرابط في المجموعات وأرسله لأصدقائك لجمع النقاط مجاناً!*"
        ),
        'store_msg': "🛒 **قائمة باقات متجر النجوم المتاحة:**\nاختر الباقة المناسبة لرصيدك للاستبدال الفوري:",
        'wheel_wait': "⏳ لقد استخدمت فرصتك اليومية! يمكنك التدوير مجدداً بعد **{} ساعة**.",
        'wheel_spin': "🎰 **جاري تدوير عجلة الحظ...**\n`[ ⭐️ | ❌ | 💎 | 💵 | ❌ ]`",
        'wheel_win': "🎉 **مبارك! لقد فزت بـ:**\n╰┈➤ **{}**",
        'wheel_lose': "😔 حظ أوفر! لم تربح شيئاً في هذه اللفة، عد غداً!",
        'help_msg': (
            "╭─── ◈ **دليل المساعدة والأوامر** ◈ ───╮\n\n"
            "• `/start` - إعادة تشغيل البوت\n"
            "• `/store` - فتح متجر شراء النجوم\n"
            "• `/link` - رابط الإحالة ورصيد النقاط\n"
            "• `/wheel` - الدخول لعجلة الحظ اليومية\n"
            "• `/contact` - التواصل المباشر مع المطور\n"
            "• `/social` - جميع حسابات السوشيال ميديا\n"
            "• `/lang` - تغيير لغة البوت\n"
            "• `/help` - عرض هذا الدليل الإرشادي\n\n"
            "📩 لأي استفسار أو مشكلة تقنية، لا تتردد في استخدام زر التواصل."
        ),
        'not_subbed': "⚠️ **تنبيه:** يجب عليك الاشتراك في القنوات التالية لتفعيل البوت:",
        'sub_check': "✅ تحقق من الاشتراك",
        'buy_success': "✅ تم استلام طلبك بنجاح! سيتم تحويل النجوم لك قريباً."
    },
    'en': {
        'welcome': (
            "╭━━━━━━━━━━━━━━━━━━━━━╮\n"
            "   ✦ KAISEN TELEGRAM STARS STORE ✦\n"
            "╰━━━━━━━━━━━━━━━━━━━━━╯\n\n"
            "Welcome to the premier store to claim Telegram Stars for free!\n\n"
            "◈ **How it works?**\n"
            "1. Share your personal invite link.\n"
            "2. Get **+1 Point** for every friend who joins.\n"
            "3. Redeem points for real Stars & valuable rewards.\n"
            "4. Spin the Lucky Wheel every 24 hours!\n\n"
            "👇 *Select an option below to get started:* "
        ),
        'btn_link': "🔗 My Link & Points",
        'btn_store': "🛒 Stars Store",
        'btn_wheel': "🎡 Lucky Wheel",
        'btn_lang': "🌐 Language / لغة",
        'btn_contact': "📞 Contact Me",
        'btn_social': "📱 Official Social Media",
        'btn_help': "❓ Help & Guidelines",
        'link_msg': (
            "╭─── ◈ **Referral System** ◈ ───╮\n\n"
            "🔗 **Your Invitation Link:**\n"
            "`https://t.me/{}?start={}`\n\n"
            "👤 Total Referrals: **{}**\n"
            "⭐️ Current Balance: **{} Points**\n\n"
            "💡 *Share your link to claim free points!*"
        ),
        'store_msg': "🛒 **Available Stars Packages:**\nChoose a package matching your points:",
        'wheel_wait': "⏳ You already spun today! Try again in **{} hours**.",
        'wheel_spin': "🎰 **Spinning the Lucky Reel...**\n`[ ⭐️ | ❌ | 💎 | 💵 | ❌ ]`",
        'wheel_win': "🎉 **Congratulations! You won:**\n╰┈➤ **{}**",
        'wheel_lose': "😔 Better luck next time! You won nothing today.",
        'help_msg': (
            "╭─── ◈ **Help & Bot Commands** ◈ ───╮\n\n"
            "• `/start` - Restart the bot\n"
            "• `/store` - Open stars store\n"
            "• `/link` - Referral link & balance\n"
            "• `/wheel` - Spin daily wheel\n"
            "• `/contact` - Direct developer contact\n"
            "• `/social` - All social media portals\n"
            "• `/lang` - Switch language\n"
            "• `/help` - View this help menu"
        ),
        'not_subbed': "⚠️ **Attention:** Please join our official channels to access the bot:",
        'sub_check': "✅ Verify Subscription",
        'buy_success': "✅ Order received successfully! Stars will be sent soon."
    }
}

# ═══════════════════════════════════════════
#             لوحات المفاتيح والأزرار
# ═══════════════════════════════════════════
def main_keyboard(lang):
    t = TEXTS[lang]
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    b1 = KeyboardButton(t['btn_link'])
    b2 = KeyboardButton(t['btn_store'])
    b3 = KeyboardButton(t['btn_wheel'])
    b4 = KeyboardButton(t['btn_lang'])
    b5 = KeyboardButton(t['btn_contact'])
    b6 = KeyboardButton(t['btn_social'])
    b_help = KeyboardButton(t['btn_help'])
    
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b5, b6)
    markup.add(b_help)
    return markup

def lang_inline_kb():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🇸🇦 العربية", callback_data="setlang_ar"),
        InlineKeyboardButton("🇬🇧 English", callback_data="setlang_en")
    )
    return markup

# ═══════════════════════════════════════════
#             التحقق من الاشتراك الإجباري
# ═══════════════════════════════════════════
def check_sub(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']:
                return False
        except:
            pass
    return True

def show_sub_gate(user_id, lang):
    markup = InlineKeyboardMarkup()
    for ch in REQUIRED_CHANNELS:
        clean_ch = str(ch).replace('@', '')
        markup.add(InlineKeyboardButton(f"📢 Channel ({clean_ch})", url=f"https://t.me/{clean_ch}"))
    markup.add(InlineKeyboardButton(TEXTS[lang]['sub_check'], callback_data="check_sub"))
    bot.send_message(user_id, TEXTS[lang]['not_subbed'], reply_markup=markup, parse_mode="Markdown")

# ═══════════════════════════════════════════
#             لوحة تحكم الأدمن (النقاط)
# ═══════════════════════════════════════════
@bot.message_handler(commands=['addme'])
def admin_add_me(message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if len(args) != 2 or not args[1].lstrip('-').isdigit():
        bot.reply_to(message, "⚠️ **طريقة الاستخدام:**\n`/addme <عدد_النقاط>`\n\n*مثال:* `/addme 100`", parse_mode="Markdown")
        return

    pts = int(args[1])
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET points = points + ? WHERE user_id = ?', (pts, ADMIN_ID))
        conn.commit()

    bot.reply_to(message, f"✅ تم شحن رصيدك بـ **{pts}** نقطة بنجاح!")

@bot.message_handler(commands=['addpoints'])
def admin_add_points(message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if len(args) != 3 or not args[1].isdigit() or not args[2].lstrip('-').isdigit():
        bot.reply_to(
            message,
            "⚠️ **طريقة الاستخدام:**\n`/addpoints <user_id> <عدد_النقاط>`\n\n*مثال:* `/addpoints 987654321 50`",
            parse_mode="Markdown"
        )
        return

    target_id = int(args[1])
    pts = int(args[2])

    user = get_user(target_id)
    if not user:
        bot.reply_to(message, "❌ المستخدم غير موجود في قاعدة البيانات (لم يقم بتشغيل البوت مسبقاً).")
        return

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET points = points + ? WHERE user_id = ?', (pts, target_id))
        conn.commit()

    bot.reply_to(message, f"✅ تم بنجاح إضافة **{pts}** نقطة للمستخدم `{target_id}`.")

    try:
        user_lang = user[4] or 'ar'
        notice = f"🎁 **مكافأة من الإدارة!**\nتمت إضافة **{pts}** نقطة إلى حسابك." if user_lang == 'ar' else f"🎁 **Admin Reward!**\n**{pts}** points added to your balance."
        bot.send_message(target_id, notice, parse_mode="Markdown")
    except:
        pass

# ═══════════════════════════════════════════
#             معالجة الأوامر الرئيسية
# ═══════════════════════════════════════════
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    user = get_user(user_id)

    if not user:
        args = message.text.split()
        referrer_id = None
        if len(args) > 1 and args[1].isdigit():
            ref_candidate = int(args[1])
            if ref_candidate != user_id:
                referrer_id = ref_candidate

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (user_id, username, referrer_id) VALUES (?, ?, ?)',
                (user_id, username, referrer_id)
            )
            conn.commit()

        welcome_intro = (
            "✦ **مرحباً بك في بوت متجر Kaisen** ✦\n"
            "✦ **Welcome to Kaisen Store Bot** ✦\n\n"
            "يرجى تحديد لغتك المفضلة للمتابعة:\n"
            "Please select your preferred language:"
        )
        bot.send_message(user_id, welcome_intro, reply_markup=lang_inline_kb(), parse_mode="Markdown")
        return

    lang = user[4]
    if not lang:
        bot.send_message(user_id, "يرجى اختيار اللغة / Select Language:", reply_markup=lang_inline_kb())
        return

    if not check_sub(user_id):
        show_sub_gate(user_id, lang)
        return

    bot.send_message(user_id, TEXTS[lang]['welcome'], reply_markup=main_keyboard(lang), parse_mode="Markdown")

@bot.message_handler(commands=['link', 'store', 'wheel', 'lang', 'contact', 'social', 'help'])
def handle_slash_commands(message):
    user = get_user(message.from_user.id)
    if not user or not user[4]:
        return handle_start(message)
    
    cmd = message.text.split()[0].replace('/', '')
    lang = user[4]

    if cmd == 'link':
        trigger_link(message.from_user.id, lang)
    elif cmd == 'store':
        trigger_store(message.from_user.id, lang)
    elif cmd == 'wheel':
        trigger_wheel(message.from_user.id, lang, message.from_user.username)
    elif cmd == 'lang':
        bot.send_message(message.from_user.id, "🌐 اختر لغة / Select Language:", reply_markup=lang_inline_kb())
    elif cmd == 'contact':
        trigger_contact(message.from_user.id)
    elif cmd == 'social':
        trigger_social(message.from_user.id)
    elif cmd == 'help':
        trigger_help(message.from_user.id, lang)

# ═══════════════════════════════════════════
#             معالجة نصوص الأزرار
# ═══════════════════════════════════════════
@bot.message_handler(func=lambda msg: True)
def handle_messages(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if not user or not user[4]:
        return handle_start(message)

    if not check_sub(user_id):
        return show_sub_gate(user_id, user[4])

    lang = user[4]
    text = message.text

    if text in [TEXTS['ar']['btn_link'], TEXTS['en']['btn_link']]:
        trigger_link(user_id, lang)
    elif text in [TEXTS['ar']['btn_store'], TEXTS['en']['btn_store']]:
        trigger_store(user_id, lang)
    elif text in [TEXTS['ar']['btn_wheel'], TEXTS['en']['btn_wheel']]:
        trigger_wheel(user_id, lang, message.from_user.username)
    elif text in [TEXTS['ar']['btn_lang'], TEXTS['en']['btn_lang']]:
        bot.send_message(user_id, "🌐 اختر لغة / Select Language:", reply_markup=lang_inline_kb())
    elif text in [TEXTS['ar']['btn_contact'], TEXTS['en']['btn_contact']]:
        trigger_contact(user_id)
    elif text in [TEXTS['ar']['btn_social'], TEXTS['en']['btn_social']]:
        trigger_social(user_id)
    elif text in [TEXTS['ar']['btn_help'], TEXTS['en']['btn_help']]:
        trigger_help(user_id, lang)

# ═══════════════════════════════════════════
#             تنفيذ وظائف الأقسام
# ═══════════════════════════════════════════
def trigger_link(user_id, lang):
    user = get_user(user_id)
    bot_info = bot.get_me()
    msg = TEXTS[lang]['link_msg'].format(bot_info.username, user_id, user[3], user[2])
    bot.send_message(user_id, msg, parse_mode="Markdown")

def trigger_store(user_id, lang):
    markup = InlineKeyboardMarkup(row_width=1)
    packages = [
        ("⭐ 15 Stars  ➔  5 Points", 5, 15),
        ("⭐ 30 Stars  ➔  10 Points", 10, 30),
        ("⭐ 70 Stars  ➔  20 Points", 20, 70),
        ("⭐ 250 Stars ➔  50 Points", 50, 250),
        ("⭐ 350 Stars ➔  100 Points", 100, 350)
    ]
    for label, pts, stars in packages:
        markup.add(InlineKeyboardButton(label, callback_data=f"buy_{pts}_{stars}"))
    bot.send_message(user_id, TEXTS[lang]['store_msg'], reply_markup=markup, parse_mode="Markdown")

def trigger_wheel(user_id, lang, username):
    user = get_user(user_id)
    now = time.time()
    last_spin = user[5]

    if now - last_spin < 86400:
        hours_left = round((86400 - (now - last_spin)) / 3600, 1)
        bot.send_message(user_id, TEXTS[lang]['wheel_wait'].format(hours_left), parse_mode="Markdown")
        return

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET last_spin = ? WHERE user_id = ?', (now, user_id))
        conn.commit()

    spin_msg = bot.send_message(user_id, TEXTS[lang]['wheel_spin'], parse_mode="Markdown")
    time.sleep(1.5)

    # احتمالات الجوائز: خسارة 90%، 15 نجمة 9%، بريميوم 0.99%، 2 دولار 0.01%
    outcomes = ["lose", "15_stars", "premium", "2_dollars"]
    weights = [90000, 9000, 990, 10]
    result = random.choices(outcomes, weights=weights, k=1)[0]

    strip_display = {
        "lose": "🔴 [ ❌ | ❌ | ❌ ]",
        "15_stars": "✨ [ ⭐️ | ⭐️ | ⭐️ ]",
        "premium": "💎 [ 💎 | 💎 | 💎 ]",
        "2_dollars": "💵 [ 💰 | 💰 | 💰 ]"
    }

    bot.edit_message_text(f"{strip_display[result]}\n\n", chat_id=user_id, message_id=spin_msg.message_id)

    if result == "lose":
        bot.send_message(user_id, TEXTS[lang]['wheel_lose'])
    else:
        prize_title = "15 ⭐️ Stars" if result == "15_stars" else "Telegram Premium 💎" if result == "premium" else "2.00$ Cash 💵"
        bot.send_message(user_id, TEXTS[lang]['wheel_win'].format(prize_title), parse_mode="Markdown")
        try:
            bot.send_message(
                LOG_CHANNEL,
                f"🎡 **فائز جديد في عجلة الحظ!**\n"
                f"👤 المستخدم: @{username or user_id}\n"
                f"🎁 الجائزة: `{prize_title}`"
            )
        except:
            pass

def trigger_contact(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("💬 WhatsApp مباشر", url="https://wa.me/213674449294"),
        InlineKeyboardButton("✈️ Telegram: @gattal_brahim", url="https://t.me/gattal_brahim"),
        InlineKeyboardButton("👾 Discord: kaisen_xv", url="https://discord.com/users/kaisen_xv"),
        InlineKeyboardButton("📘 فيسبوك / Facebook", url="https://www.facebook.com/share/1cdngkRAyZ/")
    )
    bot.send_message(user_id, "╭─── ◈ **قنوات التواصل المباشر** ◈ ───╮\nاختر المنصة التي تناسبك:", reply_markup=markup, parse_mode="Markdown")

def trigger_social(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🌐 بوابة جميع حساباتي الرسمية (All In One)", url="https://linktr.ee/kaisen_xv"),
        InlineKeyboardButton("🎵 تيك توك / TikTok (@kaisen_xv)", url="https://tiktok.com/@kaisen_xv"),
        InlineKeyboardButton("🏰 مجتمع ديسكورد / Discord Server", url="https://discord.gg/CUaqfBBcCM")
    )
    bot.send_message(user_id, "╭─── ◈ **منصات التواصل الاجتماعي الرسمية** ◈ ───╮\nتابع كافة التحديثات والمشاريع عبر الروابط أدناه:", reply_markup=markup, parse_mode="Markdown")

def trigger_help(user_id, lang):
    bot.send_message(user_id, TEXTS[lang]['help_msg'], parse_mode="Markdown")

# ═══════════════════════════════════════════
#             معالجة أزرار الـ Inline
# ═══════════════════════════════════════════
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    data = call.data

    if data.startswith("setlang_"):
        chosen_lang = data.split('_')[1]
        update_lang(user_id, chosen_lang)
        bot.answer_callback_query(call.id, "✅ Done!")

        user = get_user(user_id)
        if user and user[6]:
            referrer = user[6]
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET points = points + 1, referrals = referrals + 1 WHERE user_id = ?', (referrer,))
                cursor.execute('UPDATE users SET referrer_id = NULL WHERE user_id = ?', (user_id,))
                conn.commit()
            try:
                bot.send_message(referrer, "🎉 دخل شخص جديد عبر رابطك وحصلت على **+1 نقطة**!")
            except:
                pass

        if not check_sub(user_id):
            return show_sub_gate(user_id, chosen_lang)

        bot.send_message(user_id, TEXTS[chosen_lang]['welcome'], reply_markup=main_keyboard(chosen_lang), parse_mode="Markdown")

    elif data == "check_sub":
        user = get_user(user_id)
        lang = user[4] if user and user[4] else 'ar'
        if check_sub(user_id):
            bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح!")
            bot.send_message(user_id, TEXTS[lang]['welcome'], reply_markup=main_keyboard(lang), parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في القنوات بعد!", show_alert=True)

    elif data.startswith("buy_"):
        _, pts, stars = data.split('_')
        pts = int(pts)
        user = get_user(user_id)
        lang = user[4] if user else 'ar'

        if user[2] >= pts:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET points = points - ? WHERE user_id = ?', (pts, user_id))
                conn.commit()

            bot.answer_callback_query(call.id, TEXTS[lang]['buy_success'], show_alert=True)
            try:
                bot.send_message(
                    LOG_CHANNEL,
                    f"🛒 **طلب شراء جديد!**\n"
                    f"👤 المستخدم: @{call.from_user.username or user_id}\n"
                    f"📦 الباقة: `{stars} Stars`\n"
                    f"💰 النقاط المخصومة: `{pts}`"
                )
            except:
                pass
        else:
            bot.answer_callback_query(call.id, "❌ رصيد نقاطك غير كافٍ!" if lang == 'ar' else "❌ Not enough points!", show_alert=True)

# تشغيل البوت
bot.infinity_polling()