from loguru import logger
from pyrogram import Client, types, filters

from plugins.commands import cmd_desc, cmd_usage, cmd_args
from plugins.filters import mod_filters
from plugins.functions.utils import get_command_type, italic, bold
from plugins.bot import prefix


@Client.on_message(filters.private & filters.incoming & ~filters.edited
                   & mod_filters.command(["help"], prefix))
async def cmd_help(client: Client, message: types.Message):
    help_cmd = get_command_type(message)

    try:
        if help_cmd:
            if cmd_usage.get(help_cmd) is None:
                await message.reply_text(f"Command not found: {help_cmd}", True)
                return

            usage_str_builder = [
                f"Usage - {help_cmd}",
                "",
                "Description:",
                cmd_desc[help_cmd],
                "",
                f"Usage: {prefix[0]}{cmd_usage[help_cmd]}",
            ]
            if cmd_args.get(help_cmd) is not None:
                usage_str_builder.extend((
                    "",
                    "Arguments:",
                    "\n".join(f"{arg} - {desc}" for arg, desc in cmd_args[help_cmd].items())
                ))

            detail_usage_text = "\n".join(usage_str_builder)
            await message.reply_text(detail_usage_text, True)
        else:
            simple_usage_txt = ["Simple usage:"]
            for cmd_name, usage in cmd_usage.items():
                simple_usage_txt.append(f"\u2022 {bold(cmd_name)} - {prefix[0]}{usage}")
            simple_usage_txt.extend(("", italic(f"Do {prefix[0]}help [command] for details")))
            if len(prefix) > 1:
                available_prefix = ", ".join(f"'{pfx}'" for pfx in prefix)
                simple_usage_txt.extend(("", italic(f"Available prefix(s): {available_prefix}")))

            await message.reply_text("\n".join(simple_usage_txt))
    except:  # noqa
        logger.exception(f"Help command error for user {message.from_user.id} with arguments \"{cmd_arg}\"")
