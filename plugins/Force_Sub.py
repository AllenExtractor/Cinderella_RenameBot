from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from config import Config
from helper.database import db

async def not_subscribed(_, client, message):
    await db.add_user(client, message)
    if not Config.FORCE_SUB:
        return False
    # /start command ko exempt karo taki user join button dekh sake
    if message.command and message.command[0] == "start":
        return False
    try:             
        user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id) 
        if user.status == enums.ChatMemberStatus.BANNED:
            return True  # banned user → block karo
        else:
            return False  # joined & not banned → allow karo
    except UserNotParticipant:
        pass
    return True  # not joined → block karo


@Client.on_message(filters.private & filters.create(not_subscribed))
async def forces_sub(client, message):
    buttons = [[InlineKeyboardButton(text="📢 ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{Config.FORCE_SUB}") ]]
    text = "**sᴏʀʀʏ ᴅᴜᴅᴇ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴍʏ ᴄʜᴀɴɴᴇʟ sᴏ ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ😁**"
    
    try:
        user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id)    
        if user.status == enums.ChatMemberStatus.BANNED:
            # User banned hai → banned message do
            return await client.send_message(message.from_user.id, text="Sᴏʀʀy Yᴏᴜ'ʀᴇ Bᴀɴɴᴇᴅ Tᴏ Uꜱᴇ Mᴇ")
        else:
            # User joined & not banned → yahan KABHI nahi aana chahiye
            # (not_subscribed ne already False return kar diya hoga)
            # Agar kisi race condition se yahan aa bhi gaye, toh message forward karo
            return await message.continue_propagation()
    except UserNotParticipant:
        # User joined nahi → join karne ka message do
        return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
