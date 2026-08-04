from keep_alive import keep_alive
keep_alive()

#coded by @saleh681 in Telegram
from lib import *
from telethon import Button
from telethon.tl.types import MessageEntitySpoiler
import speech_recognition as sr
from pydub import AudioSegment
pending_input = {}
bot_client = TelegramClient('helper_session', api_id, api_hash)
saved_messages_cache = {}
anti_delete_chats = set()
ghost_mode_enabled = False
spoiler_mode_enabled = False
settings_folder = 'settings'
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

if not os.path.exists(settings_folder):
    os.makedirs(settings_folder)

for file_name, default_content in file_defaults.items():
    file_path = os.path.join(settings_folder, file_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write(default_content)

#check command
@client.on(events.NewMessage(pattern='(?i)(/check|/چک)'))
async def handle_start_command(event):
    await start_command(event)
#end of command check


@client.on(events.NewMessage(pattern='(?i)(/help|/راهنما)'))
async def handle_inline(event):
    if event.sender_id == admin_user_id:
        try:
            if event.raw_text.lower() in ['/help', '/راهنما']:
                result = await client.inline_query(f'{helper_username}', "/panel")
                await result[0].click(event.chat_id)
                await event.delete()
            elif event.raw_text in ['/help 1', '/راهنما 1']:
                await help_1(event)
            elif event.raw_text in ['/help 2', '/راهنما 2']:
                await help_2(event)
            elif event.raw_text in ['/help 3', '/راهنما 3']:
                await help_3(event)
            elif event.raw_text in ['/help 4', '/راهنما 4']:
                await help_4(event)
        except Exception as e:
            await event.reply(f"Error sending panel: {e}")


@client.on(events.NewMessage(pattern='(?i)(/ping|/پینگ)'))
async def handle_ping(event):
    await ping(event)


@client.on(events.NewMessage(pattern='(?i)(/mem|/حافظه)'))
async def handle_mem(event):
    await mem(event)


if not os.path.exists(MSAVE_DIRECTORY):
    os.makedirs(MSAVE_DIRECTORY)

@client.on(events.NewMessage(pattern='(?i)(/gmusic|/موزیک)'))
async def handle_sc(event):
    await sc(event)

@client.on(events.NewMessage(pattern='(?i)(/tarikh|/تاریخ)'))
async def handle_tarikh(event):
    await tarikh(event)

@client.on(events.NewMessage(pattern='(?i)(/gmsg|/تایپ_متن)'))
async def handle_gmsg(event):
    await gmsg(event)

@client.on(events.NewMessage(pattern='(?i)(/weather|/هواشناسی)'))
async def handle_weather(event):
    await weather(event)

@client.on(events.NewMessage(pattern='(?i)(/rsong|/آهنگ_رندوم)'))
async def handle_rsong(event):
    await rsong(event)

@client.on(events.NewMessage(pattern='(?i)(/info|/اطلاعات)'))
async def handle_info(event):
    await info(event)

@client.on(events.NewMessage(pattern='(?i)(/setprof|/تنظیم_عکس)'))
async def handle_set_profile_pic(event):
    await set_profile_pic(event)

@client.on(events.NewMessage(pattern='(?i)(/delprof|/حذف_عکس)'))
async def handle_delete_profile_pic(event):
    await delete_profile_pic(event)

@client.on(events.NewMessage(pattern='(?i)(/rinfo|/اطلاعات_کاربر)'))
async def handle_rinfo(event):
    await rinfo(event)

@client.on(events.NewMessage(pattern='(?i)(/rem|/حذف_اخیر)'))
async def handle_delete_recent_messages(event):
    await delete_recent_messages(event)

@client.on(events.NewMessage(pattern='(?i)(/sgoogle|/گوگل)'))
async def handle_sgoogle(event):
    await sgoogle(event)

@client.on(events.NewMessage(pattern='(?i)(/wiki|/ویکی)'))
async def handle_wiki(event):
    await wiki(event)

@client.on(events.NewMessage(pattern='(?i)(/save|/ذخیره)'))
async def handle_save_message(event):
    await save_message(event)
#Auto Save
@client.on(events.NewMessage)
async def save_self_destructing_media(event):
    try:
        if (
            event.sender_id != admin_user_id
            and event.is_private
            and event.message.media
            and hasattr(event.message.media, 'ttl_seconds')
            and event.message.media.ttl_seconds is not None
            and event.message.media.ttl_seconds > 0
        ):
            file = await event.download_media()
            user_id = event.sender_id
            username = event.sender.username
            caption = f"❈ Self-Saved Photo From User: {user_id}, @{username}"
            await client.send_file(admin_user_id, file, caption=caption)
            os.remove(file)

    except Exception as e:
        await event.respond(f"❈ Error while saving self-destructing media: {str(e)}")
# End Auto Save
        
@client.on(events.NewMessage(pattern='(?i)(/addbio|/اضافه_بیو)'))
async def handle_add_bio(event):
    await add_bio(event)

@client.on(events.NewMessage(pattern='(?i)(/addlname|/اضافه_نام_خانوادگی)'))
async def handle_add_lname(event):
    await add_lname(event)

@client.on(events.NewMessage(pattern='(?i)(/addrname|/اضافه_نام_رندوم)'))
async def handle_add_rname(event):
    await add_rname(event)

@client.on(events.NewMessage(pattern='(?i)(/delrname|/حذف_نام_رندوم)'))
async def handle_delete_rname(event):
    await delete_rname(event)

@client.on(events.NewMessage(pattern='(?i)(/reload|/ریلود)'))
async def handle_reload_bot(event):
    await reload_bot(event)

@client.on(events.NewMessage(pattern='(?i)(/backupchat|/پشتیبان_چت)'))
async def handle_backup_chat(event):
    await backup_chat(event)

@client.on(events.NewMessage(pattern='(?i)(/calc|/محاسبه)'))
async def handle_calculator(event):
    await calculator(event)

@client.on(events.NewMessage(pattern='(?i)(/create_channel|/ساخت_کانال) (.*)'))
async def handle_create_channel(event):
    await create_channel(event)

@client.on(events.NewMessage(pattern='(?i)(/silent|/سکوت)'))
async def handle_enemy_mode(event):
    await enemy_mode(event)

@client.on(events.NewMessage(pattern='(?i)(/unsilent|/رفع_سکوت)'))
async def handle_unenemy_mode(event):
    await unenemy_mode(event)

@client.on(events.NewMessage)
async def delete_enemy_messages(event):
    sender_id = event.sender_id
    if sender_id in enemy_list:
        user_msgs = user_messages.get(sender_id, [])
        user_msgs.append(event.message)
        user_messages[sender_id] = user_msgs[-10:]

        if len(user_msgs) >= 10:
            await client(functions.contacts.BlockRequest(sender_id))
            await client.send_message(admin_user_id, f"❈System Notification ⚠️\nBlocked User {sender_id} for sending too many messages while in silent mode")

        await event.delete()

@client.on(events.NewMessage(pattern='(?i)(/tag|/تگ)'))
async def handle_tag_all_members(event):
    await tag_all_members(event)

@client.on(events.NewMessage(pattern='(?i)(/Del|/پاک)'))
async def handle_delete_reply(event):
    await delete_reply(event)

@client.on(events.NewMessage(pattern='(?i)(/GSilent|/سکوت_گروه)'))
async def handle_save_user_id(event):
    await save_user_id(event)

@client.on(events.NewMessage(pattern='(?i)(/GUnSilent|/رفع_سکوت_گروه)(\s+\d+)?'))
async def handle_remove_user_from_silenced(event):
    await remove_user_from_silenced(event)

@client.on(events.NewMessage(pattern='(?i)(/promote|/ادمین)'))
async def handle_promote_user_to_admin(event):
    await promote_user_to_admin(event)

@client.on(events.NewMessage(pattern='(?i)(/demote|/عزل)'))
async def handle_demote_admin(event):
    await demote_admin(event)

@client.on(events.NewMessage)
async def delete_silent_user_messages(event):
    if event.is_group and event.sender_id in silenced_users:
        await client.delete_messages(event.chat_id, [event.id])

@client.on(events.NewMessage(pattern='(?i)(/pass|/رمز)'))
async def handle_generate_password(event):
    await generate_password(event)

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
@client.on(events.NewMessage(pattern='(?i)(/Gmedia|/ذخیره_ویدیو)'))
async def handle_save_video(event):
    await save_video(event)

@client.on(events.NewMessage(pattern='(?i)(/Smedia|/ارسال_ویدیو)'))
async def handle_send_video(event):
    await send_video(event)

@client.on(events.NewMessage(pattern='(?i)(/Lmedia|/لیست_ویدیو)'))
async def handle_list_saved_media(event):
    await list_saved_media(event)

@client.on(events.NewMessage(pattern='(?i)(/Freplay|/پاسخ_سریع)'))
async def handle_fast_replies(event):
    await ffast_replies(event)

@client.on(events.NewMessage(pattern='(?i)(/Lreplay|/لیست_پاسخ)'))
async def handle_show_fast_replies(event):
    await show_fast_replies(event)

@client.on(events.NewMessage)
async def handle_user_message(event):
    if event.sender_id != admin_user_id:
        message = event.raw_text
        reply = fast_replies.get(message.lower())
        if reply:
            await event.reply(reply)

@client.on(events.NewMessage(pattern='(?i)(/whois|/هویت_دامنه)'))
async def handle_whois_domain(event):
    await whois_domain(event)

@client.on(events.NewMessage(pattern='(?i)(/Scrypto|/قیمت_ارز)'))
async def handle_show_crypto_prices(event):
    await show_crypto_prices(event)

@client.on(events.NewMessage(pattern='(?i)(/sreplace|/جایگزین)'))
async def handle_replace_words(event):
    await replace_words(event)

@client.on(events.NewMessage(pattern='(?i)(/Convertdate|/تبدیل_تاریخ)'))
async def convert_date(event):
    await convert_date(event)

@client.on(events.NewMessage(pattern='(?i)(/setname|/تنظیم_نام)'))
async def handle_set_user_first_name(event):
    await set_user_first_name(event)

@client.on(events.NewMessage(pattern='(?i)(/sfootball|/فوتبال)'))
async def handle_get_football_stats(event):
    await get_football_stats(event)

@client.on(events.NewMessage(pattern='(?i)(/setcolor|/تنظیم_رنگ)'))
async def handle_apply_color_filter(event):
    await apply_color_filter(event)

@client.on(events.NewMessage(pattern='(?i)(/flood|/فلود) (\d+) - ([\w,]+)'))
async def handle_flood_message(event):
    await flood_message(event)

@client.on(events.NewMessage(pattern='(?i)(/orcen|/تبدیل_ویس) (.+)'))
async def handle_replay_as_voice(event):
    await replay_as_voice(event)

@client.on(events.NewMessage(pattern='(?i)(/setfname|/تنظیم_نام_فایل) (.+)'))
async def handle_set_music_name(event):
    await set_music_name(event)

@client.on(events.NewMessage(pattern='(?i)(/screen|/اسکرین) (.+)'))
async def handle_take_screenshot(event):
    await take_screenshot(event)

if not os.path.exists(SAVE_DIRECTORY_YT):
    os.makedirs(SAVE_DIRECTORY_YT)

@client.on(events.NewMessage(pattern='(?i)(/yt|/یوتیوب) (.+)'))
async def handle_download_youtube_video(event):
    await download_youtube_video(event)

@client.on(events.NewMessage(pattern='(?i)(/Sproxy|/پروکسی)'))
async def handle_proxy_command(event):
    await proxy_command(event)

@client.on(events.NewMessage(pattern='(?i)(/Sv2ray|/وی_تو_ری)'))
async def handle_v2ray_command(event):
    await v2ray_command(event)


@client.on(events.NewMessage(pattern='(?i)(/time|/ساعت) (.+)'))
async def handle_get_world_time(event):
    await get_world_time(event)

load_timers()

@client.on(events.NewMessage(pattern='(?i)(newtimer|تایمر_جدید) (.+)'))
async def handle_create_timer(event):
    await create_timer(event)

@client.on(events.NewMessage(pattern='(?i)(deltimer|حذف_تایمر) (.+)'))
async def handle_delete_timer(event):
    await delete_timer(event)

@client.on(events.NewMessage(pattern='(?i)(timers|تایمرها)'))
async def handle_list_timers(event):
    await list_timers(event)

@client.on(events.NewMessage(pattern='(?i)(clean timers|پاکسازی_تایمرها)'))
async def handle_clean_timers(event):
    await clean_timers(event)

@client.on(events.NewMessage(pattern='(?i)(gfile|فایل) (.+)'))
async def handle_download_file(event):
    await download_file(event)

@client.on(events.NewMessage(pattern='(?i)(getip|آی_پی) (.+)'))
async def handle_get_ip_info(event):
    await get_ip_info(event)
@client.on(events.NewMessage(pattern='(?i)(/sunextract|/استخراج فایل)'))
async def handle_extract_files(event):
    await extract_files(event)

@client.on(events.NewMessage(pattern='(?i)(Stv|تلویزیون)'))
async def handle_send_tv_channels(event):
    await send_tv_channels(event)

@client.on(events.NewMessage(pattern='(به qr|sqr|به_کیوآر)'))
async def handle_create_qr_code(event):
    await create_qr_code(event)

@client.on(events.NewMessage(pattern='(?i)(خواندن qr|readqr|خواندن_کیوآر)'))
async def handle_read_qr_code(event):
    await read_qr_code(event)

@client.on(events.NewMessage(pattern='(پاکسازی همه|cleanall)'))
async def handle_clean_messages_containing_text(event):
    await clean_messages_containing_text(event)

@client.on(events.NewMessage(pattern='^(joinall|پیوستن به همه)$'))
async def handle_join_all_channels(event):
    await join_all_channels(event)

@client.on(events.NewMessage(pattern='^(setusername|تنظیم نام کاربری) (.+)'))
async def handle_set_bot_username(event):
    await set_bot_username(event)

@client.on(events.NewMessage(pattern='^(اخراج|kick) (.+)'))
async def handle_kick_users(event):
    await kick_users(event)

@client.on(events.NewMessage(pattern='(پاکسازی بین|cleanb)'))
async def handle_clean_between_messages(event):
    await clean_between_messages(event)

@client.on(events.NewMessage(pattern='(?i)(/Ggit|/گیت)'))
async def handler_Git(event):
    await Git(event)

@client.on(events.NewMessage(pattern='(?i)(/copycontent|/کپی_محتوا)'))
async def handler_copycontent(event):
    await copycontent(event)

@client.on(events.NewMessage(pattern='(?i)(ReadAllPvs|خواندن_همه_پیوی)'))
async def handle_read_all_pvs(event):
    await read_all_pvs(event)

@client.on(events.NewMessage(pattern='(?i)(ReadallGps|خواندن_همه_گروه)'))
async def handle_read_all_groups(event):
    await read_all_groups(event)

@client.on(events.NewMessage(pattern='(?i)(ReadAllChannels|خواندن_همه_کانال)'))
async def handle_read_all_channels(event):
    await read_all_channels(event)

@client.on(events.NewMessage(pattern='(?i)(ReadAllBots|خواندن_همه_ربات)'))
async def handle_read_all_bots(event):
    await read_all_bots(event)

@client.on(events.NewMessage(pattern='(?i)(typing on|تایپ روشن)'))
async def handle_start_typing(event):
    await start_typing(event)

@client.on(events.NewMessage(pattern='(?i)(typing off|تایپ خاموش)'))
async def handle_stop_typing(event):
    await stop_typing(event)

@client.on(events.NewMessage(pattern='(?i)(sticker on|استیکر روشن)'))
async def handle_start_sticker(event):
    await start_sticker(event)

@client.on(events.NewMessage(pattern='(?i)(sticker off|استیکر خاموش)'))
async def handle_stop_sticker(event):
    await stop_sticker(event)

@client.on(events.NewMessage(pattern='(?i)(gaming on|گیم روشن)'))
async def handle_start_game(event):
    await start_game(event)

@client.on(events.NewMessage(pattern='(?i)(gaming off|گیم خاموش)'))
async def handle_stop_game(event):
    await stop_game(event)

@client.on(events.NewMessage(pattern='(?i)(DelVideos|حذف_ویدیوها)'))
async def delete_videos(event):
    await delete_media(event, media_type='video')

@client.on(events.NewMessage(pattern='(?i)(DelPhotos|حذف_عکسها)'))
async def delete_photos(event):
    await delete_media(event, media_type='photo')

@client.on(events.NewMessage(pattern='(?i)(DelVoices|حذف_ویسها)'))
async def delete_voices(event):
    await delete_media(event, media_type='voice')

@client.on(events.NewMessage(pattern='(?i)(DelFiles|حذف_فایلها)'))
async def delete_files(event):
    await delete_media(event, media_type='document')

@client.on(events.NewMessage(pattern='(?i)(DelVideoNotes|حذف_ویدیومسیج)'))
async def delete_video_notes(event):
    await delete_media(event, media_type='video_note')

@client.on(events.NewMessage(pattern='(?i)(DelGifs|حذف_گیفها)'))
async def delete_gifs(event):
    await delete_media(event, media_type='gif')

@client.on(events.NewMessage(pattern='(?i)(Pvinfo|اطلاعات_پیوی)'))
async def handle_pvinfo(event):
    await pvinfo(event)
@client.on(events.NewMessage(pattern='(?i)^(/chkdomain|/چک_دامنه)'))
async def handle_check_domain(event):
    await check_domain(event)

@client.on(events.NewMessage(pattern='(?i)^(/logout|/خروج)'))
async def logout_handler(event):
    await logout(event)

@client.on(events.NewMessage(pattern='(?i)(tpic|عکس_موقت)'))
async def handle_tpic_set(event):
    if event.raw_text.lower() in ['tpic set', 'عکس_موقت تنظیم']:
        await tpic_set(event)
    elif event.raw_text.lower() in ['tpic prv', 'عکس_موقت خصوصی']:
        await tpic_prv(event)


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

@client.on(events.NewMessage())
async def cache_private_messages(event):
    if event.is_private and event.sender_id != admin_user_id:
        sender = await event.get_sender()
        if sender and getattr(sender, 'bot', False):
            return
        name = sender.first_name if sender.first_name else "کاربر ناشناس"
        saved_messages_cache[event.id] = {
            'text': event.raw_text,
            'name': name,
            'time': event.date.strftime('%H:%M:%S')
        }

@client.on(events.MessageEdited())
async def track_edited_messages(event):
    if event.is_private and event.sender_id != admin_user_id:
        sender = await event.get_sender()
        if sender and getattr(sender, 'bot', False):
            return
        old = saved_messages_cache.get(event.id)
        old_text = old['text'] if old else "نامشخص"
        name = old['name'] if old else "کاربر ناشناس"
        await client.send_message(
            'me',
            f"✏️ پیام ویرایش شد\nفرستنده: {name}\nساعت: {event.date.strftime('%H:%M:%S')}\nمتن قبلی: {old_text}\nمتن جدید: {event.raw_text}"
        )
        saved_messages_cache[event.id] = {
            'text': event.raw_text,
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
    translator = Translator()
    translated = translator.translate(text, dest='en')
    await event.reply(translated.text)

@client.on(events.NewMessage(pattern='^(timename on|timename off|timepic on|timepic off|mini on|bio on|bio off|bold on|default on|mono on|rnd on|heart on|heart off|rname on|rname off|see rname|see bio|see lname|farsi on|fancy on|circle on)$'))
async def handle_settings(event):
    await settings(event)

@client.on(events.NewMessage(pattern='(?i)^(subscript on|زیرنویس)$'))
async def font_subscript(event):
    if event.sender_id != admin_user_id:
        return
    with open('settings/mode.txt', 'w') as f:
        f.write('Subscript')
    await event.reply("✅ فونت زیرنویس فعال شد.")

@client.on(events.NewMessage(pattern='(?i)^(double on|دبل)$'))
async def font_double(event):
    if event.sender_id != admin_user_id:
        return
    with open('settings/mode.txt', 'w') as f:
        f.write('DoubleStruck')
    await event.reply("✅ فونت دبل‌استراک فعال شد.")

@client.on(events.NewMessage(pattern='(?i)^(sansbold on|ساده_بولد)$'))
async def font_sansbold(event):
    if event.sender_id != admin_user_id:
        return
    with open('settings/mode.txt', 'w') as f:
        f.write('SansBold')
    await event.reply("✅ فونت ساده بولد فعال شد.")

@client.on(events.NewMessage(pattern='(?i)^(sans on|ساده)$'))
async def font_sans(event):
    if event.sender_id != admin_user_id:
        return
    with open('settings/mode.txt', 'w') as f:
        f.write('Sans')
    await event.reply("✅ فونت ساده فعال شد.")

@client.on(events.NewMessage(pattern='(?i)^(typewriter on|تایپ_رایتر)$'))
async def font_typewriter(event):
    if event.sender_id != admin_user_id:
        return
    with open('settings/mode.txt', 'w') as f:
        f.write('Typewriter')
    await event.reply("✅ فونت تایپ‌رایتر فعال شد.")

@client.on(events.NewMessage(pattern='(?i)^(اسپویلر روشن|spoiler on)$'))
async def spoiler_on(event):
    global spoiler_mode_enabled
    if event.sender_id != admin_user_id:
        return
    spoiler_mode_enabled = True
    await event.reply("✅ حالت اسپویلر فعال شد. از این به بعد «کپی به سیو» به‌صورت اسپویلر ارسال میشه.")

@client.on(events.NewMessage(pattern='(?i)^(اسپویلر خاموش|spoiler off)$'))
async def spoiler_off(event):
    global spoiler_mode_enabled
    if event.sender_id != admin_user_id:
        return
    spoiler_mode_enabled = False
    await event.reply("❌ حالت اسپویلر غیرفعال شد.")

@client.on(events.NewMessage(pattern='(?i)^(کپی به سیو|savecopy)$'))
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

@client.on(events.NewMessage(pattern='(?i)^(پنل|panel)$'))
async def show_panel(event):
    if event.sender_id == admin_user_id:
        text = """🎛 پنل مدیریت سلف

1️⃣ ضد حذف روشن/خاموش → بنویس: ضد حذف
2️⃣ ری‌لود ربات → بنویس: /reload
3️⃣ پینگ → بنویس: /ping
4️⃣ مصرف حافظه → بنویس: /mem
5️⃣ ترجمه به انگلیسی → بنویس: انگلیسیش کن
6️⃣ ترجمه به فارسی → بنویس: فارسیش کن
7️⃣ حذف اخیر گروه → بنویس: /rem [عدد]
8️⃣ تگ همه اعضا → بنویس: /tag
9️⃣ خروج از اکانت → بنویس: /logout
🔟 راهنمای کامل → بنویس: /راهنما"""
        await event.reply(text)

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
    translator = Translator()
    translated = translator.translate(text, dest='fa')
    await event.reply(translated.text)

daily_stats = {'messages_today': 0, 'unique_senders': set()}

@client.on(events.NewMessage)
async def track_daily_stats(event):
    if event.is_private and event.sender_id != admin_user_id:
        daily_stats['messages_today'] += 1
        daily_stats['unique_senders'].add(event.sender_id)

async def send_daily_report():
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

blocked_words = ["کص مادرت"]

@client.on(events.NewMessage)
async def auto_block_words(event):
    if event.is_private and event.sender_id != admin_user_id:
        text = event.raw_text.lower() if event.raw_text else ""
        for word in blocked_words:
            if word.lower() in text:
                await client(functions.contacts.BlockRequest(event.sender_id))
                await client.send_message(admin_user_id, f"🚫 کاربر {event.sender_id} به‌خاطر استفاده از کلمه ممنوعه بلاک شد.")
                break

@client.on(events.NewMessage(pattern='(?i)^(اضافه کلمه|addword) (.+)'))
async def add_blocked_word(event):
    if event.sender_id == admin_user_id:
        word = event.raw_text.split(' ', 1)[1].strip()
        blocked_words.append(word)
        await event.reply(f"✅ کلمه «{word}» به لیست ممنوعه اضافه شد.")

@client.on(events.NewMessage(pattern='(?i)^(لیست کلمات|listwords)$'))
async def list_blocked_words(event):
    if event.sender_id == admin_user_id:
        if blocked_words:
            await event.reply("🚫 کلمات ممنوعه:\n" + "\n".join(blocked_words))
        else:
            await event.reply("لیست خالیه.")

@client.on(events.NewMessage(pattern='(?i)^(ویس به متن|voicetotext)$'))
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

    ogg_path = await replied.download_media()
    wav_path = ogg_path.replace('.ogg', '.wav')
    AudioSegment.from_ogg(ogg_path).export(wav_path, format='wav')

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language='fa-IR')
        await event.reply(f"📝 متن ویس:\n\n{text}")
    except sr.UnknownValueError:
        await event.reply("متأسفانه نتونستم صدا رو تشخیص بدم.")
    except Exception as e:
        await event.reply(f"خطا: {e}")
    finally:
        os.remove(ogg_path)
        os.remove(wav_path)

@client.on(events.NewMessage(pattern='(?i)^(فال حافظ|falhafez)$'))
async def send_hafez_fortune(event):
    try:
        response = requests.get('https://hafez-dxle.onrender.com/fal')
        data = response.json()
        title = data.get('title', '')
        interpretation = data.get('interpreter', 'فالی پیدا نشد.')
        await event.reply(f"🔮 فال حافظ: {title}\n\n{interpretation}")
    except Exception as e:
        await event.reply(f"خطا در دریافت فال: {e}")

@client.on(events.NewMessage(pattern='(?i)^(بلاک|block)$'))
async def block_user(event):
    if event.sender_id != admin_user_id:
        return
    if not event.is_reply:
        await event.reply("روی پیام کاربر مدنظر ریپلای کنید.")
        return
    replied = await event.get_reply_message()
    target_id = replied.sender_id
    await client(functions.contacts.BlockRequest(target_id))
    await event.reply(f"🚫 کاربر {target_id} بلاک شد.")

@client.on(events.NewMessage(pattern='(?i)^(آنبلاک|unblock)$'))
async def unblock_user(event):
    if event.sender_id != admin_user_id:
        return
    if not event.is_reply:
        await event.reply("روی پیام کاربر مدنظر ریپلای کنید.")
        return
    replied = await event.get_reply_message()
    target_id = replied.sender_id
    await client(functions.contacts.UnblockRequest(target_id))
    await event.reply(f"✅ کاربر {target_id} آنبلاک شد.")

@client.on(events.NewMessage(pattern='(?i)^(حذف|delmsg)$'))
async def delete_replied_message(event):
    if event.sender_id != admin_user_id:
        return
    if not event.is_reply:
        await event.reply("روی پیامی که می‌خوای حذفش کنی ریپلای کن.")
        return
    replied = await event.get_reply_message()
    await replied.delete()
    await event.delete()

@client.on(events.NewMessage(pattern='(?i)^(گوست|ghost) (.+)$'))
async def ghost_read(event):
    if event.sender_id != admin_user_id:
        return
    target = event.pattern_match.group(2).strip()
    try:
        entity = await client.get_entity(target)
    except Exception:
        try:
            entity = await client.get_entity(int(target))
        except Exception as e:
            await event.reply(f"کاربر پیدا نشد: {e}")
            return

    dialog = None
    async for d in client.iter_dialogs():
        if d.entity.id == entity.id:
            dialog = d
            break

    if not dialog or dialog.unread_count == 0:
        await event.reply("پیام خونده‌نشده‌ای از این کاربر نیست.")
        return

    unread_count = dialog.unread_count
    messages = []
    async for msg in client.iter_messages(entity, limit=unread_count):
        messages.append(msg)
    messages.reverse()

    sender_name = getattr(entity, 'first_name', None) or getattr(entity, 'title', None) or str(entity.id)
    report = f"👻 پیام‌های خونده‌نشده از {sender_name}:\n\n"
    for msg in messages:
        text = msg.raw_text or "(رسانه بدون متن)"
        report += f"• {text}\n"

    await client.send_message('me', report)
    await event.reply("✅ پیام‌ها بدون Seen شدن ارسال شدن.")

@client.on(events.NewMessage(pattern='(?i)^(ghost on)$'))
async def ghost_mode_on_text(event):
    global ghost_mode_enabled
    if event.sender_id != admin_user_id:
        return
    ghost_mode_enabled = True
    await event.reply("👻 حالت مخفی‌کار فعال شد.")

@client.on(events.NewMessage(pattern='(?i)^(ghost off)$'))
async def ghost_mode_off_text(event):
    global ghost_mode_enabled
    if event.sender_id != admin_user_id:
        return
    ghost_mode_enabled = False
    await event.reply("👁 حالت مخفی‌کار غیرفعال شد.")

watch_keywords = []

@client.on(events.NewMessage(pattern='(?i)^(اضافه کلمه دیده‌بان|addwatch) (.+)$'))
async def add_watch_keyword(event):
    if event.sender_id != admin_user_id or not event.is_private:
        return
    keyword = event.pattern_match.group(2).strip()
    watch_keywords.append(keyword.lower())
    await event.reply(f"👁 کلمه «{keyword}» به لیست دیده‌بانی اضافه شد.")

@client.on(events.NewMessage(pattern='(?i)^(حذف کلمه دیده‌بان|delwatch) (.+)$'))
async def remove_watch_keyword(event):
    if event.sender_id != admin_user_id or not event.is_private:
        return
    keyword = event.pattern_match.group(2).strip().lower()
    if keyword in watch_keywords:
        watch_keywords.remove(keyword)
        await event.reply(f"✅ کلمه «{keyword}» از لیست دیده‌بانی حذف شد.")
    else:
        await event.reply("این کلمه توی لیست نبود.")

@client.on(events.NewMessage(pattern='(?i)^(لیست دیده‌بان|listwatch)$'))
async def list_watch_keywords(event):
    if event.sender_id == admin_user_id and event.is_private:
        if watch_keywords:
            await event.reply("👁 کلمات دیده‌بانی:\n" + "\n".join(watch_keywords))
        else:
            await event.reply("لیست خالیه.")

@client.on(events.NewMessage)
async def group_watcher(event):
    if event.sender_id != admin_user_id and event.raw_text and watch_keywords:
        text_lower = event.raw_text.lower()
        for keyword in watch_keywords:
            if keyword in text_lower:
                chat = await event.get_chat()
                sender = await event.get_sender()
                sender_name = sender.first_name if sender and sender.first_name else "ناشناس"
                chat_name = getattr(chat, 'title', None) or getattr(chat, 'first_name', 'خصوصی')
                await client.send_message(
                    admin_user_id,
                    f"👁 کلمه دیده‌بانی «{keyword}» شنیده شد!\n\n📍 چت: {chat_name}\n👤 فرستنده: {sender_name}\n💬 متن: {event.raw_text}"
                )
                break

@client.on(events.NewMessage(pattern='(?i)^(اعلام وضعیت|status)$'))
async def show_status(event):
    if event.sender_id != admin_user_id:
        return
    def read_status(path):
        try:
            with open(path, 'r') as f:
                return f.read().strip()
        except:
            return "نامشخص"
    timename = "🟢 روشن" if read_status('settings/time.txt') == 'True' else "🔴 خاموش"
    timepic = "🟢 روشن" if read_status('settings/timepic.txt') == 'True' else "🔴 خاموش"
    bio = "🟢 روشن" if read_status('settings/bioinfo.txt') == 'True' else "🔴 خاموش"
    heart = "🟢 روشن" if read_status('settings/heart.txt') == 'True' else "🔴 خاموش"
    rname = "🟢 روشن" if read_status('settings/rnamest.txt') == 'True' else "🔴 خاموش"
    mode = read_status('settings/mode.txt')
    ghost = "🟢 روشن" if ghost_mode_enabled else "🔴 خاموش"
    spoiler = "🟢 روشن" if spoiler_mode_enabled else "🔴 خاموش"
    status_lines = []
    status_lines.append("📊 وضعیت کامل سلف")
    status_lines.append("")
    status_lines.append("⚙️ تنظیمات پروفایل")
    status_lines.append(f"🕐 زمان در اسم: {timename}")
    status_lines.append(f"🖼 زمان در عکس: {timepic}")
    status_lines.append(f"📝 بیو پویا: {bio}")
    status_lines.append(f"❤️ حالت قلب: {heart}")
    status_lines.append(f"🎲 اسم رندوم: {rname}")
    status_lines.append(f"🔤 فونت فعلی: {mode}")
    status_lines.append("")
    status_lines.append("🔒 امنیت")
    status_lines.append(f"👻 حالت مخفی: {ghost}")
    status_lines.append(f"🫥 حالت اسپویلر: {spoiler}")
    status_lines.append(f"🗑 چت‌های ضد حذف فعال: {len(anti_delete_chats)}")
    status_lines.append(f"🚫 تعداد کلمات ممنوعه: {len(blocked_words)}")
    status_lines.append(f"👁 تعداد کلمات دیده‌بان: {len(watch_keywords)}")
    status_lines.append("")
    status_lines.append("📊 آمار امروز")
    status_lines.append(f"📨 پیام‌های دریافتی: {daily_stats['messages_today']}")
    status_lines.append(f"👥 کاربران متفاوت: {len(daily_stats['unique_senders'])}")
    status_lines.append("")
    status_lines.append("ℹ️ سیستم")
    status_lines.append(f"💾 مصرف حافظه: {psutil.virtual_memory().percent}%")
    await event.reply("\n".join(status_lines))

@bot_client.on(events.InlineQuery)
async def bot_inline_panel(event):
    if event.sender_id != admin_user_id:
        await event.answer([])
        return
    builder = event.builder
    result = builder.article(
        title="🎛 باز کردن پنل مدیریت سلف",
        description="برای باز کردن پنل کامل اینجا کلیک کن",
        text="🎛 پنل مدیریت سلف\nیه دسته رو انتخاب کنید:",
        buttons=[
            [Button.inline("⚙️ تنظیمات پروفایل", b"menu_settings"), Button.inline("🔤 فونت‌ها", b"menu_fonts")],
            [Button.inline("🗑 مدیریت پیام", b"menu_msg"), Button.inline("🔒 امنیت", b"menu_security")],
            [Button.inline("👻 حالت مخفی", b"menu_ghost"), Button.inline("🔮 سرگرمی", b"menu_fun")],
            [Button.inline("📊 آمار", b"menu_stats"), Button.inline("ℹ️ سیستم", b"menu_system")],
        ]
    )
    await event.answer([result])

@bot_client.on(events.NewMessage(pattern='(?i)^(/panel|/start)$'))
async def bot_show_panel(event):
    if event.sender_id != admin_user_id:
        return
    buttons = [
        [Button.inline("⚙️ تنظیمات پروفایل", b"menu_settings"), Button.inline("🔤 فونت‌ها", b"menu_fonts")],
        [Button.inline("🗑 مدیریت پیام", b"menu_msg"), Button.inline("🔒 امنیت", b"menu_security")],
        [Button.inline("👻 حالت مخفی", b"menu_ghost"), Button.inline("🔮 سرگرمی", b"menu_fun")],
        [Button.inline("📊 آمار", b"menu_stats"), Button.inline("ℹ️ سیستم", b"menu_system")],
    ]
    await event.reply("🎛 پنل مدیریت سلف\nیه دسته رو انتخاب کنید:", buttons=buttons)

@bot_client.on(events.CallbackQuery)
async def bot_handle_clicks(event):
    global ghost_mode_enabled, spoiler_mode_enabled
    if event.sender_id != admin_user_id:
        return
    data = event.data.decode('utf-8')

    if data == "menu_settings":
        buttons = [
            [Button.inline("🟢 زمان در اسم روشن", b"p_timename_on"), Button.inline("🔴 زمان در اسم خاموش", b"p_timename_off")],
            [Button.inline("🟢 زمان در عکس روشن", b"p_timepic_on"), Button.inline("🔴 زمان در عکس خاموش", b"p_timepic_off")],
            [Button.inline("🟢 بیو پویا روشن", b"p_bio_on"), Button.inline("🔴 بیو پویا خاموش", b"p_bio_off")],
            [Button.inline("🟢 قلب روشن", b"p_heart_on"), Button.inline("🔴 قلب خاموش", b"p_heart_off")],
            [Button.inline("🟢 اسم رندوم روشن", b"p_rname_on"), Button.inline("🔴 اسم رندوم خاموش", b"p_rname_off")],
            [Button.inline("🔙 برگشت", b"menu_main")],
        ]
        await event.edit("⚙️ تنظیمات پروفایل", buttons=buttons)

    elif data == "menu_fonts":
        buttons = [
            [Button.inline("🔵 بولد", b"p_font_bold"), Button.inline("🔵 مونو", b"p_font_mono")],
            [Button.inline("🔵 مینی", b"p_font_mini"), Button.inline("🔵 فارسی", b"p_font_farsi")],
            [Button.inline("🔵 فانتزی", b"p_font_fancy"), Button.inline("🔵 دایره‌ای", b"p_font_circle")],
            [Button.inline("✨ زیرنویس", b"p_font_subscript"), Button.inline("✨ دبل‌استراک", b"p_font_double")],
            [Button.inline("✨ ساده‌بولد", b"p_font_sansbold"), Button.inline("✨ ساده", b"p_font_sans")],
            [Button.inline("✨ تایپ‌رایتر", b"p_font_typewriter"), Button.inline("🔵 رندوم", b"p_font_rnd")],
            [Button.inline("🔵 پیش‌فرض", b"p_font_default")],
            [Button.inline("🔙 برگشت", b"menu_main")],
        ]
        await event.edit("🔤 فونت‌های ساعت", buttons=buttons)

    elif data == "menu_msg":
        buttons = [
            [Button.inline("🟢 ضد حذف روشن", b"p_antidelete_on"), Button.inline("🔴 ضد حذف خاموش", b"p_antidelete_off")],
            [Button.inline("🔵 تعداد چت‌های ضد حذف", b"p_antidelete_list")],
            [Button.inline("🔙 برگشت", b"menu_main")],
        ]
        await event.edit("🗑 مدیریت پیام", buttons=buttons)

    elif data == "menu_security":
        buttons = [
            [Button.inline("🚫 بلاک کاربر", b"p_block_start"), Button.inline("✅ آنبلاک کاربر", b"p_unblock_start")],
            [Button.inline("🔵 لیست کلمات ممنوعه", b"p_words_list")],
            [Button.inline("🔵 لیست کلمات دیده‌بان", b"p_watch_list")],
            [Button.inline("🔙 برگشت", b"menu_main")],
        ]
        await event.edit("🔒 امنیت", buttons=buttons)

    elif data == "menu_ghost":
        buttons = [
            [Button.inline("🟢 گوست روشن", b"p_ghost_on"), Button.inline("🔴 گوست خاموش", b"p_ghost_off")],
            [Button.inline("🟢 اسپویلر روشن", b"p_spoiler_on"), Button.inline("🔴 اسپویلر خاموش", b"p_spoiler_off")],
            [Button.inline("🔙 برگشت", b"menu_main")],
        ]
        await event.edit("👻 حالت مخفی و اسپویلر", buttons=buttons)

    elif data == "menu_fun":
        buttons = [
            [Button.inline("🔮 فال حافظ بگیر", b"p_hafez")],
            [Button.inline("🔙 برگشت", b"menu_main")],
        ]
        await event.edit("🔮 سرگرمی", buttons=buttons)

    elif data == "menu_stats":
        buttons = [
            [Button.inline("📊 آمار امروز", b"p_stats_today"), Button.inline("💾 مصرف حافظه", b"p_mem")],
            [Button.inline("🔙 برگشت", b"menu_main")],
        ]
        await event.edit("📊 آمار و گزارش", buttons=buttons)

    elif data == "menu_system":
        buttons = [
            [Button.inline("📊 پینگ", b"p_ping"), Button.inline("🔄 ری‌لود", b"p_reload")],
            [Button.inline("🔴 خروج از اکانت", b"p_logout_confirm")],
            [Button.inline("🔙 برگشت", b"menu_main")],
        ]
        await event.edit("ℹ️ سیستم", buttons=buttons)

    elif data == "menu_main":
        buttons = [
            [Button.inline("⚙️ تنظیمات پروفایل", b"menu_settings"), Button.inline("🔤 فونت‌ها", b"menu_fonts")],
            [Button.inline("🗑 مدیریت پیام", b"menu_msg"), Button.inline("🔒 امنیت", b"menu_security")],
            [Button.inline("👻 حالت مخفی", b"menu_ghost"), Button.inline("🔮 سرگرمی", b"menu_fun")],
            [Button.inline("📊 آمار", b"menu_stats"), Button.inline("ℹ️ سیستم", b"menu_system")],
        ]
        await event.edit("🎛 پنل مدیریت سلف\nیه دسته رو انتخاب کنید:", buttons=buttons)

    elif data == "p_timename_on":
        with open('settings/time.txt', 'w') as f:
            f.write('True')
        await client(UpdateProfileRequest(last_name=f'{current_time_str}'))
        await event.answer("✅ زمان در اسم فعال شد", alert=True)
    elif data == "p_timename_off":
        with open('settings/time.txt', 'w') as f:
            f.write('False')
        await client(UpdateProfileRequest(last_name=''))
        await event.answer("❌ زمان در اسم غیرفعال شد", alert=True)
    elif data == "p_timepic_on":
        with open('settings/timepic.txt', 'w') as f:
            f.write('True')
        await event.answer("✅ زمان در عکس فعال شد", alert=True)
    elif data == "p_timepic_off":
        with open('settings/timepic.txt', 'w') as f:
            f.write('False')
        await event.answer("❌ زمان در عکس غیرفعال شد", alert=True)
    elif data == "p_bio_on":
        with open('settings/bioinfo.txt', 'w') as f:
            f.write('True')
        await event.answer("✅ بیو پویا فعال شد", alert=True)
    elif data == "p_bio_off":
        with open('settings/bioinfo.txt', 'w') as f:
            f.write('False')
        await client(UpdateProfileRequest(about=''))
        await event.answer("❌ بیو پویا غیرفعال شد", alert=True)
    elif data == "p_heart_on":
        with open('settings/heart.txt', 'w') as f:
            f.write('True')
        await event.answer("✅ قلب فعال شد", alert=True)
    elif data == "p_heart_off":
        with open('settings/heart.txt', 'w') as f:
            f.write('False')
        await event.answer("❌ قلب غیرفعال شد", alert=True)
    elif data == "p_rname_on":
        with open('settings/rnamest.txt', 'w') as f:
            f.write('True')
        await event.answer("✅ اسم رندوم فعال شد", alert=True)
    elif data == "p_rname_off":
        with open('settings/rnamest.txt', 'w') as f:
            f.write('False')
        await event.answer("❌ اسم رندوم غیرفعال شد", alert=True)

    elif data == "p_font_bold":
        with open('settings/mode.txt', 'w') as f:
            f.write('Bold')
        await event.answer("✅ فونت بولد فعال شد", alert=True)
    elif data == "p_font_mono":
        with open('settings/mode.txt', 'w') as f:
            f.write('Mono')
        await event.answer("✅ فونت مونو فعال شد", alert=True)
    elif data == "p_font_mini":
        with open('settings/mode.txt', 'w') as f:
            f.write('Mini')
        await event.answer("✅ فونت مینی فعال شد", alert=True)
    elif data == "p_font_farsi":
        with open('settings/mode.txt', 'w') as f:
            f.write('Farsi')
        await event.answer("✅ فونت فارسی فعال شد", alert=True)
    elif data == "p_font_fancy":
        with open('settings/mode.txt', 'w') as f:
            f.write('Fancy')
        await event.answer("✅ فونت فانتزی فعال شد", alert=True)
    elif data == "p_font_circle":
        with open('settings/mode.txt', 'w') as f:
            f.write('Circle')
        await event.answer("✅ فونت دایره‌ای فعال شد", alert=True)
    elif data == "p_font_subscript":
        with open('settings/mode.txt', 'w') as f:
            f.write('Subscript')
        await event.answer("✅ فونت زیرنویس فعال شد", alert=True)
    elif data == "p_font_double":
        with open('settings/mode.txt', 'w') as f:
            f.write('DoubleStruck')
        await event.answer("✅ فونت دبل‌استراک فعال شد", alert=True)
    elif data == "p_font_sansbold":
        with open('settings/mode.txt', 'w') as f:
            f.write('SansBold')
        await event.answer("✅ فونت ساده بولد فعال شد", alert=True)
    elif data == "p_font_sans":
        with open('settings/mode.txt', 'w') as f:
            f.write('Sans')
        await event.answer("✅ فونت ساده فعال شد", alert=True)
    elif data == "p_font_typewriter":
        with open('settings/mode.txt', 'w') as f:
            f.write('Typewriter')
        await event.answer("✅ فونت تایپ‌رایتر فعال شد", alert=True)
    elif data == "p_font_default":
        with open('settings/mode.txt', 'w') as f:
            f.write('Default')
        await event.answer("✅ فونت پیش‌فرض فعال شد", alert=True)
    elif data == "p_font_rnd":
        with open('settings/mode.txt', 'w') as f:
            f.write('rnd')
        await event.answer("✅ فونت رندوم فعال شد", alert=True)

    elif data == "p_antidelete_on":
        anti_delete_chats.add(event.chat_id)
        await event.answer("✅ ضد حذف فعال شد", alert=True)
    elif data == "p_antidelete_off":
        anti_delete_chats.discard(event.chat_id)
        await event.answer("❌ ضد حذف غیرفعال شد", alert=True)
    elif data == "p_antidelete_list":
        await event.answer(f"🗑 چت‌های ضد حذف فعال: {len(anti_delete_chats)}", alert=True)

    elif data == "p_ghost_on":
        ghost_mode_enabled = True
        await event.answer("✅ گوست مود فعال شد", alert=True)
    elif data == "p_ghost_off":
        ghost_mode_enabled = False
        await event.answer("❌ گوست مود غیرفعال شد", alert=True)
    elif data == "p_spoiler_on":
        spoiler_mode_enabled = True
        await event.answer("✅ اسپویلر فعال شد", alert=True)
    elif data == "p_spoiler_off":
        spoiler_mode_enabled = False
        await event.answer("❌ اسپویلر غیرفعال شد", alert=True)

    elif data == "p_words_list":
        words_text = "\n".join(blocked_words) if blocked_words else "خالی"
        await event.answer(words_text[:200], alert=True)
    elif data == "p_watch_list":
        watch_text = "\n".join(watch_keywords) if watch_keywords else "خالی"
        await event.answer(watch_text[:200], alert=True)

    elif data == "p_block_start":
        pending_input[admin_user_id] = "block"
        await event.answer("آیدی عددی یا یوزرنیم کاربر رو همینجا (توی همین چت با ربات) بفرست", alert=True)
    elif data == "p_unblock_start":
        pending_input[admin_user_id] = "unblock"
        await event.answer("آیدی عددی یا یوزرنیم کاربر رو همینجا (توی همین چت با ربات) بفرست", alert=True)

    elif data == "p_hafez":
        try:
            response = requests.get('https://hafez-dxle.onrender.com/fal')
            hdata = response.json()
            interpretation = hdata.get('interpreter', 'فالی پیدا نشد.')
            await event.answer(interpretation[:200], alert=True)
        except Exception as e:
            await event.answer(f"خطا: {e}", alert=True)

    elif data == "p_stats_today":
        msg = f"📨 پیام‌ها: {daily_stats['messages_today']}\n👥 کاربران: {len(daily_stats['unique_senders'])}"
        await event.answer(msg, alert=True)
    elif data == "p_mem":
        mem_usage = psutil.virtual_memory().percent
        await event.answer(f"💾 مصرف حافظه: {mem_usage}%", alert=True)
    elif data == "p_ping":
        await event.answer("🏓 سلف روشن و پاسخگوئه", alert=True)
    elif data == "p_reload":
        await client.send_message('me', 'در حال ری‌لود توسط پنل...')
        os.execv(sys.executable, ['python'] + sys.argv)
    elif data == "p_logout_confirm":
        await event.answer("⚠️ برای خروج واقعی، دستور /logout رو مستقیم به سلف بزنید. این دکمه فقط هشداره.", alert=True)
    else:
        await event.answer("این گزینه فعلاً فقط راهنماست.", alert=True)

@bot_client.on(events.NewMessage)
async def bot_handle_pending_input(event):
    if event.sender_id != admin_user_id:
        return
    if event.raw_text and event.raw_text.startswith('/'):
        return
    action = pending_input.get(admin_user_id)
    if not action:
        return
    target = event.raw_text.strip()
    try:
        entity = await client.get_entity(target)
    except Exception:
        try:
            entity = await client.get_entity(int(target))
        except Exception as e:
            await event.reply(f"کاربر پیدا نشد: {e}")
            pending_input[admin_user_id] = None
            return

    if action == "block":
        await client(functions.contacts.BlockRequest(entity.id))
        await event.reply(f"🚫 کاربر {target} بلاک شد.")
    elif action == "unblock":
        await client(functions.contacts.UnblockRequest(entity.id))
        await event.reply(f"✅ کاربر {target} آنبلاک شد.")

    pending_input[admin_user_id] = None

scheduled_jobs = {}

async def run_scheduled_job(job_id, target, text, minutes):
    while True:
        await asyncio.sleep(minutes * 60)
        try:
            await client.send_message(target, text)
        except Exception as e:
            await client.send_message(admin_user_id, f"⚠️ خطا در زمانبند #{job_id}: {e}")

@client.on(events.NewMessage(pattern='(?i)^زمانبند (\d+) (.+)$'))
async def start_scheduled_post(event):
    if event.sender_id != admin_user_id:
        return
    if not event.is_reply:
        await event.reply("روی متنی که می‌خوای تکرار بشه ریپلای کن، بعد بنویس:\nزمانبند [دقیقه] [آیدی یا یوزرنیم گروه]")
        return
    minutes = int(event.pattern_match.group(1))
    target = event.pattern_match.group(2).strip()
    replied = await event.get_reply_message()
    text_to_send = replied.raw_text
    if not text_to_send:
        await event.reply("پیامی که روش ریپلای کردید متن نداره.")
        return
    try:
        entity = await client.get_entity(target)
    except Exception:
        try:
            entity = await client.get_entity(int(target))
        except Exception as e:
            await event.reply(f"گروه پیدا نشد: {e}")
            return
    job_id = (max(scheduled_jobs.keys()) + 1) if scheduled_jobs else 1
    task = client.loop.create_task(run_scheduled_job(job_id, entity, text_to_send, minutes))
    scheduled_jobs[job_id] = {'task': task, 'target': target, 'minutes': minutes, 'text': text_to_send}
    await event.reply(f"✅ زمانبند #{job_id} فعال شد: هر {minutes} دقیقه به {target}")

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
    job_id = int(event.pattern_match.group(1))
    job = scheduled_jobs.get(job_id)
    if not job:
        await event.reply("همچین زمانبندی وجود نداره.")
        return
    job['task'].cancel()
    del scheduled_jobs[job_id]
    await event.reply(f"✅ زمانبند #{job_id} حذف شد.")

client.start()
bot_client.start(bot_token=bot_token)
client.loop.create_task(update_first_name())
client.loop.create_task(update_last_name())
client.loop.create_task(update_about())
client.loop.create_task(update_profile_photo())
client.loop.create_task(send_daily_report())
client.loop.create_task(bot_client.run_until_disconnected())
client.loop.run_until_complete(send_welcome_message())
client.run_until_disconnected()
