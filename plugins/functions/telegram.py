import asyncio
from typing import Union, Optional

from loguru import logger
from pyrogram.errors import FloodWait, PeerIdInvalid, ChannelInvalid, ChannelPrivate, UserNotParticipant
from pyrogram.types import ChatMember


async def is_group_admin(cid: int, uid: int) -> Union[bool, ChatMember, None]:
    """
    Check is user the target group's admin
    :param cid: Group ID
    :param uid: User ID
    :return: ChatMember object when true, false/none when failed
    """
    from plugins.bot import bot_client
    result: Optional[ChatMember] = None
    try:
        result = await bot_client.get_chat_member(chat_id=cid, user_id=uid)  # noqa
        if result.status in ("creator", "administrator"):
            return result
        return False
    except FloodWait as e:
        logger.debug(f"{e}, retry after {e.x + 1} seconds...")
        await asyncio.sleep(e.x + 1)
        return await is_group_admin(cid, uid)
    except (PeerIdInvalid, ChannelInvalid, ChannelPrivate, UserNotParticipant):
        return False
    except Exception:  # noqa
        logger.exception(f"Get is group admin in {cid} for {uid} error")

    return result
