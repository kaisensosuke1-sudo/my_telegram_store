import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import random
import time

# ═══════════════════════════════════════════
#             الإعدادات والمعلومات
# ═══════════════════════════════════════════
TOKEN = '8237170809:AAEBc9FLHiFnRYwzKCXiCIwLgfNJXCph6-s'
ADMIN_ID = 5968344409
LOG_CHANNEL = "-1003760548477"  # وضعناها بين علامتي تنصيص لتفادي أي خطأ رقمي
REQUIRED_CHANNELS = ['@kaisenxmlandedits', '@MediaDownloaderchannel', '@kaisencommunity']

bot = telebot.TeleBot(TOKEN)
DB_FILE = 'bot_database.db'

# ═══════════════════════════════════════════
#             قاعدة البيانات (SQLite)
# ═══════════════════════════════════════════
def init_db():
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                points INTEGER DEFAULT 0,
                referrals INTEGER DEFAULT 0,
                lang TEXT DEFAULT 'ar',
                last_spin REAL DEFAULT 0,
                referrer_id INTEGER DEFAULT NULL
            )
        ''')
        conn.commit()

def get_user(user_id):
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

def update_lang(user_id, lang):
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET lang = ? WHERE user_id = ?', (lang, user_id))
        conn.commit()

init_db()

# ═══════════════════════════════════════════
#             النصوص والترجمة
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
            "4. جرّب حظك يومياً في ماكينة الحظ التفاعلية!\n"
            "5. تابع إثباتات التسليم ومصداقية المتجر حصرياً عبر: @storecredibility ⭐️\n\n"
            "👇 *استخدم الأزرار أدناه للتنقل داخل البوت:* "
        ),
        'btn_link': "🔗 رابطي وإحالاتي",
        'btn_store': "🛒 متجر النجوم",
        'btn_wheel': "🎡 لفة الحظ",
        'btn_lang': "🌐 تغيير اللغة",
        'btn_contact': "📞 تواصل معي",
        'btn_social': "📱 حساباتي الرسمية",
        'btn_help': "❓ المساعدة والتعليمات",
        'btn_back': "↩️ رجوع",
        'btn_home': "🏠 القائمة الرئيسية",
        'link_msg': (
            "╭─── ◈ **نظام الإحالات** ◈ ───╮\n\n"
            "🔗 **رابط الدعوة الخاص بك:**\n"
            "`https://t.me/{}?start={}`\n\n"
            "👤 عدد إحالاتك: **{}**\n"
            "⭐️ رصيدك الحالي: **{} نقطة**\n\n"
            "💡 *انشر الرابط في المجموعات وأرسله لأصدقائك لجمع النقاط مجاناً!*"
        ),
        'store_msg': "🛒 **قائمة باقات متجر النجوم المتاحة:**\nاختر الباقة المناسبة لرصيدك للاستبدال الفوري:",
        'help_msg': (
            "╭─── ◈ **دليل المساعدة والأوامر** ◈ ───╮\n\n"
            "• `/start` - بدء وتشغيل البوت\n"
            "• `/store` - فتح متجر شراء النجوم\n"
            "• `/link` - رابط الإحالة ورصيد النقاط\n"
            "• `/wheel` - الدخول لماكينة الحظ اليومية\n"
            "• `/contact` - التواصل المباشر مع المطور\n"
            "• `/social` - جميع حسابات السوشيال ميديا\n"
            "• `/lang` - تغيير لغة البوت\n"
            "• `/help` - عرض هذا الدليل الإرشادي\n\n"
            "📩 لأي استفسار أو مشكلة تقنية، لا تتردد في استخدام زر التواصل."
        ),
        'not_subbed': "⚠️ **تنبيه:** يجب عليك الاشتراك في القنوات التالية لتفعيل البوت:",
        'sub_check': "🟢 تحققت من الاشتراك",
        'buy_success': "✅ تم استلام طلبك بنجاح! سيتم مراجعته وإرسال النجوم لك قريباً."
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
            "4. Spin the Lucky Reel every 24 hours!\n"
            "5. Verify live delivery proofs & winners on: @storecredibility ⭐️\n\n"
            "👇 *Select an option below to get started:* "
        ),
        'btn_link': "🔗 My Link & Points",
        'btn_store': "🛒 Stars Store",
        'btn_wheel': "🎡 Lucky Wheel",
        'btn_lang': "🌐 Language / لغة",
        'btn_contact': "📞 Contact Me",
        'btn_social': "📱 Official Social Media",
        'btn_help': "❓ Help & Guidelines",
        'btn_back': "↩️ Back",
        'btn_home': "🏠 Main Menu",
        'link_msg': (
            "╭─── ◈ **Referral System** ◈ ───╮\n\n"
            "🔗 **Your Invitation Link:**\n"
            "`https://t.me/{}?start={}`\n\n"
            "👤 Total Referrals: **{}**\n"
            "⭐️ Current Balance: **{} Points**\n\n"
            "💡 *Share your link to claim free points!*"
        ),
        'store_msg': "🛒 **Available Stars Packages:**\nChoose a package matching your points:",
        'help_msg': (
            "╭─── ◈ **Help & Bot Commands** ◈ ───╮\n\n"
            "• `/start` - Start the bot\n"
            "• `/store` - Open stars store\n"
            "• `/link` - Referral link & balance\n"
            "• `/wheel` - Spin daily reel\n"
            "• `/contact` - Direct developer contact\n"
            "• `/social` - All social media portals\n"
            "• `/lang` - Switch language\n"
            "• `/help` - View this help menu"
        ),
        'not_subbed': "⚠️ **Attention:** Please join our official channels to access the bot:",
        'sub_check': "🟢 Verify Subscription",
        'buy_success': "✅ Order received successfully! Stars will be delivered soon."
    }
}

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
    b_back = KeyboardButton(t['btn_back'])
    b_home = KeyboardButton(t['btn_home'])
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b5, b6)
    markup.add(b_help)
    markup.add(b_back, b_home)
    return markup

def navigation_keyboard(lang):
    t = TEXTS[lang]
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton(t['btn_back']), KeyboardButton(t['btn_home']))
    return markup

def store_navigation_buttons(lang):
    t = TEXTS[lang]
    return [
        InlineKeyboardButton(t['btn_back'], callback_data="nav_back"),
        InlineKeyboardButton(t['btn_home'], callback_data="nav_home")
    ]

def lang_inline_kb():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🇸🇦 العربية", callback_data="setlang_ar"),
        InlineKeyboardButton("🇬🇧 English", callback_data="setlang_en")
    )
    return markup

def check_sub(user_id):
    if user_id == ADMIN_ID:
        return True
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
        markup.add(InlineKeyboardButton(f"🟣 Channel ({clean_ch})", url=f"https://t.me/{clean_ch}"))
    markup.add(InlineKeyboardButton(TEXTS[lang]['sub_check'], callback_data="check_sub"))
    bot.send_message(user_id, TEXTS[lang]['not_subbed'], reply_markup=markup, parse_mode="Markdown")

# ═══════════════════════════════════════════════════════════════════
#             لوحة تحكم الأدمن
# ═══════════════════════════════════════════════════════════════════

@bot.message_handler(commands=['restwheel', 'restwheelall'])
def admin_reset_wheel(message):
    if message.from_user.id != ADMIN_ID: return
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET last_spin = 0')
        conn.commit()
        cursor.execute('SELECT user_id, lang FROM users')
        all_users = cursor.fetchall()
    total = len(all_users)
    bot.reply_to(message, f"⏳ تم تصفير العجلة لـ **{total}** حساب، جاري إرسال الإشعارات...", parse_mode="Markdown")
    for u_id, u_lang in all_users:
        if u_id == ADMIN_ID: continue
        try:
            lang = u_lang or 'ar'
            notice = "🎡 **مفاجأة سارة من الإدارة!** 🎁\n\nتم إعادة تعيين عجلة الحظ لك الآن! يمكنك الدخول وتجربة حظك للفوز بنجوم وتليجرام بريميوم مجاناً.\n\n👇 اضغط على زر `🎡 لفة الحظ` بالأسفل للتدوير فوراً!" if lang == 'ar' else "🎡 **Admin Lucky Surprise!** 🎁\n\nThe Lucky Wheel has been reset for you! Spin now to win Stars & Telegram Premium.\n\n👇 Hit the `🎡 Lucky Wheel` button below to spin!"
            bot.send_message(u_id, notice, parse_mode="Markdown")
            time.sleep(0.05)
        except: pass
    bot.send_message(ADMIN_ID, "✅ **اكتملت العملية بنجاح!**", parse_mode="Markdown")

@bot.message_handler(commands=['addme', 'addpointsme'])
def admin_add_me(message):
    if message.from_user.id != ADMIN_ID: return
    args = message.text.split()
    if len(args) < 2 or not args[1].lstrip('-').isdigit():
        bot.reply_to(message, "⚠️ اكتب: `/addme 100`", parse_mode="Markdown")
        return
    pts = int(args[1])
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET points = COALESCE(points, 0) + ? WHERE user_id = ?', (pts, ADMIN_ID))
        conn.commit()
    user = get_user(ADMIN_ID)
    bot.reply_to(message, f"✅ تم شحن رصيدك بـ **{pts}** نقطة!\n⭐️ رصيدك الحالي الآن: **{user[2]}** نقطة.", parse_mode="Markdown")

@bot.message_handler(commands=['addpointsall'])
def admin_add_points_all_cmd(message):
    if message.from_user.id != ADMIN_ID: return
    args = message.text.split()
    if len(args) < 2 or not args[1].lstrip('-').isdigit():
        bot.reply_to(message, "⚠️ اكتب: `/addpointsall 20`", parse_mode="Markdown")
        return
    pts = int(args[1])
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET points = COALESCE(points, 0) + ?', (pts,))
        conn.commit()
        cursor.execute('SELECT user_id, points, lang FROM users')
        all_users = cursor.fetchall()
    count = len(all_users)
    bot.reply_to(message, f"✅ **تم شحن النقاط لـ ({count} حساب)!**\n⏳ جاري إرسال الإشعارات الآن...", parse_mode="Markdown")
    for u_id, u_pts, u_lang in all_users:
        if u_id == ADMIN_ID: continue
        try:
            lang = u_lang or 'ar'
            notice = f"🎁 **مكافأة عامة من الإدارة!**\nتمت إضافة **{pts}** نقطة إلى حسابك بنجاح.\n⭐️ رصيدك الإجمالي الآن: **{u_pts}** نقطة." if lang == 'ar' else f"🎁 **Global Admin Reward!**\n**{pts}** points have been added to your balance.\n⭐️ Current Balance: **{u_pts}** points."
            bot.send_message(u_id, notice, parse_mode="Markdown")
            time.sleep(0.05)
        except: pass
    bot.send_message(ADMIN_ID, "✅ **اكتمل توزيع النقاط والإشعارات!**", parse_mode="Markdown")

@bot.message_handler(commands=['giftrandomly'])
def admin_gift_random(message):
    if message.from_user.id != ADMIN_ID: return
    args = message.text.split()
    if len(args) < 3 or not args[1].isdigit() or not args[2].isdigit():
        bot.reply_to(message, "⚠️ اكتب:\n`/giftrandomly <عدد_النقاط> <عدد_الأشخاص>`\nمثال: `/giftrandomly 50 3`", parse_mode="Markdown")
        return
    pts = int(args[1])
    num_winners = int(args[2])
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, username FROM users WHERE user_id != ?', (ADMIN_ID,))
        all_users = cursor.fetchall()
        if not all_users:
            bot.reply_to(message, "❌ لا يوجد مستخدمين آخرين في البوت لإجراء القرعة.")
            return
        selected = random.sample(all_users, min(num_winners, len(all_users)))
        for u_id, _ in selected:
            cursor.execute('UPDATE users SET points = COALESCE(points, 0) + ? WHERE user_id = ?', (pts, u_id))
        conn.commit()
    res = f"🎉 **تم اختيار {len(selected)} فائز وإعطاؤهم {pts} نقطة!**\n\n"
    for u_id, u_name in selected:
        tag = f"@{u_name}" if u_name and u_name != "Unknown" else "بدون يوزر"
        res += f"• `{u_id}` ({tag})\n"
        try: bot.send_message(u_id, f"🎁 **مبروك!** تم اختيارك عشوائياً وحصلت على **{pts}** نقطة هدية من الإدارة!", parse_mode="Markdown")
        except: pass
    bot.reply_to(message, res, parse_mode="Markdown")

@bot.message_handler(commands=['addpoints'])
def admin_add_points(message):
    if message.from_user.id != ADMIN_ID: return
    args = message.text.split()
    if len(args) == 3 and args[1].lower() == 'all' and args[2].lstrip('-').isdigit():
        pts = int(args[2])
        with sqlite3.connect(DB_FILE, timeout=30) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET points = COALESCE(points, 0) + ?', (pts,))
            conn.commit()
            cursor.execute('SELECT user_id, points, lang FROM users')
            all_users = cursor.fetchall()
        count = len(all_users)
        bot.reply_to(message, f"✅ تم شحن **{pts}** نقطة لكل المسجلين ({count} حساب) وتثبيتها بنجاح!", parse_mode="Markdown")
        for u_id, u_pts, u_lang in all_users:
            if u_id == ADMIN_ID: continue
            try:
                lang = u_lang or 'ar'
                bot.send_message(u_id, f"🎁 **مكافأة عامة من الإدارة!**\nتمت إضافة **{pts}** نقطة لحسابك.\nرصيدك الحالي: **{u_pts}** نقطة.", parse_mode="Markdown")
                time.sleep(0.05)
            except: pass
        return
    elif len(args) == 3 and args[1].isdigit() and args[2].lstrip('-').isdigit():
        t_id = int(args[1])
        pts = int(args[2])
        u = get_user(t_id)
        if not u:
            bot.reply_to(message, "❌ المستخدم غير مسجل.")
            return
        with sqlite3.connect(DB_FILE, timeout=30) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET points = COALESCE(points, 0) + ? WHERE user_id = ?', (pts, t_id))
            conn.commit()
        updated_u = get_user(t_id)
        bot.reply_to(message, f"✅ تم بنجاح إضافة **{pts}** نقطة للمستخدم `{t_id}`.\n⭐️ رصيده الإجمالي الآن أصبح: **{updated_u[2]}** نقطة.", parse_mode="Markdown")
        try: bot.send_message(t_id, f"🎁 **مكافأة من الإدارة!**\nتمت إضافة **{pts}** نقطة إلى حسابك.\nرصيدك الآن: **{updated_u[2]}** نقطة.", parse_mode="Markdown")
        except: pass
        return
    bot.reply_to(message, "⚠️ **طريقة الاستخدام:**\n• للجميع: `/addpoints all 20`\n• لشخص: `/addpoints <ID> 50`", parse_mode="Markdown")

# ═══════════════════════════════════════════
#             معالجة الأوامر العامة
# ═══════════════════════════════════════════
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    user = get_user(user_id)
    if not user:
        args = message.text.split()
        ref_id = None
        if len(args) > 1 and args[1].isdigit():
            c = int(args[1])
            if c != user_id: ref_id = c
        with sqlite3.connect(DB_FILE, timeout=30) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (user_id, username, referrer_id) VALUES (?, ?, ?)', (user_id, username, ref_id))
            conn.commit()
        bot.send_message(user_id, "✦ **اختر لغتك / Select your language** ✦", reply_markup=lang_inline_kb(), parse_mode="Markdown")
        return
    lang = user[4] or 'ar'
    if not check_sub(user_id):
        show_sub_gate(user_id, lang)
        return
    bot.send_message(user_id, TEXTS[lang]['welcome'], reply_markup=main_keyboard(lang), parse_mode="Markdown")

@bot.message_handler(commands=['link', 'store', 'wheel', 'lang', 'contact', 'social', 'help'])
def handle_slash(message):
    user = get_user(message.from_user.id)
    if not user: return handle_start(message)
    lang = user[4] or 'ar'
    cmd = message.text.split()[0].replace('/', '')
    if cmd == 'link': trigger_link(message.from_user.id, lang)
    elif cmd == 'store': trigger_store(message.from_user.id, lang)
    elif cmd == 'wheel': trigger_wheel(message.from_user.id, lang, message.from_user.username)
    elif cmd == 'lang': bot.send_message(message.from_user.id, "🌐 اختر لغة / Select Language:", reply_markup=lang_inline_kb())
    elif cmd == 'contact': trigger_contact(message.from_user.id)
    elif cmd == 'social': trigger_social(message.from_user.id)
    elif cmd == 'help': trigger_help(message.from_user.id, lang)

@bot.message_handler(func=lambda msg: True)
def handle_texts(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if not user: return handle_start(message)
    if not check_sub(user_id): return show_sub_gate(user_id, user[4] or 'ar')
    lang = user[4] or 'ar'
    txt = message.text
    if txt in [TEXTS['ar']['btn_back'], TEXTS['en']['btn_back'],
               TEXTS['ar']['btn_home'], TEXTS['en']['btn_home']]:
        show_main_menu(user_id, lang)
    elif txt in [TEXTS['ar']['btn_link'], TEXTS['en']['btn_link']]: trigger_link(user_id, lang)
    elif txt in [TEXTS['ar']['btn_store'], TEXTS['en']['btn_store']]: trigger_store(user_id, lang)
    elif txt in [TEXTS['ar']['btn_wheel'], TEXTS['en']['btn_wheel']]: trigger_wheel(user_id, lang, message.from_user.username)
    elif txt in [TEXTS['ar']['btn_lang'], TEXTS['en']['btn_lang']]: bot.send_message(user_id, "🌐 اختر لغة / Select Language:", reply_markup=lang_inline_kb())
    elif txt in [TEXTS['ar']['btn_contact'], TEXTS['en']['btn_contact']]: trigger_contact(user_id)
    elif txt in [TEXTS['ar']['btn_social'], TEXTS['en']['btn_social']]: trigger_social(user_id)
    elif txt in [TEXTS['ar']['btn_help'], TEXTS['en']['btn_help']]: trigger_help(user_id, lang)

# ═══════════════════════════════════════════
#             الوظائف التنفيذية
# ═══════════════════════════════════════════
def show_main_menu(user_id, lang):
    bot.send_message(
        user_id,
        TEXTS[lang]['welcome'],
        reply_markup=main_keyboard(lang),
        parse_mode="Markdown"
    )

def trigger_link(user_id, lang):
    user = get_user(user_id)
    bot_info = bot.get_me()
    msg = TEXTS[lang]['link_msg'].format(bot_info.username, user_id, user[3], user[2])
    bot.send_message(user_id, msg, reply_markup=navigation_keyboard(lang), parse_mode="Markdown")

def trigger_store(user_id, lang):
    markup = InlineKeyboardMarkup(row_width=1)
    packages = [
        ("🟢 ⭐ 15 Stars  ➔  5 Points", 5, 15),
        ("🟢 ⭐ 30 Stars  ➔  10 Points", 10, 30),
        ("🟢 ⭐ 70 Stars  ➔  20 Points", 20, 70),
        ("🟢 ⭐ 250 Stars ➔  50 Points", 50, 250),
        ("🟢 ⭐ 350 Stars ➔  100 Points", 100, 350)
    ]
    for label, pts, stars in packages:
        markup.add(InlineKeyboardButton(label, callback_data=f"buy_{pts}_{stars}"))
    markup.row(*store_navigation_buttons(lang))
    bot.send_message(user_id, TEXTS[lang]['store_msg'], reply_markup=markup, parse_mode="Markdown")

def trigger_wheel(user_id, lang, username):
    user = get_user(user_id)
    now = time.time()
    last_spin = user[5]

    if now - last_spin < 86400:
        hours_left = round((86400 - (now - last_spin)) / 3600, 1)
        wait_text = f"⏳ **عفواً! لقد استخدمت لفة الحظ اليومية.**\nيرجى الانتظار **{hours_left}** ساعة للمحاولة مجدداً." if lang == 'ar' else f"⏳ **Hold on! You already spun today.**\nPlease wait **{hours_left}** hours."
        bot.send_message(user_id, wait_text, reply_markup=navigation_keyboard(lang), parse_mode="Markdown")
        return

    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET last_spin = ? WHERE user_id = ?', (now, user_id))
        conn.commit()

    wheel_intro = (
        "╭━━━━━━━━━━━━━━━━━━━━╮\n"
        "      🎡 **عجلة الحظ اليومية**\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
        "        🔺\n"
        "   ⭐  |  💎  |  💵\n"
        "  ────🎡────\n"
        "   💔  |  ⭐  |  💎\n\n"
        "🎰 **جاري تدوير العجلة...**"
    ) if lang == 'ar' else (
        "╭━━━━━━━━━━━━━━━━━━━━╮\n"
        "      🎡 **DAILY LUCKY WHEEL**\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯\n\n"
        "        🔺\n"
        "   ⭐  |  💎  |  💵\n"
        "  ────🎡────\n"
        "   💔  |  ⭐  |  💎\n\n"
        "🎰 **Spinning the wheel...**"
    )
    bot.send_message(user_id, wheel_intro, reply_markup=navigation_keyboard(lang), parse_mode="Markdown")
    slot_dice = bot.send_dice(user_id, emoji='🎰')
    time.sleep(2.5)

    outcomes = ["lose", "15_stars", "premium", "2_dollars"]
    weights = [90000, 9000, 990, 10]
    result = random.choices(outcomes, weights=weights, k=1)[0]
    if slot_dice.dice.value == 64: result = "premium"

    if result == "lose":
        final_ui = "╭━━━━━━━━━━━━━━━━━━━━━━╮\n   💔  L U C K Y  R E E L  💔\n╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n😔 **حظ أوفر في المرة القادمة!**\nلم تتطابق الرموز اليوم، لكن العجلة تتجدد كل 24 ساعة. عد غداً وحاول من جديد! 🔥" if lang == 'ar' else "╭━━━━━━━━━━━━━━━━━━━━━━╮\n   💔  L U C K Y  R E E L  💔\n╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n😔 **Better luck next time!**\nSymbols didn't match today. Spin resets in 24 hours, try again tomorrow! 🔥"
    else:
        prize_title = "15 ⭐️ Stars" if result == "15_stars" else "Telegram Premium 💎" if result == "premium" else "2.00$ Cash 💵"
        final_ui = f"╭━━━━━━━━━━━━━━━━━━━━━━╮\n   🎉 ✦ J A C K P O T ! ✦ 🎉\n╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n🥳 **مـبـارك! لـقـد كـسـبـت الـجـائـزة!**\n╰┈➤ الجائزة: **{prize_title}**\n\n📩 تواصل مع الدعم عبر زر `📞 تواصل معي` لاستلام جائزتك فوراً!" if lang == 'ar' else f"╭━━━━━━━━━━━━━━━━━━━━━━╮\n   🎉 ✦ J A C K P O T ! ✦ 🎉\n╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n🥳 **CONGRATULATIONS! YOU WON!**\n╰┈➤ Prize: **{prize_title}**\n\n📩 Contact support via `📞 Contact Me` to claim your reward!"

        try:
            # السجل المطابق لشكل طلبك تماماً بدون ماركداون معقد
            user_tag = f"@{username}" if username else "بدون يوزر"
            log_text = (
                "🎡 فائز جديد في ماكينة الحظ!\n"
                f"👤 المستخدم: {user_tag}\n"
                f"🆔 المعرف (ID): {user_id}\n"
                f"🎁 الجائزة: {prize_title}\n"
                "🕒 النوع: ماكينة الحظ اليومية"
            )
            # إرسال بدون Parse_Mode لتجنب الأعطال
            bot.send_message(LOG_CHANNEL, log_text)
        except: pass

    bot.send_message(user_id, final_ui, reply_markup=navigation_keyboard(lang), parse_mode="Markdown")

def trigger_contact(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("💬 WhatsApp مباشر", url="https://wa.me/213674449294"),
        InlineKeyboardButton("✈️ Telegram: @gattal_brahim", url="https://t.me/gattal_brahim"),
        InlineKeyboardButton("👾 Discord: kaisen_xv", url="https://discord.com/users/kaisen_xv"),
        InlineKeyboardButton("📘 فيسبوك / Facebook", url="https://www.facebook.com/share/1cdngkRAyZ/")
    )
    bot.send_message(user_id, "╭─── ◈ **قنوات التواصل المباشر** ◈ ───╮\nاختر المنصة المناسبة:", reply_markup=markup, parse_mode="Markdown")

def trigger_social(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🌐 بوابة جميع حساباتي (All In One)", url="https://linktr.ee/kaisen_xv"),
        InlineKeyboardButton("🎵 تيك توك / TikTok (@kaisen_xv)", url="https://tiktok.com/@kaisen_xv"),
        InlineKeyboardButton("🏰 مجتمع ديسكورد / Discord Server", url="https://discord.gg/CUaqfBBcCM")
    )
    bot.send_message(user_id, "╭─── ◈ **حساباتي الرسمية** ◈ ───╮", reply_markup=markup, parse_mode="Markdown")

def trigger_help(user_id, lang):
    bot.send_message(user_id, TEXTS[lang]['help_msg'], reply_markup=navigation_keyboard(lang), parse_mode="Markdown")

# ═══════════════════════════════════════════
#             معالجة أزرار الـ Inline
# ═══════════════════════════════════════════
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    data = call.data

    if data.startswith("setlang_"):
        lang = data.split('_')[1]
        update_lang(user_id, lang)
        bot.answer_callback_query(call.id, "✅ Done!")
        u = get_user(user_id)
        if u and u[6]:
            ref = u[6]
            with sqlite3.connect(DB_FILE, timeout=30) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET points = COALESCE(points, 0) + 1, referrals = COALESCE(referrals, 0) + 1 WHERE user_id = ?', (ref,))
                cursor.execute('UPDATE users SET referrer_id = NULL WHERE user_id = ?', (user_id,))
                conn.commit()
            try: bot.send_message(ref, "🎉 دخل شخص جديد عبر رابطك وحصلت على **+1 نقطة**!", parse_mode="Markdown")
            except: pass
        if not check_sub(user_id): return show_sub_gate(user_id, lang)
        bot.send_message(user_id, TEXTS[lang]['welcome'], reply_markup=main_keyboard(lang), parse_mode="Markdown")

    elif data == "check_sub":
        u = get_user(user_id)
        lang = u[4] if u and u[4] else 'ar'
        if check_sub(user_id):
            bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح!")
            show_main_menu(user_id, lang)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في القنوات بعد!", show_alert=True)

    elif data in ["nav_back", "nav_home"]:
        u = get_user(user_id)
        lang = u[4] if u and u[4] else 'ar'
        bot.answer_callback_query(call.id)
        show_main_menu(user_id, lang)

    elif data.startswith("buy_"):
        _, pts, stars = data.split('_')
        pts = int(pts)
        u = get_user(user_id)
        lang = u[4] if u else 'ar'
        if u[2] >= pts:
            with sqlite3.connect(DB_FILE, timeout=30) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET points = points - ? WHERE user_id = ?', (pts, user_id))
                conn.commit()
            bot.answer_callback_query(call.id, TEXTS[lang]['buy_success'], show_alert=True)
            try:
                user_tag = f"@{call.from_user.username}" if call.from_user.username else "بدون يوزر"
                # استخدام HTML للظهور بنفس شكل Markdown القديم بدون أعطال الرموز
                log_text = (
                    "🛒 <b>طلب شراء جديد!</b>\n"
                    f"👤 المستخدم: {user_tag}\n"
                    f"📦 الباقة: <code>{stars} Stars</code>\n"
                    f"💰 النقاط المخصومة: <code>{pts}</code>"
                )
                bot.send_message(LOG_CHANNEL, log_text, parse_mode="HTML")
            except: pass
        else:
            bot.answer_callback_query(call.id, "❌ رصيد نقاطك غير كافٍ!", show_alert=True)

bot.infinity_polling()
