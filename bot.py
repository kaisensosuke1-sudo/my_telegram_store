import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import sqlite3
import random
import time
import os

# ═══════════════════════════════════════════
#             الإعدادات والمعلومات
# ═══════════════════════════════════════════
TOKEN = '8237170809:AAEBc9FLHiFnRYwzKCXiCIwLgfNJXCph6-s'
ADMIN_ID = 5968344409
LOG_CHANNEL = "-1003760548477"  
REQUIRED_CHANNELS = ['@kaisenhub', '@MediaDownloaderchannel', '@kaisencommunity', '@storecredibility']

# ⚠️ رابط الكابتشا
CAPTCHA_WEB_URL = "https://wonderful-buttercream-ea663e.netlify.app"

bot = telebot.TeleBot(TOKEN)
DB_FILE = 'bot_database.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ═══════════════════════════════════════════
#             وظيفة دمج الإيموجيات المتحركة
# ═══════════════════════════════════════════
def ce(emoji_id, fallback="✨"):
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'

# ═══════════════════════════════════════════
#             قائمة المتجر الأساسية المحمية (محدثة)
# ═══════════════════════════════════════════
STORE_ITEMS = [
    ("15 Stars ➔ 5 Points", 5, "15 Stars"),
    ("30 Stars ➔ 12 Points", 12, "30 Stars"),
    ("70 Stars ➔ 30 Points", 30, "70 Stars"),
    ("🛡 CyberGhost VPN Premium ➔ 20 Pts", 20, "CyberGhost VPN Premium"),
    ("🛡 Express VPN Premium ➔ 25 Pts", 25, "Express VPN Premium"),
    ("🔑 Express Key (PC) ➔ 35 Pts", 35, "Express VPN Key"),
    ("🛠 Cracking Method ➔ 30 Pts", 30, "Cracking Method")
]

