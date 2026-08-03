from .library import *
from .Information import *

def get_user_bio():
    with open('settings/bio.txt', 'r') as f:
        return f.read().strip()

timezone = pytz.timezone('Asia/Tehran')

current_time_str = datetime.datetime.now(timezone).strftime("%H:%M")

def apply_font(text, mode):
    if mode == 'Bold':
        text = text.replace("0", "𝟎").replace("1", "𝟏").replace("2", "𝟐").replace("3", "𝟑").replace("4", "𝟒").replace("5", "𝟓").replace("6", "𝟔").replace("7", "𝟕").replace("8", "𝟖").replace("9", "𝟗")
    if mode == 'Mono':
        text = text.replace("0", "０").replace("1", "１").replace("2", "２").replace("3", "３").replace("4", "４").replace("5", "５").replace("6", "６").replace("7", "７").replace("8", "８").replace("9", "９")
    if mode == 'Mini':
        text = text.replace("0", "⁰").replace("1", "¹").replace("2", "²").replace("3", "³").replace("4", "⁴").replace("5", "⁵").replace("6", "⁶").replace("7", "⁷").replace("8", "⁸").replace("9", "⁹")
    if mode == 'Farsi':
        text = text.replace("0", "۰").replace("1", "۱").replace("2", "۲").replace("3", "۳").replace("4", "۴").replace("5", "۵").replace("6", "۶").replace("7", "۷").replace("8", "۸").replace("9", "۹")
    if mode == 'Fancy':
        text = text.replace("0", "⓪").replace("1", "①").replace("2", "②").replace("3", "③").replace("4", "④").replace("5", "⑤").replace("6", "⑥").replace("7", "⑦").replace("8", "⑧").replace("9", "⑨")
    if mode == 'Circle':
        text = text.replace("0", "⓿").replace("1", "❶").replace("2", "❷").replace("3", "❸").replace("4", "❹").replace("5", "❺").replace("6", "❻").replace("7", "❼").replace("8", "❽").replace("9", "❾")
    if mode == 'Subscript':
        text = text.replace("0", "₀").replace("1", "₁").replace("2", "₂").replace("3", "₃").replace("4", "₄").replace("5", "₅").replace("6", "₆").replace("7", "₇").replace("8", "₈").replace("9", "₉")
    if mode == 'DoubleStruck':
        text = text.replace("0", "𝟘").replace("1", "𝟙").replace("2", "𝟚").replace("3", "𝟛").replace("4", "𝟜").replace("5", "𝟝").replace("6", "𝟞").replace("7", "𝟟").replace("8", "𝟠").replace("9", "𝟡")
    if mode == 'SansBold':
        text = text.replace("0", "𝟬").replace("1", "𝟭").replace("2", "𝟮").replace("3", "𝟯").replace("4", "𝟰").replace("5", "𝟱").replace("6", "𝟲").replace("7", "𝟳").replace("8", "𝟴").replace("9", "𝟵")
    if mode == 'Sans':
        text = text.replace("0", "𝟢").replace("1", "𝟣").replace("2", "𝟤").replace("3", "𝟥").replace("4", "𝟦").replace("5", "𝟧").replace("6", "𝟨").replace("7", "𝟩").replace("8", "𝟪").replace("9", "𝟫")
    if mode == 'Typewriter':
        text = text.replace("0", "𝟶").replace("1", "𝟷").replace("2", "𝟸").replace("3", "𝟹").replace("4", "𝟺").replace("5", "𝟻").replace("6", "𝟼").replace("7", "𝟽").replace("8", "𝟾").replace("9", "𝟿")
    if mode == 'rnd':
        font_options = [
            ["𝟶", "𝟷", "𝟸", "𝟹", "𝟺", "𝟻", "𝟼", "𝟽", "𝟾", "𝟿"],
            ["⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨"],
            ["⓿", "❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽", "❾"],
            ["0", "𝟙", "ϩ", "Ӡ", "५", "Ϭ", "Ϭ", "7", "𝟠", "९"],
            ["⁰", "₁", "²", "₃", "⁴", "₅", "⁶", "₇", "⁸", "₉"],
            ["０", "１", "２", "３", "４", "５", "６", "７", "８", "９"],
            ["𝟬", "𝟭", "𝟮", "𝟯", "𝟰", "𝟱", "𝟲", "𝟳", "𝟴", "𝟵"],
            ["𝟎", "𝟏", "𝟐", "𝟑", "𝟒", "𝟓", "𝟔", "𝟕", "𝟖", "𝟗"],
            ["𝟶", "𝟷", "𝟸", "𝟹", "𝟺", "𝟻", "𝟼", "𝟽", "𝟾", "𝟿"]
        ]
        random_font = random.choice(font_options)
        text = text.translate(str.maketrans("0123456789", "".join(random_font)))
    return text


