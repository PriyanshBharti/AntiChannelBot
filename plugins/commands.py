from loguru import logger
from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.raw.types import BotCommand, BotCommandScopeUsers, BotCommandScopeChatAdmins

cmd_scope = {
    "private": ("start", "help"),
    "group_admin": ("stat", "is", "cwl", "crm"),
}

cmd_usage = {
    "start": "start",
    "help": "help [command]",
    "stat": "stat [clear]",
    "is": "is <reply/channel_id/mention>",
    "cwl": "cwl <reply/channel_id/mention>",
    "crm": "crm <reply/channel_id/mention>"
}

cmd_desc = {
    "start": "Start the bot",
    "help": "Show command usage",
    "stat": "Show statistics of this group for channels banned",
    "is": "Check for a channel is in whitelist",
    "cwl": "Add a channel to this group's whitelist",
    "crm": "Remove whitelist of the channel from this group"
}

cmd_args = {
    "stat": {
        "clear": "Clear current group's ban statistics (Won't affect ban result)",
    },
    "is": {
        "channel_id": "Channel ID",
    },
    "cwl": {
        "channel_id": "Channel ID",
        "reply": "Reply to a message sent by channel",
        "mention": "Mention a channel (@Telegram)"
    },
    "crm": {
        "channel_id": "Channel ID",
        "reply": "Reply to a message sent by channel",
        "mention": "Mention a channel (@Telegram)"
    },
}


def get_cmd_scope(str_scope: str):
    """
    Get a command scope by command
    :param str_scope: Scope name
    :return: BotCommandScope
    """
    if str_scope == "private":
        return BotCommandScopeUsers
    elif str_scope == "group_admin":
        return BotCommandScopeChatAdmins


async def init_bot_commands(client: Client):
    for str_scope, cmd_names in cmd_scope.items():
        commands = []
        for cmd_name in cmd_names:
            commands.append(BotCommand(
                command=cmd_name,
                description=cmd_desc[cmd_name]
            ))

        try:
            result = await client.send(
                functions.bots.SetBotCommands(
                    scope=get_cmd_scope(str_scope)(),
                    commands=commands,
                    lang_code="en"
                )
            )
            if result:
                logger.debug(f"Bot commands is set for scope {str_scope}. Commands applied: {', '.join(cmd_names)}")
            else:
                logger.warning(f"Failed to set up commands for scope {str_scope}.")
        except:  # noqa
            logger.exception(f"Error setting bot commands for scope {str_scope}.")

    logger.debug("Bot commands initialized.")