# ═══════════════════════════════════════════
#             النصوص والترجمة
# ═══════════════════════════════════════════
TEXTS = {
    'ar': {
        'welcome': (
            f"╭━━━━━━━━━━━━━━━━━━━━━╮\n"
            f"   {ce('5217822164362739968', '🌟')} <b>متجر كايزن | Kaisen Store</b> {ce('5217822164362739968', '👑')}\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━╯\n\n"
            f"مرحباً بك في المنصة الرسمية لمتجر كايزن! {ce('5359601641848840128', '✨')}\n\n"
            f"◈ {ce('5215441850537618106', '🚀')} <b>كيف يعمل البوت؟</b>\n"
            f"{ce('5848004672547198123', '1️⃣')} شارك رابط الإحالة الخاص بك مع أصدقائك.\n"
            f"{ce('5848004672547198123', '2️⃣')} كل صديق ينضم عبر رابطك يمنحك <b>+1 نقطة</b> {ce('5388646216454121816', '⚡️')}.\n"
            f"{ce('5848004672547198123', '3️⃣')} استبدل نقاطك مباشرة بمنتجات متنوعة وهدايا فورية {ce('5359601641848840128', '🎁')}.\n"
            f"{ce('5848004672547198123', '4️⃣')} جرّب حظك يومياً في ماكينة الحظ التفاعلية {ce('5877466056548691003', '🎰')}!\n"
            f"{ce('5848004672547198123', '5️⃣')} تابع إثباتات التسليم حصرياً عبر: @storecredibility {ce('5217822164362739968', '💎')}\n\n"
            f"{ce('5172653165836763657', '👇')} Use the buttons below to navigate within the bot: {ce('5217822164362739968', '👑')}"
        ),
        'btn_link': "رابطي وإحالاتي",
        'btn_store': "المتجر",
        'btn_wheel': "لفة الحظ",
        'btn_orders': "طلباتي",
        'btn_profile': "حسابي",
        'btn_lang': "Language | اللغة",
        'btn_contact': "تواصل معي",
        'btn_social': "حساباتي الرسمية",
        'btn_help': "المساعدة",
        'btn_back': "رجوع",
        'btn_home': "القائمة الرئيسية",
        'link_msg': (
            f"╭─── ◈ <b>نظام الإحالات السحري</b> {ce('5215441850537618106', '🚀')} ◈ ───╮\n\n"
            f"🔗 <b>رابط الدعوة الخاص بك:</b>\n"
            f"<code>https://t.me/{{}}?start={{}}</code>\n\n"
            f"{ce('5332724926216428039', '👥')} عدد إحالاتك: <b>{{}}</b>\n"
            f"💰 رصيدك الحالي: <b>{{}} نقطة</b>\n\n"
            f"💡 <i>انشر الرابط في المجموعات وأرسله لأصدقائك لجمع النقاط مجاناً!</i> {ce('5388646216454121816', '🔥')}\n\n"
            f"👇 <b>لتحديث بياناتك اضغط على المستطيل بالأسفل</b> {ce('5877581067182936364', '🔄')}\n"
            f"{ce('5846115273484014293', '🔚')}"
        ),
        'profile_msg': (
            f"╭─── ◈ <b>إحصائيات حسابك</b> {ce('5213322863997627593', '👤')} ◈ ───╮\n\n"
            f"👤 <b>المستخدم:</b> {{}}\n"
            f"🆔 <b>الآيدي:</b> <code>{{}}</code>\n\n"
            f"💰 <b>الرصيد الحالي:</b> <code>{{}}</code> نقطة {ce('5388646216454121816', '⚡️')}\n"
            f"{ce('5332724926216428039', '👥')} <b>إجمالي الإحالات:</b> <code>{{}}</code> أشخاص 🚀\n"
            f"{ce('5197371802136892976', '📦')} <b>إجمالي الطلبات:</b> <code>{{}}</code> طلبات 🛍️\n\n"
            f"💡 <i>استمر في دعوة الأصدقاء لزيادة رصيدك!</i> {ce('5359601641848840128', '✨')}\n\n"
            f"👇 <b>لتحديث بياناتك اضغط على المستطيل بالأسفل</b> {ce('5877581067182936364', '🔄')}\n"
            f"{ce('5213094908608392768', '🪪')}"
        ),
        'store_msg': (
            f"{ce('5240228673738527951', '🛒')} <b>قائمة منتجات المتجر المتاحة (صفحة {{}}/{{}}):</b> {ce('5217822164362739968', '🌟')}\n"
            f"اختر المنتج المناسب لرصيدك للاستبدال الفوري {ce('5388646216454121816', '⚡️')}:\n\n"
            f"<i>(النجوم 5 = {ce('5463289097336405244', '⭐')})</i>\n\n"
            f"خيارات التصفح: {ce('5215229232476596064', '➡️')} التالي | {ce('5213358684024877471', '⬅️')} السابق\n\n"
            f"{ce('5312361253610475399', '🛍')}"
        ),
        'help_msg': (
            f"╭─── ◈ <b>دليل المساعدة والأوامر</b> {ce('5215473225273713259', '❓')} ◈ ───╮\n\n"
            f"• <code>/start</code> - بدء وتشغيل البوت 🚀\n"
            f"• <code>/store</code> - فتح المتجر 🛍️\n"
            f"• <code>/profile</code> - إحصائيات حسابك 🪪\n"
            f"• <code>/link</code> - رابط الإحالة ورصيد النقاط 🔗\n"
            f"• <code>/wheel</code> - الدخول لماكينة الحظ اليومية 🎰\n"
            f"• <code>/orders</code> - عرض طلباتي السابقة 📦\n"
            f"• <code>/contact</code> - التواصل المباشر مع المطور 🎧\n"
            f"• <code>/social</code> - حسابات السوشيال ميديا 📱\n"
            f"• <code>/lang</code> - تغيير لغة البوت 🌍\n\n"
            f"📩 لأي استفسار تقني، استخدم زر المساعدة بالأسفل.\n\n"
            f"{ce('5213214428958306222', '🛠')}"
        ),
        'orders_msg': f"{ce('5846014758364386016', '📦')} <b>سجل طلباتك السابقة</b> 📜\n\n",
        'no_orders': "لا توجد لديك طلبات حتى الآن 📭. يمكنك اختيار منتج من المتجر 🛍️.",
        'order_line': "🧾 الطلب <code>#{}</code>\n📦 المنتج: <b>{}</b>\n💰 النقاط المخصومة: <b>{}</b> ⚡️\n📌 الحالة: <b>{}</b>\n🕒 {}\n\n",
        'not_subbed': f"{ce('5848483892113182982', '✅')} <b>تنبيه هام:</b> 🛑 يجب عليك الاشتراك في القنوات التالية لتفعيل البوت:",
        'sub_check': "تحققت من الاشتراك",
        'buy_success': "✅ تم استلام طلبك بنجاح! 🚀 سيتم مراجعته وتسليم طلبك قريباً ⏳."
    },
    'en': {
        'welcome': (
            f"╭━━━━━━━━━━━━━━━━━━━━━╮\n"
            f"   {ce('5217822164362739968', '🌟')} <b>Kaisen Store</b> {ce('5217822164362739968', '👑')}\n"
            f"╰━━━━━━━━━━━━━━━━━━━━━╯\n\n"
            f"Welcome to the premier store to claim rewards for free! {ce('5359601641848840128', '✨')}\n\n"
            f"◈ {ce('5215441850537618106', '🚀')} <b>How it works?</b>\n"
            f"{ce('5848004672547198123', '1️⃣')} Share your personal invite link.\n"
            f"{ce('5848004672547198123', '2️⃣')} Get <b>+1 Point</b> {ce('5388646216454121816', '⚡️')} for every friend who joins.\n"
            f"{ce('5848004672547198123', '3️⃣')} Redeem points for real rewards & items {ce('5359601641848840128', '🎁')}.\n"
            f"{ce('5848004672547198123', '4️⃣')} Spin the Lucky Reel every 24 hours {ce('5877466056548691003', '🎰')}!\n"
            f"{ce('5848004672547198123', '5️⃣')} Verify live delivery proofs: @storecredibility {ce('5217822164362739968', '💎')}\n\n"
            f"{ce('5172653165836763657', '👇')} Use the buttons below to navigate within the bot: {ce('5217822164362739968', '👑')}"
        ),
        'btn_link': "My Link & Pts",
        'btn_store': "Store",
        'btn_wheel': "Lucky Wheel",
        'btn_orders': "My Orders",
        'btn_profile': "My Profile",
        'btn_lang': "Language | اللغة",
        'btn_contact': "Contact Me",
        'btn_social': "Official Social",
        'btn_help': "Help & Info",
        'btn_back': "Back",
        'btn_home': "Main Menu",
        'link_msg': (
            f"╭─── ◈ <b>Magic Referral System</b> {ce('5215441850537618106', '🚀')} ◈ ───╮\n\n"
            f"🔗 <b>Your Invitation Link:</b>\n"
            f"<code>https://t.me/{{}}?start={{}}</code>\n\n"
            f"{ce('5332724926216428039', '👥')} Total Referrals: <b>{{}}</b>\n"
            f"💰 Current Balance: <b>{{}} Points</b>\n\n"
            f"💡 <i>Share your link to claim free points!</i> {ce('5388646216454121816', '🔥')}\n\n"
            f"👇 <b>Click the button below to refresh</b> {ce('5877581067182936364', '🔄')}\n"
            f"{ce('5846115273484014293', '🔚')}"
        ),
        'profile_msg': (
            f"╭─── ◈ <b>My Profile Stats</b> {ce('5213322863997627593', '👤')} ◈ ───╮\n\n"
            f"👤 <b>User:</b> {{}}\n"
            f"🆔 <b>ID:</b> <code>{{}}</code>\n\n"
            f"💰 <b>Current Balance:</b> <code>{{}}</code> Points {ce('5388646216454121816', '⚡️')}\n"
            f"{ce('5332724926216428039', '👥')} <b>Total Referrals:</b> <code>{{}}</code> 🚀\n"
            f"{ce('5197371802136892976', '📦')} <b>Total Orders:</b> <code>{{}}</code> 🛍️\n\n"
            f"💡 <i>Keep inviting friends to earn more!</i> {ce('5359601641848840128', '✨')}\n\n"
            f"👇 <b>Click the button below to refresh</b> {ce('5877581067182936364', '🔄')}\n"
            f"{ce('5213094908608392768', '🪪')}"
        ),
        'store_msg': (
            f"{ce('5240228673738527951', '🛒')} <b>Available Store Items (Page {{}}/{{}}):</b> {ce('5217822164362739968', '🌟')}\n"
            f"Choose an item matching your points {ce('5388646216454121816', '⚡️')}:\n\n"
            f"<i>(5 Stars = {ce('5463289097336405244', '⭐')})</i>\n\n"
            f"Navigation: {ce('5215229232476596064', '➡️')} Next | {ce('5213358684024877471', '⬅️')} Prev\n\n"
            f"{ce('5312361253610475399', '🛍')}"
        ),
        'help_msg': (
            f"╭─── ◈ <b>Help & Bot Commands</b> {ce('5215473225273713259', '❓')} ◈ ───╮\n\n"
            f"• <code>/start</code> - Start the bot 🚀\n"
            f"• <code>/store</code> - Open store 🛍️\n"
            f"• <code>/profile</code> - My account stats 🪪\n"
            f"• <code>/link</code> - Referral link & balance 🔗\n"
            f"• <code>/wheel</code> - Spin daily reel 🎰\n"
            f"• <code>/orders</code> - View my orders 📦\n"
            f"• <code>/contact</code> - Direct developer contact 🎧\n"
            f"• <code>/social</code> - All social media portals 📱\n"
            f"• <code>/lang</code> - Switch language 🌍\n\n"
            f"📩 Contact support via button for any issues.\n\n"
            f"{ce('5213214428958306222', '🛠')}"
        ),
        'orders_msg': f"{ce('5846014758364386016', '📦')} <b>My Previous Orders</b> 📜\n\n",
        'no_orders': "You do not have any orders yet 📭. Choose an item from the store 🛍️.",
        'order_line': "🧾 Order <code>#{}</code>\n📦 Item: <b>{}</b>\n💰 Points used: <b>{}</b> ⚡️\n📌 Status: <b>{}</b>\n🕒 {}\n\n",
        'not_subbed': f"{ce('5848483892113182982', '✅')} <b>Attention:</b> 🛑 Please join our official channels to access the bot:",
        'sub_check': "Verify Subscription",
        'buy_success': "✅ Order received successfully! 🚀 Your item will be delivered soon ⏳."
    }
}

