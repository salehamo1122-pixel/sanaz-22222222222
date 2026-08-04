from .library import *
from .Information import *
from .updater import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ============= تنظیمات Spotify =============
# اگه نداره، این بخش رو کامنت کن
try:
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
except:
    sp = None

# ============= توابع کمکی =============
def get_current_time_str():
    return datetime.datetime.now().strftime("%H:%M")

def clear_pic_folder():
    pic_folder = 'pic/'
    if os.path.exists(pic_folder):
        for file in os.listdir(pic_folder):
            os.remove(os.path.join(pic_folder, file))

# ============= دستورات =============
async def send_welcome_message():
    try:
        admin_user = await client.get_entity(admin_user_id)
        admin_first_name = admin_user.first_name if admin_user.first_name else "there"
        await client.send_message(admin_user_id, f'سلام و عرض احترام {admin_first_name}\nساخته شده به دست saleh681@\nقوانین را رعایت کنید تا از طرف تلگرام بن نشید')
    except Exception as e:
        print(f"Error in send_welcome_message: {e}")

def set_user_bio(bio):
    with open('settings/bio.txt', 'w') as f:
        f.write(bio)

def set_user_lname(lname):
    with open('settings/nameinfo.txt', 'w') as f:
        f.write(lname)

def get_user_bio():
    with open('settings/bio.txt', 'r') as f:
        return f.read().strip()

async def download_and_send(audio_url, event, title, artist, views, release_date, url):
    try:
        response = urllib.request.urlopen(audio_url)
        audio_file = io.BytesIO(response.read())
        audio_file.name = f"{title}.mp3"
        caption = f"{title} - {artist}\nViews: {views} k\nRelease date: {release_date}\nLink: {url}\n\n**Note: Due to the copyright law, we can only show you 30 seconds of music here, I hope you understand us**"
        await client.send_file(event.chat_id, audio_file, caption=caption)
    except Exception as e:
        await event.reply(f"Failed to send audio: {str(e)}")

def load_admins():
    try:
        with open('settings/admin.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_admins(admins):
    with open('settings/admin.json', 'w') as file:
        json.dump(admins, file)

def generate_random_filename():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(10))

def find_matching_filename(message):
    SAVE_FOLDER = 'save'
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
    for file in os.listdir(SAVE_FOLDER):
        if message.lower() == os.path.splitext(file)[0].lower():
            return os.path.join(SAVE_FOLDER, file)
    return None

fast_replies_file = 'settings/fast_replies.json'

def load_fast_replies():
    try:
        with open(fast_replies_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_fast_replies(fast_replies):
    with open(fast_replies_file, 'w') as f:
        json.dump(fast_replies, f, indent=4)

def get_uptime(start_time):
    now = datetime.datetime.now()
    uptime = now - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} days {hours} hours {minutes} minutes {seconds} seconds"

start_time = datetime.datetime.now()

async def start_command(event):
    if event.sender_id == admin_user_id:
        uptime = get_uptime(start_time)
        message = f"**Bot is online:)\nUptime is: {uptime}**"
        await event.edit(message)

async def ping(event):
    if event.sender_id == admin_user_id:
        start_time = datetime.datetime.now()
        await event.delete()
        message = await event.respond('Pong!')
        end_time = datetime.datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        user_link = f'❈[I Never Lose](tg://user?id={admin_user_id})'
        await message.edit(f'**{user_link} ! Response time: {response_time:.2f} ms**')

async def mem(event):
    if event.sender_id == admin_user_id:
        memory = psutil.virtual_memory().percent
        await event.edit(f'**❈MEMORY USAGE: {memory}%**')

MSAVE_DIRECTORY = 'music'

