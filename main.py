from asyncio import run

from loguru import logger
from pyrogram import Client, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

async def main():
    bot_client = Client("bot")
    await bot_client.start()
    import plugins.bot
    setattr(plugins.bot, "bot_client", bot_client)
    bot_info = await bot_client.get_me()
    logger.success(f"Bot instance \"{bot_info.username}\" started.")
    await idle()
    logger.debug(f"Stopping bot instance \"{bot_info.username}\" ...")
    await bot_client.stop()
    logger.info(f"Bot instance \"{bot_info.username}\" stopped.")
    
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Client.on_message(filters.command(["start", "start@AntiChannel_RBot"]))
async def start(_, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name} 😉️!</b>
 `Heya I'm A Anti Channel Telegram bot Just add me to the chat, and I will block the channels that write to the chat.`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📢 Cʜᴀɴɴᴇʟ", url="https://t.me/DeeCodeBots"
                    ),
                    InlineKeyboardButton(
                        "Sᴜᴘᴘᴏʀᴛ 👥", url="https://t.me/DeCodeSupport"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🧑‍💻 Dᴇᴠ 🧑‍💻", url="https://t.me/DeeCodeDevs"
                    )
                ]
            ]
        )
    )


if __name__ == '__main__':
    run(main())