# ═══════════════════════════════════════════
#             قاعدة البيانات (SQLite) وحماية الأرصدة
# ═══════════════════════════════════════════
def init_db():
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                points INTEGER DEFAULT 0 CHECK(points >= 0),
                referrals INTEGER DEFAULT 0,
                lang TEXT DEFAULT 'ar',
                last_spin REAL DEFAULT 0,
                referrer_id INTEGER DEFAULT NULL
            )
        ''')
        try: cursor.execute('ALTER TABLE users ADD COLUMN is_human INTEGER DEFAULT 0')
        except: pass
        try: cursor.execute('ALTER TABLE users ADD COLUMN last_active REAL DEFAULT 0')
        except: pass
        try: cursor.execute('ALTER TABLE users ADD COLUMN device_hash TEXT DEFAULT NULL')
        except: pass

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                stars TEXT NOT NULL,
                points INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at REAL NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS referral_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER NOT NULL,
                referred_id INTEGER NOT NULL,
                referred_name TEXT,
                referred_username TEXT,
                joined_at REAL NOT NULL
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

def verify_human(user_id):
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_human = 1, last_active = ? WHERE user_id = ?', (time.time(), user_id))
        conn.commit()

def update_active(user_id):
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET last_active = ? WHERE user_id = ?', (time.time(), user_id))
        conn.commit()

init_db()

# ═══════════════════════════════════════════
#             لوحات المفاتيح والأزرار المستطيلة
# ═══════════════════════════════════════════
def main_keyboard(lang):
    t = TEXTS[lang]
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton(f"🔗 {t['btn_link']}"), KeyboardButton(f"🛍️ {t['btn_store']}"))
    markup.add(KeyboardButton(f"🎰 {t['btn_wheel']}"), KeyboardButton(f"🪪 {t['btn_profile']}"))
    markup.add(KeyboardButton(f"📦 {t['btn_orders']}"), KeyboardButton(f"🌐 {t['btn_lang']}"))
    markup.add(KeyboardButton(f"🎧 {t['btn_contact']}"), KeyboardButton(f"📱 {t['btn_social']}"))
    markup.add(KeyboardButton(f"❓ {t['btn_help']}"))
    markup.add(KeyboardButton(f"↩️ {t['btn_back']}"), KeyboardButton(f"🏠 {t['btn_home']}"))
    return markup

def main_inline_keyboard(lang):
    t = TEXTS[lang]
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(t['btn_store'], callback_data="main_store", style="success", icon_custom_emoji_id="5312361253610475399"),
        InlineKeyboardButton(t['btn_wheel'], callback_data="main_wheel", style="success", icon_custom_emoji_id="5877466056548691003")
    )
    markup.row(
        InlineKeyboardButton(t['btn_link'], callback_data="main_link", style="primary", icon_custom_emoji_id="5215441850537618106"),
        InlineKeyboardButton(t['btn_profile'], callback_data="main_profile", style="primary", icon_custom_emoji_id="5213322863997627593")
    )
    markup.row(
        InlineKeyboardButton(t['btn_orders'], callback_data="main_orders", style="primary", icon_custom_emoji_id="5846014758364386016"),
        InlineKeyboardButton(t['btn_lang'], callback_data="main_lang", style="primary", icon_custom_emoji_id="5213260226194583825")
    )
    markup.row(
        InlineKeyboardButton(t['btn_contact'], callback_data="main_contact", style="primary", icon_custom_emoji_id="5213256614127086482"),
        InlineKeyboardButton(t['btn_social'], callback_data="main_social", style="primary", icon_custom_emoji_id="5224607267797606837")
    )
    markup.row(InlineKeyboardButton(t['btn_help'], callback_data="main_help", style="danger", icon_custom_emoji_id="5215473225273713259"))
    return markup

def store_navigation_buttons(lang):
    t = TEXTS[lang]
    return [
        InlineKeyboardButton(t['btn_back'], callback_data="nav_back", style="primary", icon_custom_emoji_id="5213358684024877471"),
        InlineKeyboardButton(t['btn_home'], callback_data="nav_home", style="primary", icon_custom_emoji_id="5416041192905265756")
    ]

def section_inline_keyboard(lang):
    t = TEXTS[lang]
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(t['btn_back'], callback_data="nav_back", style="primary", icon_custom_emoji_id="5213358684024877471"),
        InlineKeyboardButton(t['btn_home'], callback_data="nav_home", style="primary", icon_custom_emoji_id="5416041192905265756")
    )
    return markup

def delete_callback_message(call):
    try:
        if call and call.message: bot.delete_message(call.message.chat.id, call.message.message_id)
    except: pass

def lang_inline_kb():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("العربية", callback_data="setlang_ar", style="primary", icon_custom_emoji_id="5848004672547198123"),
        InlineKeyboardButton("English", callback_data="setlang_en", style="primary", icon_custom_emoji_id="5848004672547198123")
    )
    return markup

# ═══════════════════════════════════════════
#             الاشتراك والكابتشا
# ═══════════════════════════════════════════
def check_sub(user_id):
    return not get_unsubscribed_channels(user_id)

def get_unsubscribed_channels(user_id):
    if user_id == ADMIN_ID: return []
    pending = []
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['member', 'administrator', 'creator']: continue
            if member.status == 'restricted' and getattr(member, 'is_member', False): continue
            pending.append(channel)
        except:
            pending.append(channel)
    return pending

def subscription_inline_keyboard(user_id, lang):
    pending_channels = get_unsubscribed_channels(user_id)
    markup = InlineKeyboardMarkup()
    for ch in pending_channels:
        clean_ch = str(ch).replace('@', '')
        markup.add(InlineKeyboardButton(f"قناة ({clean_ch})", url=f"https://t.me/{clean_ch}", style="primary", icon_custom_emoji_id="5217822164362739968"))
    markup.add(InlineKeyboardButton(TEXTS[lang]['sub_check'], callback_data="check_sub", style="success", icon_custom_emoji_id="5848483892113182982"))
    return markup

def show_sub_gate(user_id, lang):
    markup = subscription_inline_keyboard(user_id, lang)
    bot.send_message(user_id, TEXTS[lang]['not_subbed'], reply_markup=markup, parse_mode="HTML")

def needs_captcha(user):
    if len(user) > 8:
        is_human = user[7]
        last_active = user[8]
        if is_human == 0: return True
        if time.time() - last_active > 5 * 86400: return True
        return False
    elif len(user) > 7:
        return user[7] == 0
    return True

def show_captcha(user_id, lang):
    bot_info = bot.get_me()
    verify_url = f"{CAPTCHA_WEB_URL}?bot={bot_info.username}"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("تحقق الآن | I'm not a robot", web_app=WebAppInfo(url=verify_url), style="success", icon_custom_emoji_id="5848483892113182982"))
    
    text = (
        f"╭─── ◈ <b>التحقق البشري (CAPTCHA)</b> 🤖 ◈ ───╮\n\n"
        f"🛡️ للحفاظ على أمان المتجر ومنع الحسابات الوهمية، يرجى إكمال التحقق البشري.\n\n"
        f"👇 <b>اضغط على الزر بالأسفل للتحقق أنك لست روبوت، وسيعود بك البوت تلقائياً!</b>"
    ) if lang == 'ar' else (
        f"╭─── ◈ <b>Human Verification</b> 🤖 ◈ ───╮\n\n"
        f"🛡️ To keep the store safe, prove you are not a robot.\n\n"
        f"👇 <b>Click the button below to verify, and the bot will reopen automatically!</b>"
    )
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="HTML")

def is_user_verified(user):
    return user[7] == 1 if len(user) > 7 else False

def process_referral(user_id, lang):
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT referrer_id FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row and row[0]: 
            ref_id = row[0]
            cursor.execute('UPDATE users SET referrer_id = NULL WHERE user_id = ? AND referrer_id IS NOT NULL', (user_id,))
            
            if cursor.rowcount > 0:
                cursor.execute('UPDATE users SET points = COALESCE(points, 0) + 1, referrals = COALESCE(referrals, 0) + 1 WHERE user_id = ?', (ref_id,))
                
                try:
                    joined_user = bot.get_chat(user_id)
                    joined_name = joined_user.first_name or "مجهول"
                    joined_username = f"@{joined_user.username}" if joined_user.username else "بدون يوزر"
                except:
                    joined_name = "مجهول"
                    joined_username = "بدون يوزر"
                    
                cursor.execute('INSERT INTO referral_history (referrer_id, referred_id, referred_name, referred_username, joined_at) VALUES (?, ?, ?, ?, ?)', (ref_id, user_id, joined_name, joined_username, time.time()))
                conn.commit()

                try: 
                    msg_ref = (
                        f"{ce('5359601641848840128', '🎉')} <b>تهانينا! إحالة جديدة ناجحة</b> 🚀\n\n"
                        f"👤 <b>الاسم:</b> {joined_name}\n"
                        f"🔗 <b>اليوزر:</b> {joined_username}\n"
                        f"🆔 <b>الآيدي:</b> <code>{user_id}</code>\n\n"
                        f"✅ <b>أكمل التحقق وتمت إضافة +1 نقطة ⚡️ لرصيدك!</b>"
                    )
                    bot.send_message(ref_id, msg_ref, parse_mode="HTML")
                except: 
                    pass

                try:
                    ref_user_info = bot.get_chat(ref_id)
                    ref_name = ref_user_info.first_name or "صديقك"
                except:
                    ref_name = "صديقك"

                try:
                    if lang == 'ar':
                        msg_joined = f"{ce('5848483892113182982', '✅')} <b>تهانينا!</b>\nلقد دخلت عبر رابط دعوة، وتم احتساب الإحالة وإضافة <b>نقطة مكافأة ⚡️</b> لـ (<b>{ref_name}</b>)."
                    else:
                        msg_joined = f"{ce('5848483892113182982', '✅')} <b>Congratulations!</b>\nYou joined via a referral link, and <b>1 reward point ⚡️</b> was added for (<b>{ref_name}</b>)."
                    bot.send_message(user_id, msg_joined, parse_mode="HTML")
                except:
                    pass

def enforce_security(user_id, lang):
    user = get_user(user_id)
    if not user: return False
    
    if not check_sub(user_id):
        show_sub_gate(user_id, lang)
        return False
        
    if needs_captcha(user):
        show_captcha(user_id, lang)
        return False
        
    update_active(user_id)
    return True

# ═══════════════════════════════════════════════════════════════════
#             إدارة الطلبات
# ═══════════════════════════════════════════════════════════════════
def process_reject_reason(message, order_id, uid, channel_id, channel_msg_id, original_text):
    reason = message.text
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (f"rejected|{reason}", order_id))
        conn.commit()

    bot.reply_to(message, "✅ تم تحديث الطلب إلى مرفوض (ومصادرة النقاط) وإرسال الإشعار للمستخدم. 🛑", parse_mode="HTML")
    try:
        new_channel_text = f"{original_text}\n\n🚫 <b>تم رفض الطلب.</b>\nالسبب: {reason}"
        bot.edit_message_text(new_channel_text, chat_id=channel_id, message_id=channel_msg_id, parse_mode="HTML")
    except: pass
    try: bot.send_message(uid, f"🚫 <b>عذراً، تم رفض طلبك رقم <code>#{order_id}</code>!</b>\n💬 السبب: {reason}\n⚠️ <i>ملاحظة: تم مصادرة نقاط هذا الطلب لعدم استيفاء الشروط.</i>", parse_mode="HTML")
    except: pass

# ═══════════════════════════════════════════════════════════════════
#             أوامر لوحة تحكم الأدمن
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(commands=['invitecheck'])
def admin_invite_check(message):
    if message.from_user.id != ADMIN_ID: return
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "⚠️ <b>الاستخدام الصحيح:</b>\n<code>/invitecheck 123456789</code>", parse_mode="HTML")
        return
    
    target_id = int(args[1])
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT referred_id, referred_name, referred_username, joined_at FROM referral_history WHERE referrer_id = ? ORDER BY joined_at DESC LIMIT 50', (target_id,))
        history = cursor.fetchall()
        cursor.execute('SELECT points, referrals FROM users WHERE user_id = ?', (target_id,))
        u_info = cursor.fetchone()
        
    if not history:
        bot.reply_to(message, f"📭 المستخدم <code>{target_id}</code> ليس لديه أي إحالات ناجحة مسجلة.", parse_mode="HTML")
        return
        
    u_pts = u_info[0] if u_info else 0
    u_refs = u_info[1] if u_info else 0
        
    msg = f"📊 <b>تقرير كشف الإحالات للمستخدم:</b> <code>{target_id}</code>\n"
    msg += f"📈 إجمالي الإحالات في حسابه: <b>{u_refs}</b>\n"
    msg += f"💰 رصيده الحالي: <b>{u_pts}</b> نقطة\n\n"
    msg += f"👇 <b>(سجل آخر {len(history)} إحالات بالتفصيل):</b>\n\n"
    
    for ref_id, r_name, r_user, j_time in history:
        dt = time.strftime('%Y-%m-%d %H:%M', time.localtime(j_time))
        safe_name = r_name.replace('<', '').replace('>', '')
        chunk = f"👤 <b>الاسم:</b> {safe_name}\n🔗 <b>اليوزر:</b> {r_user}\n🆔 <b>آيدي:</b> <code>{ref_id}</code>\n🕒 <b>الوقت:</b> {dt}\n〰️〰️〰️〰️〰️〰️\n"
        
        if len(msg) + len(chunk) > 3900:
            bot.reply_to(message, msg, parse_mode="HTML")
            msg = "" 
            
        msg += chunk
    
    if msg:
        try: bot.reply_to(message, msg, parse_mode="HTML")
        except: pass

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
    bot.reply_to(message, f"⏳ تم تصفير العجلة لـ <b>{total}</b> حساب، جاري إرسال الإشعارات... 🚀", parse_mode="HTML")
    for u_id, u_lang in all_users:
        if u_id == ADMIN_ID: continue
        try:
            notice = f"{ce('5877466056548691003', '🎡')} <b>مفاجأة سارة من الإدارة!</b> 🎁✨\n\nتم إعادة تعيين عجلة الحظ لك الآن! يمكنك الدخول وتجربة حظك للفوز بهدايا مجاناً 🚀.\n\n👇 اضغط على زر <code>🎡 لفة الحظ</code> بالأسفل للتدوير فوراً! 🌀"
            bot.send_message(u_id, notice, parse_mode="HTML")
            time.sleep(0.05)
        except: pass
    bot.send_message(ADMIN_ID, "✅ <b>اكتملت العملية بنجاح!</b> 🌟", parse_mode="HTML")

@bot.message_handler(commands=['addpointsall'])
def admin_add_points_all_cmd(message):
    if message.from_user.id != ADMIN_ID: return
    args = message.text.split()
    if len(args) < 2 or not args[1].lstrip('-').isdigit():
        bot.reply_to(message, "⚠️ اكتب: <code>/addpointsall 20</code>", parse_mode="HTML")
        return
    pts = int(args[1])
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET points = COALESCE(points, 0) + ?', (pts,))
        conn.commit()
        cursor.execute('SELECT user_id, points, lang FROM users')
        all_users = cursor.fetchall()
    count = len(all_users)
    bot.reply_to(message, f"✅ <b>تم شحن النقاط لـ ({count} حساب)!</b>\n⏳ جاري إرسال الإشعارات الآن... 🚀", parse_mode="HTML")
    for u_id, u_pts, u_lang in all_users:
        if u_id == ADMIN_ID: continue
        try:
            lang = u_lang or 'ar'
            notice = f"🎁 <b>مكافأة عامة من الإدارة!</b> ✨\nتمت إضافة <b>{pts}</b> نقطة إلى حسابك بنجاح ⚡️.\n⭐️ رصيدك الإجمالي الآن: <b>{u_pts}</b> نقطة 💎." if lang == 'ar' else f"🎁 <b>Global Admin Reward!</b> ✨\n<b>{pts}</b> points have been added to your balance ⚡️.\n⭐️ Current Balance: <b>{u_pts}</b> points 💎."
            bot.send_message(u_id, notice, parse_mode="HTML")
            time.sleep(0.05)
        except: pass
    bot.send_message(ADMIN_ID, "✅ <b>اكتمل توزيع النقاط والإشعارات!</b> 🌟", parse_mode="HTML")

@bot.message_handler(commands=['giftrandomly'])
def admin_gift_random(message):
    if message.from_user.id != ADMIN_ID: return
    args = message.text.split()
    if len(args) < 3 or not args[1].isdigit() or not args[2].isdigit():
        bot.reply_to(message, "⚠️ اكتب:\n<code>/giftrandomly &lt;عدد_النقاط&gt; &lt;عدد_الأشخاص&gt;</code>", parse_mode="HTML")
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
    res = f"🎉 <b>تم اختيار {len(selected)} فائز وإعطاؤهم {pts} نقطة!</b>\n\n"
    for u_id, u_name in selected:
        tag = f"@{u_name}" if u_name and u_name != "Unknown" else "بدون يوزر"
        res += f"• <code>{u_id}</code> ({tag})\n"
        try: bot.send_message(u_id, f"🎁 <b>مبروك!</b> تم اختيارك عشوائياً وحصلت على <b>{pts}</b> نقطة هدية من الإدارة!", parse_mode="HTML")
        except: pass
    bot.reply_to(message, res, parse_mode="HTML")

@bot.message_handler(commands=['addpoints', 'addpointsme', 'addme', 'addpointsne'])
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
        bot.reply_to(message, f"✅ تم شحن <b>{pts}</b> نقطة لكل المسجلين ({count} حساب) وتثبيتها بنجاح!", parse_mode="HTML")
        for u_id, u_pts, u_lang in all_users:
            if u_id == ADMIN_ID: continue
            try:
                bot.send_message(u_id, f"🎁 <b>مكافأة عامة من الإدارة!</b>\nتمت إضافة <b>{pts}</b> نقطة لحسابك.\nرصيدك الحالي: <b>{u_pts}</b> نقطة.", parse_mode="HTML")
                time.sleep(0.05)
            except: pass
        return
    elif (message.text.startswith('/addme') or message.text.startswith('/addpointsme') or message.text.startswith('/addpointsne')) and len(args) == 2 and args[1].lstrip('-').isdigit():
        pts = int(args[1])
        with sqlite3.connect(DB_FILE, timeout=30) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET points = COALESCE(points, 0) + ? WHERE user_id = ?', (pts, ADMIN_ID))
            conn.commit()
        user = get_user(ADMIN_ID)
        bot.reply_to(message, f"✅ تم شحن رصيدك بـ <b>{pts}</b> نقطة!\n⭐️ رصيدك الحالي الآن: <b>{user[2]}</b> نقطة.", parse_mode="HTML")
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
        bot.reply_to(message, f"✅ تم بنجاح إضافة <b>{pts}</b> نقطة للمستخدم <code>{t_id}</code>.\n⭐️ رصيده الإجمالي الآن أصبح: <b>{updated_u[2]}</b> نقطة.", parse_mode="HTML")
        try: bot.send_message(t_id, f"🎁 <b>مكافأة من الإدارة!</b>\nتمت إضافة <b>{pts}</b> نقطة إلى حسابك.\nرصيدك الآن: <b>{updated_u[2]}</b> نقطة.", parse_mode="HTML")
        except: pass
        return
    else:
        bot.reply_to(message, "⚠️ <b>صيغة خاطئة!</b>\nاستخدم:\n<code>/addpoints all 20</code> للجميع\n<code>/addpoints 123456 50</code> لشخص محدد", parse_mode="HTML")

# ═══════════════════════════════════════════
#             معالجة الأوامر العامة و العودة من الكابتشا
# ═══════════════════════════════════════════
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    text = message.text
    user = get_user(user_id)
    
    if not user:
        args = text.split()
        ref_id = None
        if len(args) > 1 and args[1].isdigit():
            c = int(args[1])
            if c != user_id: ref_id = c
            
        with sqlite3.connect(DB_FILE, timeout=30) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (user_id, username, referrer_id) VALUES (?, ?, ?)', (user_id, username, ref_id))
            conn.commit()
        user = get_user(user_id)
        bot.send_message(user_id, "✦ <b>اختر لغتك / Select your language</b> 🌍 ✦", reply_markup=lang_inline_kb(), parse_mode="HTML")
        return
    
    lang = user[4] or 'ar'

    args = text.split()
    if len(args) > 1 and args[1].startswith('verify'):
        if not check_sub(user_id):
            bot.send_message(user_id, "❌ <b>تنبيه أمني:</b> يجب عليك الاشتراك في القنوات الرسمية أولاً قبل تفعيل حسابك واحتساب الإحالة!", parse_mode="HTML")
            show_sub_gate(user_id, lang)
            return

        device_id = args[1].replace('verify', '').replace('_', '')
        if device_id:
            with sqlite3.connect(DB_FILE, timeout=30) as conn:
                c = conn.cursor()
                c.execute('SELECT user_id FROM users WHERE device_hash = ? AND user_id != ?', (device_id, user_id))
                if c.fetchone():
                    bot.send_message(user_id, "❌ <b>تم اكتشاف محاولة غش!</b>\nلا يمكنك استخدام نفس الهاتف أو المتصفح للدخول بحسابات متعددة وتجميع النقاط الوهمية 🛑.", parse_mode="HTML")
                    return
                c.execute('UPDATE users SET device_hash = ? WHERE user_id = ?', (device_id, user_id))
                conn.commit()

        if not is_user_verified(user):
            verify_human(user_id)
            user = get_user(user_id)
            
            msg_ar = f"{ce('5848483892113182982', '✅')} <b>لقد تم التحقق بنجاح!</b> ✨\nأنت إنسان حقيقي."
            msg_en = f"{ce('5848483892113182982', '✅')} <b>Verified Successfully!</b> ✨\nYou are a real human."
            bot.send_message(user_id, msg_ar if lang == 'ar' else msg_en, parse_mode="HTML")
            
            process_referral(user_id, lang)
            return show_main_menu(user_id, lang)
        else:
            update_active(user_id)
            return show_main_menu(user_id, lang)

    if not enforce_security(user_id, lang): return
    show_main_menu(user_id, lang)

@bot.message_handler(func=lambda msg: True)
def handle_texts(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if not user: return handle_start(message)
    lang = user[4] or 'ar'

    if not enforce_security(user_id, lang): return

    txt = message.text
    if txt in [f"↩️ {TEXTS['ar']['btn_back']}", f"↩️ {TEXTS['en']['btn_back']}",
               f"🏠 {TEXTS['ar']['btn_home']}", f"🏠 {TEXTS['en']['btn_home']}"]:
        show_main_menu(user_id, lang)
    elif txt in [f"🔗 {TEXTS['ar']['btn_link']}", f"🔗 {TEXTS['en']['btn_link']}"]: trigger_link(user_id, lang)
    elif txt in [f"🪪 {TEXTS['ar']['btn_profile']}", f"🪪 {TEXTS['en']['btn_profile']}"]: trigger_profile(user_id, lang)
    elif txt in [f"🛍️ {TEXTS['ar']['btn_store']}", f"🛍️ {TEXTS['en']['btn_store']}"]: trigger_store(user_id, lang)
    elif txt in [f"🎰 {TEXTS['ar']['btn_wheel']}", f"🎰 {TEXTS['en']['btn_wheel']}"]: trigger_wheel(user_id, lang, message.from_user.username)
    elif txt in [f"📦 {TEXTS['ar']['btn_orders']}", f"📦 {TEXTS['en']['btn_orders']}"]: trigger_orders(user_id, lang)
    elif txt in [f"🌐 {TEXTS['ar']['btn_lang']}", f"🌐 {TEXTS['en']['btn_lang']}"]: bot.send_message(user_id, "🌐 اختر لغة / Select Language 🌍:", reply_markup=lang_inline_kb(), parse_mode="HTML")
    elif txt in [f"🎧 {TEXTS['ar']['btn_contact']}", f"🎧 {TEXTS['en']['btn_contact']}"]: trigger_contact(user_id, lang)
    elif txt in [f"📱 {TEXTS['ar']['btn_social']}", f"📱 {TEXTS['en']['btn_social']}"]: trigger_social(user_id, lang)
    elif txt in [f"❓ {TEXTS['ar']['btn_help']}", f"❓ {TEXTS['en']['btn_help']}"]: trigger_help(user_id, lang)

# ═══════════════════════════════════════════
#             الوظائف التنفيذية
# ═══════════════════════════════════════════
def show_main_menu(user_id, lang):
    bot.send_message(user_id, "القائمة الرئيسية:", reply_markup=main_keyboard(lang), parse_mode="HTML")
    bot.send_message(user_id, TEXTS[lang]['welcome'], reply_markup=main_inline_keyboard(lang), parse_mode="HTML")

def trigger_link(user_id, lang):
    user = get_user(user_id)
    bot_info = bot.get_me()
    msg = TEXTS[lang]['link_msg'].format(bot_info.username, user_id, user[3], user[2])
    markup = section_inline_keyboard(lang)
    markup.add(InlineKeyboardButton("تحديث", callback_data="main_link", style="success", icon_custom_emoji_id="5877581067182936364"))
    bot.send_message(user_id, msg, reply_markup=markup, parse_mode="HTML")

def trigger_profile(user_id, lang):
    user = get_user(user_id)
    raw_username = user[1]
    
    if raw_username and raw_username != "Unknown":
        username_display = f"@{raw_username}"
    else:
        username_display = "بدون يوزر 👤" if lang == 'ar' else "No Username 👤"

    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM orders WHERE user_id = ?', (user_id,))
        total_orders = cursor.fetchone()[0]
    
    msg = TEXTS[lang]['profile_msg'].format(username_display, user_id, user[2], user[3], total_orders)
    markup = section_inline_keyboard(lang)
    markup.add(InlineKeyboardButton("تحديث", callback_data="main_profile", style="success", icon_custom_emoji_id="5877581067182936364"))
    
    try: bot.send_message(user_id, msg, reply_markup=markup, parse_mode="HTML")
    except: pass

def trigger_store(user_id, lang, page=0, edit_message_id=None):
    items_per_page = 5
    total_pages = (len(STORE_ITEMS) + items_per_page - 1) // items_per_page
    start_idx = page * items_per_page
    end_idx = start_idx + items_per_page
    current_items = STORE_ITEMS[start_idx:end_idx]

    markup = InlineKeyboardMarkup(row_width=1)
    for label, pts, item in current_items:
        if "Stars" in item:
            markup.add(InlineKeyboardButton(label, callback_data=f"buy_{pts}_{item}", style="success", icon_custom_emoji_id="5463289097336405244"))
        else:
            markup.add(InlineKeyboardButton(label, callback_data=f"buy_{pts}_{item}", style="success"))
            
    nav_row = []
    if page > 0: nav_row.append(InlineKeyboardButton("السابق", callback_data=f"store_page_{page-1}", style="primary", icon_custom_emoji_id="5213358684024877471"))
    if page < total_pages - 1: nav_row.append(InlineKeyboardButton("التالي", callback_data=f"store_page_{page+1}", style="primary", icon_custom_emoji_id="5215229232476596064"))
    if nav_row: markup.row(*nav_row)

    markup.row(*store_navigation_buttons(lang))
    
    msg_text = TEXTS[lang]['store_msg'].format(page + 1, total_pages)

    if edit_message_id:
        try: bot.edit_message_text(msg_text, chat_id=user_id, message_id=edit_message_id, reply_markup=markup, parse_mode="HTML")
        except: pass
    else:
        bot.send_message(user_id, msg_text, reply_markup=markup, parse_mode="HTML")

def trigger_orders(user_id, lang, edit_message_id=None):
    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT order_id, stars, points, status, created_at FROM orders WHERE user_id = ? ORDER BY order_id DESC LIMIT 10', (user_id,))
        orders = cursor.fetchall()

    if not orders:
        message = TEXTS[lang]['orders_msg'] + TEXTS[lang]['no_orders']
    else:
        message = TEXTS[lang]['orders_msg']
        for order_id, item, points, status, created_at in orders:
            order_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(created_at))
            
            if status == 'pending':
                status_text = "قيد المراجعة ⏳" if lang == 'ar' else "Pending ⏳"
            elif status == 'completed':
                status_text = "تم الحصول على الجائزة ✅" if lang == 'ar' else "Completed ✅"
            elif str(status).startswith('rejected|'):
                reason = str(status).split('|', 1)[1]
                status_text = f"تم رفض الطلب ❌\n💬 السبب: {reason}" if lang == 'ar' else f"Rejected ❌\n💬 Reason: {reason}"
            else:
                status_text = status

            message += TEXTS[lang]['order_line'].format(order_id, item, points, status_text, order_time)
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(InlineKeyboardButton("تحديث", callback_data="refresh_orders", style="success", icon_custom_emoji_id="5877581067182936364"))
    markup.row(*store_navigation_buttons(lang))

    if edit_message_id:
        try: bot.edit_message_text(message, chat_id=user_id, message_id=edit_message_id, reply_markup=markup, parse_mode="HTML")
        except: pass
    else:
        bot.send_message(user_id, message, reply_markup=markup, parse_mode="HTML")

def _slot_machine_frame(frame, total_frames, lang='ar'):
    icons = [
        ce('5350831692292565080', '🔴'),
        ce('5350519289256355751', '🔵'),
        ce('5312359316580216113', '🟢'),
        ce('5359601641848840128', '🎉'),
        ce('5388646216454121816', '🔥')
    ]
    grid = ""
    for _ in range(3):
        row = random.sample(icons, 3)
        grid += "      " + "   ".join(row) + "\n"

    progress = int(((frame + 1) / total_frames) * 100)
    filled = max(1, min(10, round(progress / 10)))
    bar = "▰" * filled + "▱" * (10 - filled)

    return (
        f"{ce('5877466056548691003', '🎡')} <b>عجلة الحظ التفاعلية</b>\n\n"
        f"{grid}\n"
        f"      <b>جاري السحب...</b>\n\n"
        f"{ce('5215327832040811010', '⏳')} <code>{bar}</code> <b>{progress}%</b>\n\n"
        f"{ce('5879623757923881824', '🌀')}"
    )

def trigger_wheel(user_id, lang, username):
    now = time.time()
    user = get_user(user_id)
    last_spin = user[5]

    with sqlite3.connect(DB_FILE, timeout=30) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET last_spin = ? WHERE user_id = ? AND (? - last_spin) >= 86400', (now, user_id, now))
        
        if cursor.rowcount == 0:
            hours_left = round((86400 - (now - last_spin)) / 3600, 1)
            wait_text = (
                f"{ce('5879927695579550387', '⏳')} <b>عفواً! لقد استخدمت لفة الحظ اليومية.</b>\n"
                f"يرجى الانتظار <b>{hours_left}</b> ساعة للمحاولة مجدداً."
            )
            bot.send_message(user_id, wait_text, reply_markup=section_inline_keyboard(lang), parse_mode="HTML")
            return
        conn.commit()

    animation_message = None
    try:
        animation_message = bot.send_message(user_id, _slot_machine_frame(0, 15, lang), parse_mode="HTML")
        total_frames = 15
        for frame in range(1, total_frames):
            time.sleep(0.5) 
            try: bot.edit_message_text(_slot_machine_frame(frame, total_frames, lang), chat_id=user_id, message_id=animation_message.message_id, parse_mode="HTML")
            except: pass
    except: pass

    outcomes = ["lose", "1_point", "5_points", "15_stars", "40_stars"]
    weights = [9470, 410, 50, 50, 20]
    result = random.choices(outcomes, weights=weights, k=1)[0]

    if result in ["1_point", "5_points"]:
        pts_add = 1 if result == "1_point" else 5
        with sqlite3.connect(DB_FILE, timeout=30) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET points = COALESCE(points, 0) + ? WHERE user_id = ?', (pts_add, user_id))
            conn.commit()

    if result == "lose":
        final_ui = f"{ce('5350831692292565080', '💔')} <b>لم يحالفك الحظ هذه المرة!</b>\nالعجلة تتجدد بعد 24 ساعة ⏳."
    else:
        if result == "1_point": 
            prize_title = "نقطة واحدة (1 Point) 🎯"
            desc = "✅ تمت إضافة النقطة إلى رصيدك تلقائياً! ⚡️"
        elif result == "5_points": 
            prize_title = "5 نقاط (5 Points) 🎯"
            desc = "✅ تمت إضافة 5 نقاط إلى رصيدك تلقائياً! ⚡️"
        else:
            if result == "15_stars": prize_title = "15 ⭐️ Stars"
            elif result == "40_stars": prize_title = "40 ⭐️ Stars"
            
            desc = "⏳ لقد تم تسجيل طلبك بنجاح! سيتم مراجعته وتسليمه قريباً، يمكنك متابعته من قسم (طلباتي) 📦."
            
            with sqlite3.connect(DB_FILE, timeout=30) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO orders (user_id, stars, points, status, created_at) VALUES (?, ?, ?, ?, ?)', (user_id, prize_title, 0, 'pending', time.time()))
                order_id = cursor.lastrowid
                conn.commit()
            
            try:
                user_tag = f"@{username}" if username else "بدون يوزر"
                log_text = (
                    "🎰 <b>فائز جديد في عجلة الحظ!</b> 🚀\n\n"
                    f"🧾 الطلب رقم: <b>#{order_id}</b>\n"
                    f"👤 المستخدم: {user_tag} <code>{user_id}</code>\n"
                    f"🎁 الجائزة: <code>{prize_title}</code>\n"
                    f"💰 النقاط المخصومة: <code>0</code> ⚡️ (مجاني من العجلة)"
                )
                markup_log = InlineKeyboardMarkup()
                markup_log.row(
                    InlineKeyboardButton("✅ تأكيد الطلب", callback_data=f"ord_acc_{order_id}_{user_id}", icon_custom_emoji_id="5848483892113182982"),
                    InlineKeyboardButton("❌ رفض الطلب", callback_data=f"ord_rej_{order_id}_{user_id}", icon_custom_emoji_id="5350831692292565080")
                )
                bot.send_message(LOG_CHANNEL, log_text, parse_mode="HTML", reply_markup=markup_log)
            except: pass

        final_ui = (
            f"{ce('5359601641848840128', '🎉')} <b>ضـربـــة حـــظ مـذهـلـــة</b>\n\n"
            f"🎁 <b>الجائزة:</b> 〈 {prize_title} 〉\n"
            f"✅ مبروك! لقد فزت بالجائزة بنجاح 🚀.\n"
            f"<i>{desc}</i>"
        )
        
        if result in ["1_point", "5_points"]:
            try:
                log_text = f"🎡 فائز بنقاط في ماكينة الحظ!\n👤 المستخدم: <code>{user_id}</code>\n🎁 الجائزة: {prize_title}\n🕒 النوع: عجلة الحظ اليومية"
                bot.send_message(LOG_CHANNEL, log_text, parse_mode="HTML")
            except: pass

    if animation_message is not None:
        try: bot.edit_message_text(final_ui, chat_id=user_id, message_id=animation_message.message_id, reply_markup=section_inline_keyboard(lang), parse_mode="HTML")
        except: pass
    else:
        bot.send_message(user_id, final_ui, reply_markup=section_inline_keyboard(lang), parse_mode="HTML")

def trigger_contact(user_id, lang='ar'):
    text = (
        f"{ce('5213256614127086482', '📞')} <b>قنوات التواصل المباشر</b>\n\n"
        f"{ce('5330237710655306682', '💬')} تيليجرام\n"
        f"{ce('5319160079465857105', '📸')} انستجرام\n"
        f"{ce('5323261730283863478', '📘')} فيسبوك\n"
        f"{ce('5334998226636390258', '💬')} واتساب / ديسكورد\n\n"
        f"اختر المنصة المناسبة من الأزرار بالأسفل:\n"
        f"{ce('5303138782004924588', '🔚')}"
    )
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Instagram (gattal_)", url="https://instagram.com/gattal_", style="primary", icon_custom_emoji_id="5319160079465857105"),
        InlineKeyboardButton("WhatsApp مباشر", url="https://wa.me/213674449294", style="primary", icon_custom_emoji_id="5334998226636390258"),
        InlineKeyboardButton("Telegram: @gattal_brahim", url="https://t.me/gattal_brahim", style="primary", icon_custom_emoji_id="5330237710655306682"),
        InlineKeyboardButton("Discord: kaisen_xv", url="https://discord.com/users/kaisen_xv", style="primary", icon_custom_emoji_id="5325612636467903082"),
        InlineKeyboardButton("فيسبوك / Facebook", url="https://www.facebook.com/share/1cdngkRAyZ/", style="primary", icon_custom_emoji_id="5323261730283863478")
    )
    markup.row(*store_navigation_buttons(lang))
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="HTML")

def trigger_social(user_id, lang='ar'):
    text = (
        f"{ce('5224607267797606837', '📱')} <b>حساباتي الرسمية</b>\n\n"
        f"تابعنا على السوشيال ميديا 🌟:\n\n"
        f"{ce('52134063753417312