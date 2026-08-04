from keep_alive import keep_alive
keep_alive()

# coded by @saleh681 in Telegram
import os
import sys
import asyncio
import datetime
import time
import json
import random
import re
import requests
import psutil
from telethon import TelegramClient, events, Button, functions
from telethon.tl.types import MessageEntitySpoiler
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
import pytz

# ============= ایمپورت از فایل‌های lib =============
from lib.Information import *
from lib.command import *
from lib.helpertx import *
from lib.library import *
from lib.updater import *

# ============= تنظیمات اولیه =============
# این مقادیر از فایل Information.py می‌آیند
# اگه در Information.py تعریف نشده‌اند، اینجا تعریف کن
try:
    api_id = API_ID
    api_hash = API_HASH
    admin_user_id = ADMIN_USER_ID
    bot_token = BOT_TOKEN
    helper_username = HELPER_USERNAME
except:
    # مقادیر پیش‌فرض (جایگزین کن)
    api_id = 12345
    api_hash = 'your_api_hash'
    admin_user_id = 123456789
    bot_token = 'your_bot_token'
    helper_username = 'your_helper_bot'

# ============= تعریف متغیرهای سراسری =============
pending_input = {}
saved_messages_cache = {}
anti_delete_chats = set()
ghost_mode_enabled = False
spoiler_mode_enabled = False
enemy_list = []
user_messages = {}
silenced_users = set()
fast_replies = {}
watch_keywords = []
blocked_words = ["کص مادرت"]
scheduled_jobs = {}

daily_stats = {'messages_today': 0, 'unique_senders': set()}
timezone = pytz.timezone('Asia/Tehran')

# ============= تنظیمات پوشه‌ها =============
settings_folder = 'settings'
SAVE_FOLDER = 'saved_media'
MSAVE_DIRECTORY = 'music_saves'
SAVE_DIRECTORY_YT = 'youtube_saves'

for folder in [settings_folder, SAVE_FOLDER, MSAVE_DIRECTORY, SAVE_DIRECTORY_YT]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# ============= تنظیمات پیش‌فرض فایل‌ها =============
file_defaults = {
    'time.txt': 'False',
    'timepic.txt': 'False',
    'nameinfo.txt': 'time',
    'bioinfo.txt': 'False',
    'heart.txt': 'False',
    'rnamest.txt': 'False',
    'bio.txt': 'time',
    'mode.txt': 'Default',
    'creator.txt': '@DevSeyed',
    'tpic.json': '{"cordx": 80, "cordy": 230, "size": 50, "color": "white"}',
    'rname.txt': ''
}

