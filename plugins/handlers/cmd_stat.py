from loguru import logger
from pyrogram import Client, types, filters

from plugins.filters import mod_filters
from plugins.functions import database
from plugins.functions.telegram import is_group_admin
from plugins.functions.utils import get_command_type, get_raw_ch_number
from plugins.bot import prefix


@Client.on_message(filters.group & filters.incoming & ~filters.service & ~filters.edited
                   & mod_filters.command(["stat"], prefix))
async def cmd_stat(client: Client, message: types.Message):
    # Basic data
    user_obj = message.from_user
    chat_obj = message.chat
    uid = user_obj and user_obj.id or "Unknown"
    cid = chat_obj and chat_obj.id or "Unknown"
    is_clear = get_command_type(message) == "clear"
    chat_id = get_raw_ch_number(cid)

    try:
        if is_clear and await is_group_admin(cid, uid):
            result_count = await database.clear_channel_stat_data(group_id=chat_id)
            if result_count is None:
                await message.reply_text("No record to clear.", True)
                return
            await message.reply_text(f"Cleared {result_count} channel(s).", True)
            return

        result_count = database.get_banned_channels_count(group_id=chat_id)
        if result_count is None:
            await message.reply_text("This group didn't have ban record yet.", True)
            return
        await message.reply_text(f"Total channel(s) banned: {result_count}", True)
    except:  # noqa
        logger.exception(f"Error when running command stat for {uid} in {cid}")
