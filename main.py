from asyncio import run

from loguru import logger
from pyrogram import Client, idle

from plugins.commands import init_bot_commands


def init_link_channel():
    """
    Initialize linked channel database's table
    """
    from plugins.glovar import linked_channel_db, whitelist_db, stat_db

    sql_path = "plugins/sqls/"

    try:
        # Execute create link channel table script
        sql_script = open(sql_path + "create_link_channel_table.sql", "r").read()
        cur = linked_channel_db.cursor()
        cur.executescript(sql_script)
        linked_channel_db.commit()
        cur.close()
    except:  # noqa
        logger.exception("Error while initializing linked channel database table")

    try:
        # Execute create whitelist table script
        sql_script = open(sql_path + "create_whitelist_table.sql", "r").read()
        cur = whitelist_db.cursor()
        cur.executescript(sql_script)
        whitelist_db.commit()
        cur.close()
    except:  # noqa
        logger.exception("Error while initializing whitelist database table")

    try:
        # Execute create stat table script
        sql_script = open(sql_path + "create_stat_table.sql", "r").read()
        cur = stat_db.cursor()
        cur.executescript(sql_script)
        stat_db.commit()
        cur.close()
    except:  # noqa
        logger.exception("Error while initializing stat database table")

    logger.debug("All database initialized")


async def main():
    import plugins.glovar
    init_link_channel()
    bot_client = Client("bot")
    setattr(plugins.bot, "bot_client", bot_client)
    # Get username first before fully initialize
    logger.debug("Connect first time for getting username only")
    is_authorized = await bot_client.connect()
    if not is_authorized:
        await bot_client.authorize()
    bot_info = await bot_client.get_me()
    setattr(plugins.bot, "bot_name", bot_info.username)
    await bot_client.disconnect()
    logger.debug(f"Disconnected, now for real bot initialize")
    await bot_client.start()
    await init_bot_commands(bot_client)
    fixed_prefix = f"Bot instance \"{bot_info.username}\" "
    logger.success(fixed_prefix + "started.")
    await idle()
    logger.debug(fixed_prefix + "stopping...")
    # Stop bot instance
    await bot_client.stop()
    from plugins.bot import linked_channel_db, whitelist_db, stat_db
    # Close all db(s)
    linked_channel_db.close()
    whitelist_db.close()
    stat_db.close()
    logger.info(fixed_prefix + "stopped.")


if __name__ == '__main__':
    run(main())