async def sc(event):
    if event.sender_id == admin_user_id:
        if sp is None:
            await event.edit("**❈ Spotify service is not available. Please install spotipy.**")
            return
        
        query = event.raw_text[7:]  # Adjust the index to match '/gmusic '
        try:
            results = sp.search(q=query, type='track')
            tracks = results.get('tracks', {}).get('items', [])
            
            if tracks:
                track = tracks[0]
                title = track.get('name', '')
                artist = track.get('artists', [{}])[0].get('name', '')
                url = track.get('external_urls', {}).get('spotify', '')
                views = track.get('popularity', '')
                release_date = track.get('album', {}).get('release_date', '')
                
                await event.delete()
                await download_and_send(track, event, title, artist, views, release_date, url)
            else:
                await event.edit(f'**❈Sorry, no results found.**')
        except Exception as e:
            await event.edit(f'**❈Error: {str(e)}**')

async def download_and_send(track, event, title, artist, views, release_date, url):
    try:
        audio_url = track.get('preview_url')
        
        if audio_url:
            if not os.path.exists(MSAVE_DIRECTORY):
                os.makedirs(MSAVE_DIRECTORY)
            
            audio_file_path = os.path.join(MSAVE_DIRECTORY, f'{title}.mp3')
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url) as resp:
                    if resp.status == 200:
                        with open(audio_file_path, 'wb') as file:
                            while True:
                                chunk = await resp.content.read(1024)
                                if not chunk:
                                    break
                                file.write(chunk)
                        
                        await event.reply(
                            file=audio_file_path,
                            message=f"**❈Title: {title}\nArtist: {artist}\nViews: {views} K\nRelease Date: {release_date}\n[Listen on Spotify]({url})**",
                        )
                        
                        os.remove(audio_file_path)
                    else:
                        await event.reply(f"Failed to download: Status {resp.status}")
        else:
            await event.reply(f"No audio preview available.")
    
    except Exception as e:
        await event.reply(f"Failed: {str(e)}")

async def tarikh(event):
    if event.sender_id == admin_user_id:
        try:
            jalali_date = JalaliDate.today().strftime('%A %d %B %Y')
            await event.edit(f'**❈ Today is: {jalali_date}**')
        except Exception as e:
            await event.reply(f"Failed to retrieve date: {str(e)}")

async def gmsg(event):
    if event.sender_id == admin_user_id:
        try:
            await event.delete()
            processing_message = await event.respond("Processing your message...")

            msg = event.raw_text[6:]
            for i in range(len(msg)):
                await processing_message.edit(f"{msg[:i+1]}")
                await asyncio.sleep(0.3)

            await processing_message.edit(f"{msg} 💚")
        except Exception as e:
            await event.reply(f"Failed to process message: {str(e)}")

async def weather(event):
    if event.sender_id == admin_user_id:
        try:
            location = event.raw_text[9:]
            url = f'https://wttr.in/{location}?format=%C\n%t\n%h\n'
            response = requests.get(url)

            if response.status_code == 200:
                weather_data = response.text.split('\n')
                condition = weather_data[0] if len(weather_data) > 0 else "نامشخص"
                temperature = weather_data[1] if len(weather_data) > 1 else "نامشخص"
                humidity = weather_data[2] if len(weather_data) > 2 else "نامشخص"

                message = f'**❈ Current weather in {location}:**\n\nCondition: {condition}\nTemperature: {temperature}\nHumidity: {humidity}'
                await event.edit(message)
            else:
                await event.reply('**❈ Sorry, there was an error retrieving the weather information.**')
        except Exception as e:
            await event.reply(f'Failed to fetch weather: {str(e)}')

async def rsong(event):
    if event.sender_id == admin_user_id:
        try:
            channel = '@LiMuTa'
            limit = 100
            messages = await client.get_messages(channel, limit=limit)
            
            audio_messages = [
                m for m in messages 
                if hasattr(m, 'media') 
                and hasattr(m.media, 'document') 
                and m.media.document.mime_type == 'audio/mpeg'
            ]
            
            if audio_messages:
                random_audio_message = random.choice(audio_messages)
                await client.forward_messages(event.chat_id, random_audio_message)
                await event.edit('**❈ Your random song has been sent!**')
                await asyncio.sleep(0.5)
                await client.delete_messages(event.chat_id, event.id)
            else:
                await event.respond('**❈ No audio messages found.**')
        except Exception as e:
            await event.respond(f'Failed to retrieve and send random song: {str(e)}')

