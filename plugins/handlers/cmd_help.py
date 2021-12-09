from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton



@Client.on_message(
    filters.command("help")
    & filters.private
    & filters.group
    & ~ filters.edited
)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>Hi {message.from_user.first_name}!
Setting up
1) Add this Bot to your Group and Make it Admin With Ban And Delte Message permission

Commands

- /start: To Start the bot
- /help : To Help You
- /stat : Show statistics of this group for channels banned
- /is   : check for a channel is in whitelist
- /cwl  : Add a channel to this group's whitelisti
- /crm  : Remove whitelist of the channel from this group

**=>> Note 🧑‍🔧**
- Use /is/cwl and /crm In Groups Online /Comond channel id
 </b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Support Chat", url="https://t.me/DeCodeSupport"
                    )
                ]
            ]
        )
    )    

