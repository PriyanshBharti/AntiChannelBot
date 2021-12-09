from typing import Optional

from loguru import logger
from pyrogram import Client, types, filters, errors

from plugins.filters import mod_filters
from plugins.functions import database
from plugins.functions.telegram import is_group_admin
from plugins.functions.utils import get_command_type, get_message_mentions, bold, italic, get_raw_ch_number
from plugins.bot import prefix


async def get_channel_id(client: Client, message: types.Message) -> Optional[int]:
    # Get channel id from message

    # Reply
    if message.reply_to_message and message.reply_to_message.sender_chat:
        channel_id = message.reply_to_message.sender_chat.id
        return get_raw_ch_number(channel_id)

    # User input
    try:
        cmd_arg = get_command_type(message)
        channel_id = int(cmd_arg)

        return get_raw_ch_number(channel_id)
    except ValueError:
        pass

    # Mention
    mentions = get_message_mentions(message)
    if len(mentions) == 0:
        # Say something that is empty
        await message.reply_text(f"Incorrect usage.", True)
        return

    str_mention = mentions[0]
    if not isinstance(str_mention, str):
        # User is not allowed
        await message.reply_text(f"User is not a channel.", True)
        return
    try:
        channel_peer = await client.resolve_peer(str_mention)
        if not channel_peer.channel_id:
            # User is not allowed
            await message.reply_text(f"User is not a channel.", True)
            return
        channel_id = channel_peer.channel_id

        return get_raw_ch_number(channel_id)
    except (errors.UsernameOccupied, errors.UsernameInvalid):
        return
    except:  # noqa
        logger.exception(f"Error while resolving peer {str_mention} in function get_channel_id")
        return


@Client.on_message(filters.group & filters.incoming & ~filters.service & ~filters.edited
                   & mod_filters.command(["is"], prefix))
async def cmd_get_whitelist(client: Client, message: types.Message):
    # Basic data
    user_obj = message.from_user
    chat_obj = message.chat
    uid = user_obj and user_obj.id or "Unknown"
    cid = chat_obj and chat_obj.id or "Unknown"
    group_id = get_raw_ch_number(cid)

    try:
        # Check is admin
        if not await is_group_admin(cid, uid):
            return

        channel_id = await get_channel_id(client, message)
        if not channel_id:
            return

        # Check is linked channel
        if await database.get_linked_group(channel_id=channel_id):
            await message.reply_text("Linked channel already whitelisted automatically.", True)
            return

        # Check database for whitelist
        result = database.match_whitelist(group_id=group_id, channel_id=channel_id)
        result_text = italic("not whitelisted") if not result else bold("whitelisted")
        await message.reply_text("Channel is " + result_text, True)
    except:  # noqa
        logger.exception(f"Error while running command get whitelist for user {uid} from group {cid}")


@Client.on_message(filters.group & filters.incoming & ~filters.service & ~filters.edited
                   & mod_filters.command(["cwl"], prefix))
async def cmd_add_whitelist(client: Client, message: types.Message):
    # Basic data
    user_obj = message.from_user
    chat_obj = message.chat
    uid = user_obj and user_obj.id or "Unknown"
    cid = chat_obj and chat_obj.id or "Unknown"
    group_id = get_raw_ch_number(cid)

    try:
        # Check is admin
        if not await is_group_admin(cid, uid):
            return

        channel_id = await get_channel_id(client, message)
        if not channel_id:
            return

        # Check is linked channel
        if await database.get_linked_group(channel_id=channel_id):
            await message.reply_text("Linked channel already whitelisted automatically.", True)
            return

        # Check is channel already whitelisted
        if database.match_whitelist(group_id=group_id, channel_id=channel_id):
            await message.reply_text("Channel already whitelisted.", True)
            return

        # Add channel into whitelist for this group
        await database.add_whitelist(group_id=group_id, channel_id=channel_id)
        await message.reply_text("Channel added into whitelist.", True)

        # Unban if it's banned before
        try:
            channel_id = int(f"-100{channel_id}")
            if await client.unban_chat_member(cid, channel_id):
                logger.debug(f"Unbanned channel {channel_id} for group {cid}")
        except errors.ChatAdminRequired:
            pass
    except:  # noqa
        logger.exception(f"Error while running command add whitelist for user {uid} from group {cid}")


@Client.on_message(filters.group & filters.incoming & ~filters.service & ~filters.edited
                   & mod_filters.command(["crm"], prefix))
async def cmd_remove_whitelist(client: Client, message: types.Message):
    # Basic data
    user_obj = message.from_user
    chat_obj = message.chat
    uid = user_obj and user_obj.id or "Unknown"
    cid = chat_obj and chat_obj.id or "Unknown"
    group_id = get_raw_ch_number(cid)

    try:
        # Check is admin
        if not await is_group_admin(cid, uid):
            return

        channel_id = await get_channel_id(client, message)
        if not channel_id:
            return

        # Check is linked channel
        if await database.get_linked_group(channel_id=channel_id):
            await message.reply_text("Linked channel already whitelisted automatically and cannot be removed.", True)
            return

        # Check is channel already whitelisted
        if not database.match_whitelist(group_id=group_id, channel_id=channel_id):
            await message.reply_text("Channel is not whitelisted.", True)
            return

        # Remove channel into whitelist for this group
        await database.remove_whitelist(group_id=group_id, channel_id=channel_id)
        await message.reply_text("Channel removed from whitelist.", True)
    except:  # noqa
        logger.exception(f"Error while running command remove whitelist for user {uid} from group {cid}")