async def info(event):
    if event.sender_id == admin_user_id:
        try:
            username = event.text[6:].strip()

            if username:
                user = await client.get_entity(username)

                if isinstance(user, User):
                    photo = await client.download_profile_photo(user)

                    if photo and os.path.exists(photo):
                        caption = f"Id: {user.id}\nFirst: {user.first_name}\nUsername: @{user.username}"
                        await event.reply(file=photo, message=caption)
                        os.remove(photo)
                    else:
                        await event.edit("**❈ Failed to download the profile picture.**")
                else:
                    await event.edit('**❈ Username belongs to a channel or group.**')
            else:
                await event.edit('❈ Please provide a username.')

        except ValueError:
            await event.edit('**❈ Invalid username provided.**')
        except Exception as e:
            await event.edit(f'Failed to retrieve user info: {str(e)}')

async def set_profile_pic(event):
    if event.sender_id == admin_user_id:    
        if event.is_reply:
            try:
                reply = await event.get_reply_message()

                if reply.photo:
                    photo = await client.download_media(reply.photo)

                    if photo and os.path.exists(photo):
                        with open(photo, 'rb') as f:
                            uploaded_file = await client.upload_file(photo)
                            await client(functions.photos.UploadProfilePhotoRequest(file=uploaded_file))

                        os.remove(photo)
                        await event.edit(f'**❈ [Profile](tg://user?id={admin_user_id}) picture updated successfully!**')
                    else:
                        await event.edit('**❈ Failed to download photo.**')
                else:
                    await event.edit('**❈ Please reply to a photo to set as your profile picture.**')

            except Exception as e:
                await event.respond(f'**❈ Error updating profile picture: {str(e)}**')
        else:
            await event.edit('**❈ Please reply to a photo to set as your profile picture.**')

async def delete_profile_pic(event):
    if event.sender_id == admin_user_id:
        try:
            photos = await client.get_profile_photos('me')
            
            if photos and len(photos) > 0:
                await client(functions.photos.DeletePhotosRequest(id=[InputPhoto(id=photos[0].id, access_hash=photos[0].access_hash, file_reference=photos[0].file_reference)]))
                await event.edit(f'**❈ [Profile](tg://user?id={admin_user_id}) picture deleted successfully!**')
            else:
                await event.edit('**❈ No profile photos found to delete.**')
        
        except Exception as e:
            await event.edit(f'**❈ Error deleting profile picture: {str(e)}**')

async def rinfo(event):
    if event.sender_id == admin_user_id:
        try:
            await event.delete()
            if event.is_reply:
                reply = await event.get_reply_message()

                if reply.sender_id:
                    user = await client.get_entity(reply.sender_id)

                    if isinstance(user, types.User):
                        user_full = await client(functions.users.GetFullUserRequest(user.id))
                        user_info = await client(functions.users.GetUsersRequest([user.id]))
                        user_status = user_info[0].status

                        if isinstance(user_status, types.UserStatusOnline):
                            last_seen = "آنلاین"
                        elif isinstance(user_status, types.UserStatusOffline):
                            last_seen = user_status.was_online.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            last_seen = "اخیرا"

                        common_chats = await client(functions.messages.GetCommonChatsRequest(user_id=user.id, max_id=0, limit=10))
                        groups_count = len(common_chats.chats)

                        bio = user_full.about if hasattr(user_full, 'about') and user_full.about else "ندارد"

                        photos = await client(functions.photos.GetUserPhotosRequest(user_id=user.id, offset=0, max_id=0, limit=0))
                        profile_count = len(photos.photos) if photos and photos.photos else 0

                        info_text = (
                            f"نام: ({user.first_name})\nشناسه: (`{user.id}`)\nنام کاربری: (@{user.username})\nشماره: (***********)\nتعداد پروفایل: ({profile_count})\nوضعیت: ({last_seen})\nگروه‌ها: ({groups_count})\n\nبیوگرافی: ({bio})"
                        )

                        if photos and len(photos.photos) > 0:
                            await client.send_file(event.chat_id, file=photos.photos[0], caption=info_text)
                        else:
                            await client.send_message(event.chat_id, info_text)

                    elif isinstance(user, types.Channel):
                        info_text = f"Id: {user.id}\nTitle: {user.title}\nUsername: {user.username}\nDescription: {user.description}"
                        await client.send_message(event.chat_id, info_text)

                else:
                    await client.send_message(event.chat_id, '**❈ The replied message does not have a sender.**')
            else:
                await client.send_message(event.chat_id, '**❈ Please reply to a message to get its sender information.**')
        except Exception as e:
            await client.send_message(event.chat_id, f'❈ Error getting information: {str(e)}')

