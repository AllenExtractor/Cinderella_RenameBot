import logging
import logging.config
import warnings
from pyrogram import Client, idle
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from pytz import timezone
from datetime import datetime
import asyncio
from plugins.web_support import web_server
from plugins.file_rename import app
import pyromod

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="SnowRenamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.force_channel = Config.FORCE_SUB
        if Config.FORCE_SUB:
            try:
                link = await self.export_chat_invite_link(Config.FORCE_SUB)
                self.invitelink = link
            except Exception as e:
                logging.warning(e)
                logging.warning("Make Sure Bot admin in force sub channel")
                self.force_channel = None
        logging.info(f"{me.first_name} ✅✅ BOT started successfully ✅✅")

        for id in Config.ADMIN:
            try:
                await self.send_message(id, f"**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
            except:
                pass

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>")
            except:
                print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Stopped 🙄")

bot_instance = Bot()

async def main():
    # Web server PEHLE start karo - Render health check ke liye zaroori
    web_app = web.AppRunner(await web_server())
    await web_app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(web_app, bind_address, Config.PORT).start()
    logging.info(f"Web server started on port {Config.PORT}")

    if Config.STRING_SESSION:
        await asyncio.gather(
            app.start(),
            bot_instance.start()
        )
    else:
        await bot_instance.start()
    await idle()

if __name__ == "__main__":
    warnings.filterwarnings("ignore", message="There is no current event loop")
    asyncio.run(main())