for file_name, default_content in file_defaults.items():
    file_path = os.path.join(settings_folder, file_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(default_content)

# ============= توابع کمکی =============
def read_setting(filename):
    try:
        with open(os.path.join(settings_folder, filename), 'r', encoding='utf-8') as f:
            return f.read().strip()
    except:
        return 'False'

def write_setting(filename, value):
    with open(os.path.join(settings_folder, filename), 'w', encoding='utf-8') as f:
        f.write(str(value))

def get_current_time():
    return datetime.datetime.now(timezone).strftime("%H:%M")

def get_current_date():
    return datetime.datetime.now(timezone).strftime("%Y/%m/%d")

# ============= توابع اصلی ربات =============
async def update_first_name():
    """به‌روزرسانی خودکار اسم اول"""
    while True:
        try:
            if read_setting('time.txt') == 'True':
                current_time = get_current_time()
                await client(UpdateProfileRequest(first_name=f"⏰ {current_time}"))
            await asyncio.sleep(60)
        except Exception as e:
            print(f"Error in update_first_name: {e}")
            await asyncio.sleep(60)

async def update_last_name():
    """به‌روزرسانی خودکار اسم آخر"""
    while True:
        try:
            if read_setting('rnamest.txt') == 'True':
                rname = read_setting('rname.txt')
                if rname:
                    await client(UpdateProfileRequest(last_name=rname))
            await asyncio.sleep(300)
        except Exception as e:
            print(f"Error in update_last_name: {e}")
            await asyncio.sleep(300)

async def update_about():
    """به‌روزرسانی خودکار بیو"""
    while True:
        try:
            if read_setting('bioinfo.txt') == 'True':
                bio_text = read_setting('bio.txt')
                if bio_text == 'time':
                    bio_text = f"⏰ {get_current_time()} | 📅 {get_current_date()}"
                await client(UpdateProfileRequest(about=bio_text))
            await asyncio.sleep(300)
        except Exception as e:
            print(f"Error in update_about: {e}")
            await asyncio.sleep(300)

async def update_profile_photo():
    """به‌روزرسانی خودکار عکس پروفایل با زمان"""
    while True:
        try:
            if read_setting('timepic.txt') == 'True':
                # اینجا کد تولید عکس با زمان رو قرار بده
                # از توابع library.py استفاده کن
                pass
            await asyncio.sleep(3600)
        except Exception as e:
            print(f"Error in update_profile_photo: {e}")
            await asyncio.sleep(3600)

async def send_welcome_message():
    """ارسال پیام خوش‌آمدگویی"""
    try:
        await asyncio.sleep(5)
        await client.send_message('me', "✅ ربات سلف با موفقیت راه‌اندازی شد!")
        await client.send_message('me', f"📅 تاریخ: {get_current_date()}\n⏰ زمان: {get_current_time()}")
    except Exception as e:
        print(f"Error in send_welcome_message: {e}")

async def send_daily_report():
    """ارسال گزارش روزانه"""
    while True:
        now = datetime.datetime.now(timezone)
        target_time = now.replace(hour=23, minute=59, second=0, microsecond=0)
        if now >= target_time:
            target_time += datetime.timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        report = f"""📊 گزارش روزانه

📨 تعداد پیام‌های دریافتی: {daily_stats['messages_today']}
👥 تعداد کاربران متفاوت: {len(daily_stats['unique_senders'])}
🗑 چت‌های ضد حذف فعال: {len(anti_delete_chats)}"""
        await client.send_message('me', report)

        daily_stats['messages_today'] = 0
        daily_stats['unique_senders'] = set()

def load_timers():
    """بارگذاری تایمرها از فایل"""
    timer_file = os.path.join(settings_folder, 'timers.json')
    if os.path.exists(timer_file):
        try:
            with open(timer_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_timers(timers):
    """ذخیره تایمرها در فایل"""
    timer_file = os.path.join(settings_folder, 'timers.json')
    with open(timer_file, 'w', encoding='utf-8') as f:
        json.dump(timers, f, ensure_ascii=False, indent=2)

# ============= کلاینت‌های تلگرام =============
client = TelegramClient('TRself-MT', api_id, api_hash)
bot_client = TelegramClient('helper_session', api_id, api_hash)

# ============= دستورات ربات =============
@client.on(events.NewMessage(pattern='(?i)(/start|/help)'))
async def start_command(event):
    if event.sender_id == admin_user_id:
        await event.reply("🤖 ربات سلف فعال است!\nاز /panel برای دسترسی به پنل استفاده کنید.")

@client.on(events.NewMessage(pattern='(?i)(/panel|پنل)'))
async def show_panel(event):
    if event.sender_id == admin_user_id:
        text = """🎛 پنل مدیریت سلف

⚙️ تنظیمات پروفایل
🔤 فونت‌ها
🗑 مدیریت پیام
🔒 امنیت
👻 حالت مخفی
🔮 سرگرمی
📊 آمار
ℹ️ سیستم

برای دسترسی به هر بخش، دستور مربوطه رو بزنید."""
        await event.reply(text)

@client.on(events.NewMessage(pattern='(?i)(/ping|پینگ)'))
async def ping_command(event):
    if event.sender_id == admin_user_id:
        start = time.time()
        await event.reply("🏓 پینگ...")
        end = time.time()
        await event.reply(f"🏓 پینگ: {round((end - start) * 1000)}ms")

@client.on(events.NewMessage(pattern='(?i)(/status|وضعیت)'))
async def status_command(event):
    if event.sender_id == admin_user_id:
        status_lines = [
            "📊 وضعیت کامل سلف",
            "",
            "⚙️ تنظیمات پروفایل",
            f"🕐 زمان در اسم: {'🟢 روشن' if read_setting('time.txt') == 'True' else '🔴 خاموش'}",
            f"🖼 زمان در عکس: {'🟢 روشن' if read_setting('timepic.txt') == 'True' else '🔴 خاموش'}",
            f"📝 بیو پویا: {'🟢 روشن' if read_setting('bioinfo.txt') == 'True' else '🔴 خاموش'}",
            f"❤️ حالت قلب: {'🟢 روشن' if read_setting('heart.txt') == 'True' else '🔴 خاموش'}",
            f"🎲 اسم رندوم: {'🟢 روشن' if read_setting('rnamest.txt') == 'True' else '🔴 خاموش'}",
            f"🔤 فونت فعلی: {read_setting('mode.txt')}",
            "",
            "🔒 امنیت",
            f"👻 حالت مخفی: {'🟢 روشن' if ghost_mode_enabled else '🔴 خاموش'}",
            f"🫥 حالت اسپویلر: {'🟢 روشن' if spoiler_mode_enabled else '🔴 خاموش'}",
            f"🗑 چت‌های ضد حذف فعال: {len(anti_delete_chats)}",
            "",
            "📊 آمار امروز",
            f"📨 پیام‌های دریافتی: {daily_stats['messages_today']}",
            f"👥 کاربران متفاوت: {len(daily_stats['unique_senders'])}",
            "",
            "ℹ️ سیستم",
            f"💾 مصرف حافظه: {psutil.virtual_memory().percent}%"
        ]
        await event.reply("\n".join(status_lines))

@client.on(events.NewMessage(pattern='(?i)(timename on|timename off|timepic on|timepic off|bio on|bio off|heart on|heart off|rname on|rname off)'))
async def handle_settings(event):
    if event.sender_id != admin_user_id:
        return
    
    command = event.raw_text.lower()
    setting_map = {
        'timename on': ('time.txt', 'True'),
        'timename off': ('time.txt', 'False'),
        'timepic on': ('timepic.txt', 'True'),
        'timepic off': ('timepic.txt', 'False'),
        'bio on': ('bioinfo.txt', 'True'),
        'bio off': ('bioinfo.txt', 'False'),
        'heart on': ('heart.txt', 'True'),
        'heart off': ('heart.txt', 'False'),
        'rname on': ('rnamest.txt', 'True'),
        'rname off': ('rnamest.txt', 'False'),
    }
    
    if command in setting_map:
        filename, value = setting_map[command]
        write_setting(filename, value)
        await event.reply(f"✅ تنظیمات با موفقیت تغییر کرد: {command}")

@client.on(events.NewMessage(pattern='(?i)(/setname|تنظیم_نام) (.+)'))
async def set_user_first_name(event):
    if event.sender_id == admin_user_id:
        new_name = event.pattern_match.group(1).strip()
        try:
            await client(UpdateProfileRequest(first_name=new_name))
            await event.reply(f"✅ اسم اول با موفقیت به «{new_name}» تغییر کرد.")
        except Exception as e:
            await event.reply(f"❌ خطا: {e}")

@client.on(events.NewMessage(pattern='(?i)(/addbio|اضافه_بیو) (.+)'))
async def add_bio(event):
    if event.sender_id == admin_user_id:
        new_bio = event.pattern_match.group(1).strip()
        try:
            await client(UpdateProfileRequest(about=new_bio))
            write_setting('bio.txt', new_bio)
            await event.reply(f"✅ بیو با موفقیت به «{new_bio}» تغییر کرد.")
        except Exception as e:
            await event.reply(f"❌ خطا: {e}")

@client.on(events.NewMessage(pattern='(?i)(/addlname|اضافه_نام_خانوادگی) (.+)'))
async def add_lname(event):
    if event.sender_id == admin_user_id:
        new_lname = event.pattern_match.group(1).strip()
        try:
            await client(UpdateProfileRequest(last_name=new_lname))
            await event.reply(f"✅ نام خانوادگی با موفقیت به «{new_lname}» تغییر کرد.")
        except Exception as e:
            await event.reply(f"❌ خطا: {e}")

@client.on(events.NewMessage(pattern='(?i)(/addrname|اضافه_نام_رندوم) (.+)'))
async def add_rname(event):
    if event.sender_id == admin_user_id:
        new_rname = event.pattern_match.group(1).strip()
        write_setting('rname.txt', new_rname)
        write_setting('rnamest.txt', 'True')
        await event.reply(f"✅ اسم رندوم «{new_rname}» با موفقیت اضافه شد.")

@client.on(events.NewMessage(pattern='(?i)(/delrname|حذف_نام_رندوم)'))
async def delete_rname(event):
    if event.sender_id == admin_user_id:
        write_setting('rname.txt', '')
        write_setting('rnamest.txt', 'False')
        await event.reply("✅ اسم رندوم با موفقیت حذف شد.")

@client.on(events.NewMessage(pattern='(?i)(/reload|ریلود)'))
async def reload_bot(event):
    if event.sender_id == admin_user_id:
        await event.reply("🔄 در حال ری‌لود ربات...")
        os.execv(sys.executable, ['python'] + sys.argv)

@client.on(events.NewMessage(pattern='(?i)(/logout|خروج)'))
async def logout_handler(event):
    if event.sender_id == admin_user_id:
        await event.reply("⚠️ در حال خروج از اکانت...")
        await client.log_out()
        sys.exit(0)

@client.on(events.NewMessage(pattern='(?i)(/mem|حافظه)'))
async def mem_command(event):
    if event.sender_id == admin_user_id:
        mem = psutil.virtual_memory()
        await event.reply(f"💾 حافظه:\nکل: {mem.total / (1024**3):.1f}GB\nمصرف: {mem.percent}%\nآزاد: {mem.available / (1024**3):.1f}GB")

# ============= دستورات مربوط به ضد حذف =============
@client.on(events.NewMessage(pattern='^(ضد حذف|antidelete)$'))
async def toggle_anti_delete(event):
    if event.sender_id == admin_user_id:
        chat_id = event.chat_id
        if chat_id in anti_delete_chats:
            anti_delete_chats.remove(chat_id)
            await event.reply("❌ ضد حذف برای این چت غیرفعال شد.")
        else:
            anti_delete_chats.add(chat_id)
            await event.reply("✅ ضد حذف برای این چت فعال شد.")

# ============= ذخیره خودکار پیام‌های نابودشونده =============
@client.on(events.NewMessage)
async def save_self_destructing_media(event):
    try:
        if (event.sender_id != admin_user_id and 
            event.is_private and 
            event.message.media and 
            hasattr(event.message.media, 'ttl_seconds') and 
            event.message.media.ttl_seconds is not None and 
            event.message.media.ttl_seconds > 0):
            
            file = await event.download_media()
            user_id = event.sender_id
            username = event.sender.username if event.sender else "Unknown"
            caption = f"❈ Self-Saved Photo From User: {user_id}, @{username}"
            await client.send_file(admin_user_id, file, caption=caption)
            os.remove(file)
    except Exception as e:
        print(f"Error saving self-destructing media: {e}")

# ============= ردیابی پیام‌های ویرایش و حذف =============
@client.on(events.NewMessage)
async def cache_private_messages(event):
    if event.is_private and event.sender_id != admin_user_id:
        sender = await event.get_sender()
        if sender and getattr(sender, 'bot', False):
            return
        name = sender.first_name if sender and sender.first_name else "کاربر ناشناس"
        saved_messages_cache[event.id] = {
            'text': event.raw_text or "(بدون متن)",
            'name': name,
            'time': event.date.strftime('%H:%M:%S')
        }
        daily_stats['messages_today'] += 1
        daily_stats['unique_senders'].add(event.sender_id)

@client.on(events.MessageEdited())
async def track_edited_messages(event):
    if event.is_private and event.sender_id != admin_user_id:
        old = saved_messages_cache.get(event.id)
        old_text = old['text'] if old else "نامشخص"
        name = old['name'] if old else "کاربر ناشناس"
        await client.send_message(
            'me',
            f"✏️ پیام ویرایش شد\nفرستنده: {name}\nساعت: {event.date.strftime('%H:%M:%S')}\nمتن قبلی: {old_text}\nمتن جدید: {event.raw_text}"
        )
        saved_messages_cache[event.id] = {
            'text': event.raw_text or "(بدون متن)",
            'name': name,
            'time': event.date.strftime('%H:%M:%S')
        }

@client.on(events.MessageDeleted())
async def track_deleted_messages(event):
    for msg_id in event.deleted_ids:
        data = saved_messages_cache.get(msg_id)
        if data:
            await client.send_message(
                'me',
                f"🗑 پیام حذف شد\nفرستنده: {data['name']}\nساعت: {data['time']}\nمتن: {data['text']}"
            )
            del saved_messages_cache[msg_id]

# ============= ترجمه =============
@client.on(events.NewMessage(pattern='(?i)(انگلیسیش کن|/entranslate)(.*)'))
async def translate_to_english(event):
    if event.sender_id != admin_user_id:
        return
    
    if event.is_reply:
        replied = await event.get_reply_message()
        text = replied.raw_text
    else:
        parts = event.raw_text.split(' ', 1)
        text = parts[1].strip() if len(parts) > 1 else None
    
    if not text:
        await event.reply("روی یه پیام ریپلای کنید یا متن رو جلوی دستور بنویسید.")
        return
    
    try:
        translator = Translator()
        translated = translator.translate(text, dest='en')
        await event.reply(f"📝 ترجمه انگلیسی:\n\n{translated.text}")
    except Exception as e:
        await event.reply(f"❌ خطا در ترجمه: {e}")

@client.on(events.NewMessage(pattern='(?i)(فارسیش کن|/fatranslate)(.*)'))
async def translate_to_farsi(event):
    if event.sender_id != admin_user_id:
        return
    
    if event.is_reply:
        replied = await event.get_reply_message()
        text = replied.raw_text
    else:
        parts = event.raw_text.split(' ', 1)
        text = parts[1].strip() if len(parts) > 1 else None
    
    if not text:
        await event.reply("روی یه پیام ریپلای کنید یا متن رو جلوی دستور بنویسید.")
        return
    
    try:
        translator = Translator()
        translated = translator.translate(text, dest='fa')
        await event.reply(f"📝 ترجمه فارسی:\n\n{translated.text}")
    except Exception as e:
        await event.reply(f"❌ خطا در ترجمه: {e}")

# ============= کپی به سیو با اسپویلر =============
@client.on(events.NewMessage(pattern='(?i)(کپی به سیو|savecopy)$'))
async def copy_to_saved(event):
    if event.sender_id != admin_user_id:
        return
    
    if not event.is_reply:
        await event.reply("روی یه پیام ریپلای کنید و بعد این دستور رو بزنید.")
        return
    
    replied = await event.get_reply_message()
    sender = await replied.get_sender()
    sender_name = sender.first_name if sender and sender.first_name else "ناشناس"
    caption = f"📌 کپی‌شده از: {sender_name}\n📝 متن: {replied.raw_text or '(بدون متن)'}"

    if spoiler_mode_enabled and replied.raw_text and not replied.media:
        entities = [MessageEntitySpoiler(offset=0, length=len(replied.raw_text))]
        await client.send_message('me', replied.raw_text, formatting_entities=entities)
    elif replied.media:
        await client.send_file('me', replied.media, caption=caption)
    else:
        await client.send_message('me', caption)
    
    await event.delete()

# ============= گوست مود =============
@client.on(events.NewMessage(pattern='(?i)(ghost on|گوست روشن)$'))
async def ghost_mode_on_text(event):
    global ghost_mode_enabled
    if event.sender_id != admin_user_id:
        return
    ghost_mode_enabled = True
    await event.reply("👻 حالت مخفی‌کار فعال شد.")

@client.on(events.NewMessage(pattern='(?i)(ghost off|گوست خاموش)$'))
async def ghost_mode_off_text(event):
    global ghost_mode_enabled
    if event.sender_id != admin_user_id:
        return
    ghost_mode_enabled = False
    await event.reply("👁 حالت مخفی‌کار غیرفعال شد.")

@client.on(events.NewMessage(pattern='(?i)(اسپویلر روشن|spoiler on)$'))
async def spoiler_on(event):
    global spoiler_mode_enabled
    if event.sender_id != admin_user_id:
        return
    spoiler_mode_enabled = True
    await event.reply("✅ حالت اسپویلر فعال شد. «کپی به سیو» به‌صورت اسپویلر ارسال میشه.")

@client.on(events.NewMessage(pattern='(?i)(اسپویلر خاموش|spoiler off)$'))
async def spoiler_off(event):
    global spoiler_mode_enabled
    if event.sender_id != admin_user_id:
        return
    spoiler_mode_enabled = False
    await event.reply("❌ حالت اسپویلر غیرفعال شد.")

# ============= بلاک و آنبلاک =============
@client.on(events.NewMessage(pattern='(?i)(بلاک|block)$'))
async def block_user(event):
    if event.sender_id != admin_user_id:
        return
    if not event.is_reply:
        await event.reply("روی پیام کاربر مدنظر ریپلای کنید.")
        return
    replied = await event.get_reply_message()
    target_id = replied.sender_id
    await client(BlockRequest(target_id))
    await event.reply(f"🚫 کاربر {target_id} بلاک شد.")

@client.on(events.NewMessage(pattern='(?i)(آنبلاک|unblock)$'))
async def unblock_user(event):
    if event.sender_id != admin_user_id:
        return
    if not event.is_reply:
        await event.reply("روی پیام کاربر مدنظر ریپلای کنید.")
        return
    replied = await event.get_reply_message()
    target_id = replied.sender_id
    await client(UnblockRequest(target_id))
    await event.reply(f"✅ کاربر {target_id} آنبلاک شد.")

# ============= فال حافظ =============
@client.on(events.NewMessage(pattern='(?i)(فال حافظ|falhafez)$'))
async def send_hafez_fortune(event):
    if event.sender_id != admin_user_id:
        return
    try:
        response = requests.get('https://hafez-dxle.onrender.com/fal')
        data = response.json()
        title = data.get('title', '')
        interpretation = data.get('interpreter', 'فالی پیدا نشد.')
        await event.reply(f"🔮 فال حافظ: {title}\n\n{interpretation}")
    except Exception as e:
        await event.reply(f"❌ خطا در دریافت فال: {e}")

# ============= ویس به متن =============
@client.on(events.NewMessage(pattern='(?i)(ویس به متن|voicetotext)$'))
async def voice_to_text(event):
    if event.sender_id != admin_user_id:
        return
    if not event.is_reply:
        await event.reply("روی یه پیام ویس ریپلای کنید و بعد این دستور رو بزنید.")
        return
    
    replied = await event.get_reply_message()
    if not replied.voice:
        await event.reply("پیامی که روش ریپلای کردید ویس نیست.")
        return

    try:
        ogg_path = await replied.download_media()
        wav_path = ogg_path.replace('.ogg', '.wav')
        AudioSegment.from_ogg(ogg_path).export(wav_path, format='wav')

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
        
        text = recognizer.recognize_google(audio_data, language='fa-IR')
        await event.reply(f"📝 متن ویس:\n\n{text}")
    except sr.UnknownValueError:
        await event.reply("متأسفانه نتونستم صدا رو تشخیص بدم.")
    except Exception as e:
        await event.reply(f"❌ خطا: {e}")
    finally:
        try:
            os.remove(ogg_path)
            os.remove(wav_path)
        except:
            pass

# ============= زمانبند (Scheduler) =============
@client.on(events.NewMessage(pattern='(?i)^زمانبند (\d+) (.+)$'))
async def start_scheduled_post(event):
    if event.sender_id != admin_user_id:
        return
    if not event.is_reply:
        await event.reply("روی متنی که می‌خوای تکرار بشه ریپلای کن، بعد بنویس:\nزمانبند [دقیقه] [آیدی یا یوزرنیم گروه]")
        return
    
    try:
        minutes = int(event.pattern_match.group(1))
        target = event.pattern_match.group(2).strip()
        replied = await event.get_reply_message()
        text_to_send = replied.raw_text
        
        if not text_to_send:
            await event.reply("پیامی که روش ریپلای کردید متن نداره.")
            return
        
        try:
            entity = await client.get_entity(target)
        except:
            try:
                entity = await client.get_entity(int(target))
            except Exception as e:
                await event.reply(f"گروه پیدا نشد: {e}")
                return
        
        job_id = (max(scheduled_jobs.keys()) + 1) if scheduled_jobs else 1
        
        async def run_scheduled_job():
            while True:
                await asyncio.sleep(minutes * 60)
                try:
                    await client.send_message(entity, text_to_send)
                except Exception as e:
                    await client.send_message(admin_user_id, f"⚠️ خطا در زمانبند #{job_id}: {e}")
        
        task = client.loop.create_task(run_scheduled_job())
        scheduled_jobs[job_id] = {'task': task, 'target': target, 'minutes': minutes, 'text': text_to_send}
        await event.reply(f"✅ زمانبند #{job_id} فعال شد: هر {minutes} دقیقه به {target}")
        
    except Exception as e:
        await event.reply(f"❌ خطا: {e}")

@client.on(events.NewMessage(pattern='(?i)^لیست زمانبندها$'))
async def list_scheduled_jobs(event):
    if event.sender_id != admin_user_id:
        return
    if not scheduled_jobs:
        await event.reply("هیچ زمانبندی فعال نیست.")
        return
    lines = ["📅 زمانبندهای فعال:"]
    for jid, info in scheduled_jobs.items():
        lines.append(f"#{jid} → هر {info['minutes']} دقیقه به {info['target']}")
    await event.reply("\n".join(lines))

@client.on(events.NewMessage(pattern='(?i)^حذف زمانبند (\d+)$'))
async def delete_scheduled_job(event):
    if event.sender_id != admin_user_id:
        return
    try:
        job_id = int(event.pattern_match.group(1))
        job = scheduled_jobs.get(job_id)
        if not job:
            await event.reply("همچین زمانبندی وجود نداره.")
            return
        job['task'].cancel()
        del scheduled_jobs[job_id]
        await event.reply(f"✅ زمانبند #{job_id} حذف شد.")
    except Exception as e:
        await event.reply(f"❌ خطا: {e}")

# ============= راه‌اندازی ربات =============
async def main():
    try:
        # استارت کلاینت‌ها
        await client.start()
        await bot_client.start(bot_token=bot_token)
        
        # اجرای تسک‌های پس‌زمینه
        client.loop.create_task(update_first_name())
        client.loop.create_task(update_last_name())
        client.loop.create_task(update_about())
        client.loop.create_task(update_profile_photo())
        client.loop.create_task(send_daily_report())
        
        # ارسال پیام خوش‌آمدگویی
        await send_welcome_message()
        
        print("✅ ربات با موفقیت راه‌اندازی شد!")
        print(f"📱 اکانت: {await client.get_me()}")
        
        # اجرای ربات‌ها
        await asyncio.gather(
            client.run_until_disconnected(),
            bot_client.run_until_disconnected()
        )
        
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی: {e}")
        raise

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 ربات متوقف شد.")
    except Exception as e:
        print(f"❌ خطای اصلی: {e}")