async def update_last_name():
    global current_time_str
    while True:
        with open('settings/time.txt', 'r') as f:
            option_enabled = f.read().strip() == 'True'
        with open('settings/heart.txt', 'r') as f:
            heart_enabled = f.read().strip() == 'True'
        with open('settings/mode.txt', 'r') as f:
            mode = f.read().strip()

        if option_enabled:
            current_time = datetime.datetime.now(timezone)
            rounded_time = current_time.replace(second=0, microsecond=0) + datetime.timedelta(minutes=ceil(current_time.second/60))
            current_time_str = rounded_time.strftime("%H:%M")
            current_time_str = apply_font(current_time_str, mode)

            heart_list = ['❤️', '💛', '💚', '💙', '💜', '🖤', '🤍', '🧡', '💖', '💗', '💓', '💞', '💕', '💘', '💝', '💟', '🩵']
            heart = random.choice(heart_list)

            with open('settings/nameinfo.txt', 'r') as f:
                user_lname = f.read()
            user_lname = user_lname.replace("time", current_time_str).replace("heart", heart)
            await client(UpdateProfileRequest(last_name=f"{user_lname}"))
        
        await asyncio.sleep(60 - datetime.datetime.now(timezone).second)



async def update_about():
    while True:
        with open('settings/bioinfo.txt', 'r') as f:
            bio_info_enabled = f.read().strip() == 'True'

        if bio_info_enabled:
            with open('settings/mode.txt', 'r') as f:
                mode = f.read().strip()

            current_time = datetime.datetime.now(timezone)
            rounded_time = current_time.replace(second=0, microsecond=0) + datetime.timedelta(minutes=ceil(current_time.second / 60))
            current_time_str = rounded_time.strftime("%H:%M")
            persian_date = jdatetime.datetime.now().strftime("%Y/%m/%d")

            current_time_str = apply_font(current_time_str, mode)
            persian_date = apply_font(persian_date, mode)

            heart_list = ['❤️', '💛', '💚', '💙', '💜', '🖤', '🤍', '🧡', '💖', '💗', '💓', '💞', '💕', '💘', '💝', '💟', '🩵']
            heart = random.choice(heart_list)

            bio = get_user_bio().replace("time", current_time_str).replace("heart", heart).replace("DATE", persian_date)
            await client(UpdateProfileRequest(about=bio))

        await asyncio.sleep(60 - datetime.datetime.now(timezone).second)


async def update_first_name():
    prev_name = ''
    while True:
        with open('settings/rnamest.txt', 'r') as f:
            rname_enabled = f.read().strip() == 'True'
        if rname_enabled:
            with open('settings/rname.txt', 'r') as f:
                names = f.read().strip().split(',')
            if len(names) >= 1:
                first_name = random.choice(names).strip()
                while first_name == prev_name:
                    first_name = random.choice(names).strip()
                await client(UpdateProfileRequest(first_name=first_name))
                prev_name = first_name
        current_time = datetime.datetime.now(timezone)
        rounded_time = current_time.replace(second=0, microsecond=0) + datetime.timedelta(minutes=ceil(current_time.second/60))
        current_time_str = rounded_time.strftime("%H:%M")
        next_minute = (rounded_time + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
        time_until_next_minute = (next_minute - current_time).total_seconds()
        await asyncio.sleep(time_until_next_minute)


async def update_profile_photo():
    while True:
        with open('settings/timepic.txt', 'r') as f:
            option_enabled = f.read().strip() == 'True'

        if option_enabled:
            current_time = datetime.datetime.now(timezone)
            rounded_time = current_time.replace(second=0, microsecond=0) + datetime.timedelta(minutes=ceil(current_time.second/60))
            current_time_str = rounded_time.strftime("%H:%M")
            with open('settings/tpic.json', 'r') as f:
                data = json.load(f)
                cordx = data['cordx']
                cordy = data['cordy']
                size = data['size']
                color_string = data['color']
            with Image.open('pic/profile.jpg') as img:
                draw = ImageDraw.Draw(img)
                font_path = 'fonts/Freshman.ttf'
                font_size = size
                font = ImageFont.truetype(font_path, font_size)
                color = color_string
                position = (cordx, cordy)
                draw.text(position, current_time_str, fill=color, font=font)
                img.save('pic/profile_modified.jpg', quality=95)

            photos = await client.get_profile_photos('me')
            if photos.total > 0:
                await client(functions.photos.DeletePhotosRequest(id=[InputPhoto(id=photos[0].id, access_hash=photos[0].access_hash, file_reference=photos[0].file_reference)]))

            with open('pic/profile_modified.jpg', 'rb') as f:
                uploaded_file = await client.upload_file(f)
                await client(functions.photos.UploadProfilePhotoRequest(file=uploaded_file))

        if os.path.exists('pic/profile_modified.jpg'):
            os.remove('pic/profile_modified.jpg')

        await asyncio.sleep(60 - datetime.datetime.now(timezone).second)