async def delete_recent_messages(event):
    if event.sender_id == admin_user_id:
        try:
            parts = event.text.split()
            if len(parts) < 2:
                await event.respond('**❈ Please specify a number. Example: /rem 10**')
                return
                
            num = int(parts[1])

            if num > 50:
                await event.respond('**❈ Sorry, you can only delete up to 50 messages at a time.**')
                return

            messages = await client.get_messages(event.chat_id, limit=num)

            if not messages:
                await event.respond('**❈ No messages found to delete.**')
                return

            await client.delete_messages(entity=event.chat_id, message_ids=[msg.id for msg in messages], revoke=True)
            await event.respond(f'**❈ {num} messages deleted successfully!**')

        except ValueError:
            await event.respond('**❈ Please specify a valid number of messages to delete.**')
        except Exception as e:
            await event.respond(f'**❈ Error deleting messages: {str(e)}**')

# ... ادامه بقیه توابع ...

# ============= بخش تنظیمات اصلاح‌شده =============
patterns_actions = {
    'timename on': ('settings/time.txt', 'True', '**❈Time Name Activated!**'),
    'timename off': ('settings/time.txt', 'False', '**❈Time Name DeActivated!**'),
    'timepic on': ('settings/timepic.txt', 'True', '**❈Time Pic Activated!**'),
    'timepic off': ('settings/timepic.txt', 'False', '**❈Time Pic DeActivated!**'),
    'bio on': ('settings/bioinfo.txt', 'True', '**❈Bio Activated!**'),
    'bio off': ('settings/bioinfo.txt', 'False', '**❈Bio DeActivated!**'),
    'bold on': ('settings/mode.txt', 'Bold', '**❈Bold Mode Activated!**'),
    'mini on': ('settings/mode.txt', 'Mini', '**❈Mini Mode Activated!**'),
    'rnd on': ('settings/mode.txt', 'rnd', '**❈Rnd Mode Activated!**'),
    'default on': ('settings/mode.txt', 'Default', '**❈Default Mode Activated!**'),
    'mono on': ('settings/mode.txt', 'Mono', '**❈Mono Mode Activated!**'),
    'heart on': ('settings/heart.txt', 'True', '**❈heart Activated!**'),
    'heart off': ('settings/heart.txt', 'False', '**❈heart DeActivated!**'),
    'rname on': ('settings/rnamest.txt', 'True', '**❈Rname Activated!**'),
    'rname off': ('settings/rnamest.txt', 'False', '**❈Rname DeActivated!**'),
    'see rname': ('settings/rname.txt', None, '**❈Rnames : \n**'),
    'see bio': ('settings/bio.txt', None, '**❈Your Bio : \n**'),
    'see lname': ('settings/nameinfo.txt', None, '❈Your lname : \n'),
    'farsi on': ('settings/mode.txt', 'Farsi', '❈حالت فارسی فعال شد!'),
    'fancy on': ('settings/mode.txt', 'Fancy', '❈حالت فانتزی فعال شد!'),
    'circle on': ('settings/mode.txt', 'Circle', '❈حالت دایره‌ای فعال شد!')
}

