from html import escape
from typing import Any, Tuple, Union

from loguru import logger
from pyrogram import types


def get_text(message: types.Message) -> str:
    # Get message's text
    text = ""
    try:
        if not message:
            return ""

        the_text = message.text or message.caption

        if the_text:
            text += the_text
    except:  # noqa
        logger.exception("Get text error")

    return text


def get_raw_ch_number(identifier: Union[str, int]) -> int:
    # Remove -100 prefix in channel / chat number
    try:
        identifier = str(identifier)
        if identifier.startswith("-100"):
            return int(identifier[4:])

        return int(identifier)
    except:  # noqa
        logger.exception("Get raw channel/chat number error")


def get_command_type(message: types.Message) -> str:
    # Get the command type "a" in "/command a"
    result = ""
    try:
        text = get_text(message)
        command_list = list(filter(None, text.split(" ")))
        result = text[len(command_list[0]):].strip()
    except:  # noqa
        logger.exception("Get command type error")

    return result


def get_message_mentions(message: types.Message) -> Tuple[Union[int, str]]:
    # Get all user id mentioned (@) from message
    result = []
    try:
        message_text = get_text(message).encode('utf-16')

        for entities in message.entities:
            if entities.type == "mention":
                result.append(message_text[entities.offset:entities.length + entities.offset].decode('utf-16'))
            elif entities.type == "text_mention":
                result.append(entities.user.id)
    except:  # noqa
        logger.exception("Get message mentions error")

    return tuple(result)


def italic(text: Any) -> str:
    # Get italic text
    try:
        text = str(text).strip()

        if text:
            return f"<i>{escape(text)}</i>"
    except:  # noqa
        logger.exception("Italic error")

    return ""


def bold(text: Any) -> str:
    # Get a bold text
    try:
        text = str(text).strip()

        if text:
            return f"<b>{escape(text)}</b>"
    except:  # noqa
        logger.exception("Bold error")

    return ""
