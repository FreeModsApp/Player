import urllib.parse
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

START_TEXT = """
<i>👋 Hᴇʏ,</i>{}\n
<i><b>Send or Forward Me Any File Here Which You Want To Upload Remotely In Streaam.net.</b></i>"""

HELP_TEXT = """
<b>🔥For Bot Related Any Help Contact @LegendAkshay</b>"""

ABOUT_TEXT = """
<b>🔥This Bot Is Only For Streaam.net Users To Made Uploading Easy & Fast.</b>\n
<b>(If You Are Not User Of Streaam.net So Fill The Form On Website And Start Using or We Banned You From Our Bot.)</b>"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )

@StreamBot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()

def get_media_file_size(m):
    media = m.video or m.audio or m.document
    if media and media.file_size:
        return media.file_size
    else:
        return None


def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None


@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="__Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ__\n\n @SID12O **Tʜᴇʏ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>This Is a Private Bot For our Streaam.net Users, You have to Join Our Telegram Channel To Verify You</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Join", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
               
                            ]]
                    ),
                    parse_mode="HTML"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ</i> <b><a href='http://t.me/LegendAkshay'>[ Click-Here ]</a></b>",
                    parse_mode="HTML",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text=START_TEXT.format(m.from_user.mention),
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
              )                                                                         
                                                                                       
                                                                            
    else:
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="**Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Qᴜɪᴄᴋʟʏ ᴄᴏɴᴛᴀᴄᴛ** @SID12O",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Pʟᴇᴀsᴇ Jᴏɪɴ Mʏ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴛʜɪs Bᴏᴛ**!\n\n**Dᴜᴇ ᴛᴏ Oᴠᴇʀʟᴏᴀᴅ, Oɴʟʏ Cʜᴀɴɴᴇʟ Sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜᴇ Bᴏᴛ**!",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                          InlineKeyboardButton("🤖 Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url=f"https://t.me/{Var.UPDATES_CHANNEL}")],
                         [InlineKeyboardButton("🔄 Joined", url=f"https://t.me/{(await b.get_me()).username}?start=AvishkarPatil_{usr_cmd}")
                        
                        ]]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍᴇ** [Akshay](https://t.me/LegendAkshay).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))
        file_name = get_media_file_name(get_msg)
        file_size = humanbytes(get_media_file_size(get_msg))

        stream_link = "https://{}/{}/{}".format(Var.FQDN, get_msg.message_id, file_name) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.message_id,
                                     file_name)

        msg_text ="""
<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n
<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n
<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n
<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n
<b>🚸 Nᴏᴛᴇ : Tʜɪs ᴘᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ, Nᴏᴛ Exᴘɪʀᴇᴅ</b>\n
<i>© @AvishkarPatil </i>"""

        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open", url=stream_link)]])
        )



@StreamBot.on_message(filters.private & filters.command(["about"]))
async def start(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ **\n\n [{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Started Your Bot !!__"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="<i>Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Admin @SID12O</i>",
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**This Is a Private Bot For our PlayerJet / 10Drives.com Users, You have to Join Our Telegram Channel To Verify You**",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("🤖 Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="__Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍᴇ__ [Aᴠɪsʜᴋᴀʀ Pᴀᴛɪʟ](https://t.me/LegendAkshay).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text=HELP_TEXT,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
        )