async def settings(event):
    if event.sender_id != admin_user_id:
        return
    
    # دریافت متن دستور
    command = event.raw_text.lower().strip()
    
    if command not in patterns_actions:
        await event.edit("**❈ Command not recognized.**")
        return
    
    file_path, content, response = patterns_actions[command]

    if content is not None:
        with open(file_path, 'w') as f:
            f.write(content)

    # اجرای اکشن‌های ویژه
    if command == 'timename off':
        await client(UpdateProfileRequest(last_name=''))

    if command == 'timename on':
        await client(UpdateProfileRequest(last_name=get_current_time_str()))

    if command == 'bio off':
        await client(UpdateProfileRequest(about=''))
    
    if command == 'timepic off':
        photos = await client.get_profile_photos('me')
        if photos and len(photos) > 0:
            await client(functions.photos.DeletePhotosRequest(id=[InputPhoto(id=photos[0].id, access_hash=photos[0].access_hash, file_reference=photos[0].file_reference)]))

    # اضافه کردن محتوای فایل به پاسخ
    if file_path.endswith('.txt'):
        try:
            with open(file_path, 'r') as f:
                file_content = f.read()
            if file_content not in ["True", "False", "Bold", "Mono", "Default", "Mini", "rnd"] and file_content:
                response += f"`{file_content}`"
        except:
            pass

    await event.edit(response)

# ============= توابع tpic اصلاح‌شده =============
async def tpic_set(event):
    if event.sender_id == admin_user_id:
        try:
            pic_folder = 'pic/'
            if not os.path.exists(pic_folder):
                os.makedirs(pic_folder)
            
            clear_pic_folder()
            
            if event.is_reply:
                replied_msg = await event.get_reply_message()
                if replied_msg.photo:
                    photo = await client.download_media(replied_msg.photo, pic_folder + 'profile.jpg')
                    await event.edit("**❈ Working . . .**")
                    
                    if replied_msg.raw_text and '[' in replied_msg.raw_text and ']' in replied_msg.raw_text:
                        caption = replied_msg.raw_text
                        coordinates = [int(coord) for coord in caption[caption.index('[') + 1: caption.index(']')].split(',')]
                        color_start = caption.index('{') + 1
                        color_end = caption.index('}')
                        color = caption[color_start:color_end]
                        
                        with open('settings/tpic.json', 'w') as f:
                            json.dump({'cordx': coordinates[0], 'cordy': coordinates[1], 'size': coordinates[2], 'color': color}, f)
                        await event.edit("**❈ All Done ✅**")
                    else:
                        await event.edit("**❈ Please provide coordinates and color in format: [x,y,size]{color}**")
        except Exception as e:
            await event.edit(f"**❈ An error occurred: {e}**")

async def tpic_prv(event):
    if event.sender_id == admin_user_id:
        try:
            await event.delete()
            
            with open('settings/tpic.json', 'r') as f:
                data = json.load(f)
                cordx = data['cordx']
                cordy = data['cordy']
                size = data['size']
                color_string = data['color']
            
            pic_folder = 'pic/'
            if not os.path.exists(pic_folder):
                os.makedirs(pic_folder)
            
            # بررسی وجود فایل font
            font_path = 'fonts/Freshman.ttf'
            if not os.path.exists(font_path):
                # استفاده از فونت پیش‌فرض
                font_path = None
            
            with Image.open(pic_folder + 'profile.jpg') as img:
                draw = ImageDraw.Draw(img)
                if font_path:
                    font = ImageFont.truetype(font_path, size)
                else:
                    font = ImageFont.load_default()
                
                color = color_string
                position = (cordx, cordy)
                draw.text(position, "TEST", fill=color, font=font)
                img.save(pic_folder + 'profile_test.jpg', quality=95)
                
                with open(pic_folder + 'profile_test.jpg', 'rb') as f:
                    await client.send_file(event.chat_id, f, caption=f"cordx : {cordx}\ncordy : {cordy}\nsize : {size}\ncolor : {color}")
                
                os.remove(pic_folder + 'profile_test.jpg')
        except Exception as e:
            await event.edit(f"**❈ مشکلی پیش آمده: {e}**")
