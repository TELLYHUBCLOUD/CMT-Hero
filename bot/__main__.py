from asyncio import create_subprocess_exec, gather
from os import execl as osexecl
from signal import SIGINT, signal
from sys import executable
from time import time, sleep, monotonic
from uuid import uuid4

from aiofiles import open as aiopen
from aiofiles.os import path as aiopath
from aiofiles.os import remove as aioremove
from psutil import (boot_time, cpu_count, cpu_percent, cpu_freq, disk_usage,
                    net_io_counters, swap_memory, virtual_memory)
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler

from bot import (DATABASE_URL, INCOMPLETE_TASK_NOTIFIER, LOGGER,
                 STOP_DUPLICATE_TASKS, Interval, QbInterval, bot, botStartTime,
                 config_dict, scheduler, user_data)
from bot.helper.listeners.aria2_listener import start_aria2_listener

from .helper.ext_utils.bot_utils import (cmd_exec, get_readable_file_size,
                                         get_readable_time, set_commands,
                                         sync_to_async, get_progress_bar_string)
from .helper.ext_utils.db_handler import DbManger
from .helper.ext_utils.fs_utils import clean_all, exit_clean_up, start_cleanup
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.message_utils import (editMessage, sendFile,
                                                   sendMessage, auto_delete_message)
from .modules import (anonymous, authorize, bot_settings, cancel_mirror,
                      category_select, clone, eval, gd_count, gd_delete,
                      gd_list, leech_del, mirror_leech, rmdb, rss,
                      shell, status, torrent_search,
                      torrent_select, users_settings, ytdlp)


async def stats(_, message):
    total, used, free, disk = disk_usage('/')
    memory = virtual_memory()
    currentTime = get_readable_time(time() - botStartTime)
    mem_p = memory.percent
    osUptime = get_readable_time(time() - boot_time())
    cpuUsage = cpu_percent(interval=0.5)
    if await aiopath.exists('.git'):
        command = '''
                    remote_url=$(git config --get remote.origin.url) &&
                    if echo "$remote_url" | grep -qE "github\.com[:/](.*)/(.*?)(\.git)?$"; then
                        owner_name=$(echo "$remote_url" | awk -F/ '{ print $(NF-1) }') &&
                        repo_name=$(echo "$remote_url" | awk -F/ '{ print $NF }' | sed 's/\.git$//') &&
                        last_commit=$(git log -1 --pretty=format:'%h') &&
                        commit_link="https://github.com/$owner_name/$repo_name/commit/$last_commit" &&
                        echo $commit_link;
                    else
                        echo "Failed to extract repository name and owner name from the remote URL.";
                    fi
                '''
        commit_link = (await cmd_exec(command, True))[0]
        commit_id = (await cmd_exec("git log -1 --pretty=format:'%h'", True))[0]
        commit_from = (await cmd_exec("git log -1 --date=short --pretty=format:'%cr'", True))[0]
        commit_date = (await cmd_exec("git log -1 --date=format:'%d %B %Y' --pretty=format:'%ad'", True))[0]
        commit_time = (await cmd_exec("git log -1 --date=format:'%I:%M:%S %p' --pretty=format:'%ad'", True))[0]
        commit_name = (await cmd_exec("git log -1 --pretty=format:'%s'", True))[0]
        
        commit_html_link = f'<a href="{commit_link}">{commit_id}</a>'
        
        stats = f'<b>REPOSITORY INFO</b>\n\n' \
            f"<code>• Last commit: </code>{commit_html_link}\n"\
            f'<code>• Commit date: </code>{commit_date}\n'\
            f'<code>• Commited on: </code>{commit_time}\n'\
            f'<code>• From now   : </code>{commit_from}\n'\
            f"<code>• What's new : </code>{commit_name}\n"\
            f'\n'\
            f'<b>SYSTEM INFO</b>\n\n'\
            f'<code>• Bot uptime :</code> {currentTime}\n'\
            f'<code>• Sys uptime :</code> {osUptime}\n'\
            f'<code>• CPU usage  :</code> {cpuUsage}%\n'\
            f'<code>• RAM usage  :</code> {mem_p}%\n'\
            f'<code>• Disk usage :</code> {disk}%\n'\
            f'<code>• Disk space :</code> {get_readable_file_size(free)}/{get_readable_file_size(total)}\n\n'\
            
        if config_dict['SHOW_LIMITS']:
        
            DIRECT_LIMIT = config_dict['DIRECT_LIMIT']
            YTDLP_LIMIT = config_dict['YTDLP_LIMIT']
            GDRIVE_LIMIT = config_dict['GDRIVE_LIMIT']
            TORRENT_LIMIT = config_dict['TORRENT_LIMIT']
            CLONE_LIMIT = config_dict['CLONE_LIMIT']
            MEGA_LIMIT = config_dict['MEGA_LIMIT']
            LEECH_LIMIT = config_dict['LEECH_LIMIT']
            USER_MAX_TASKS = config_dict['USER_MAX_TASKS']
        
            torrent_limit = '∞' if TORRENT_LIMIT == '' else f'{TORRENT_LIMIT}GB/Link'
            clone_limit = '∞' if CLONE_LIMIT == '' else f'{CLONE_LIMIT}GB/Link'
            gdrive_limit = '∞' if GDRIVE_LIMIT == '' else f'{GDRIVE_LIMIT}GB/Link'
            mega_limit = '∞' if MEGA_LIMIT == '' else f'{MEGA_LIMIT}GB/Link'
            leech_limit = '∞' if LEECH_LIMIT == '' else f'{LEECH_LIMIT}GB/Link'
            user_task = '∞' if USER_MAX_TASKS == '' else f'{USER_MAX_TASKS} Tasks/user'
            ytdlp_limit = '∞' if YTDLP_LIMIT == '' else f'{YTDLP_LIMIT}GB/Link'
            direct_limit = '∞' if DIRECT_LIMIT == '' else f'{DIRECT_LIMIT}GB/Link'
            stats += f'<b>LIMITATIONS</b>\n\n'\
                f'<code>• Torrent    :</code> {torrent_limit}\n'\
                f'<code>• Gdrive     :</code> {gdrive_limit}\n'\
                f'<code>• Ytdlp      :</code> {ytdlp_limit}\n'\
                f'<code>• Direct     :</code> {direct_limit}\n'\
                f'<code>• Leech      :</code> {leech_limit}\n'\
                f'<code>• Clone      :</code> {clone_limit}\n'\
                f'<code>• Mega       :</code> {mega_limit}\n'\
                f'<code>• User tasks :</code> {user_task}\n\n'
    await sendMessage(message, stats)


async def start(_, message):
    if len(message.command) > 1:
        userid = message.from_user.id
        input_token = message.command[1]
        if userid not in user_data:
            return await sendMessage(message, 'Token ini bukan untukmu!\n\nSilakan buat sendiri.')
        data = user_data[userid]
        if 'token' not in data or data['token'] != input_token:
            return await sendMessage(message, 'Token sudah digunakan!\n\nSilakan buat yang baru.')
        data['token'] = str(uuid4())
        data['time'] = time()
        user_data[userid].update(data)
        msg = 'Token berhasil diperbarui!\n\n'
        msg += f'Masa Token Berlaku: {get_readable_time(int(config_dict["TOKEN_TIMEOUT"]))}'
        return await sendMessage(message, msg)
    elif config_dict['DM_MODE']:
        start_string = 'Bot sudah di restart.\n' \
                       'Sekarang kau bisa mengunakannya.\n' \
                       'Silahkan gunakan disini: @peamasamba'
    else:
        start_string = 'Maaf, kau tak bisa gunakan ini!\n' \
                       'Gabung kesini @peamasamba.\n' \
                       'Terima Kasih'
    await sendMessage(message, start_string)


async def restart(_, message):
    restart_message = await sendMessage(message, "Restarting...")
    if scheduler.running:
        scheduler.shutdown(wait=False)
    for interval in [QbInterval, Interval]:
        if interval:
            interval[0].cancel()
    await sync_to_async(clean_all)
    proc1 = await create_subprocess_exec('pkill', '-9', '-f', '-e', 'gunicorn|buffet|openstack|render|zcl')
    proc2 = await create_subprocess_exec('python3', 'update.py')
    await gather(proc1.wait(), proc2.wait())
    async with aiopen(".restartmsg", "w") as f:
        await f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    osexecl(executable, executable, "-m", "bot")

async def ping(_, message):
    start_time = monotonic()
    reply = await sendMessage(message, "Starting Ping")
    end_time = monotonic()
    ping_time = int((end_time - start_time) * 1000)
    await editMessage(reply, f'{ping_time} ms')

async def log(_, message):
    await sendFile(message, 'Z_Logs.txt')

help_string = f'''
<b>NOTE: Click on any CMD to see more detalis.</b>

/{BotCommands.MirrorCommand[0]} or /{BotCommands.MirrorCommand[1]}: Upload to Cloud Drive.
/{BotCommands.ZipMirrorCommand[0]} or /{BotCommands.ZipMirrorCommand[1]}: Upload as zip.
/{BotCommands.UnzipMirrorCommand[0]} or /{BotCommands.UnzipMirrorCommand[1]}: Unzip before upload.

<b>Use qBit commands for torrents only:</b>
/{BotCommands.QbMirrorCommand[0]} or /{BotCommands.QbMirrorCommand[1]}: Download using qBittorrent and Upload to Cloud Drive.
/{BotCommands.QbZipMirrorCommand[0]} or /{BotCommands.QbZipMirrorCommand[1]}: Download using qBittorrent and upload as zip.
/{BotCommands.QbUnzipMirrorCommand[0]} or /{BotCommands.QbUnzipMirrorCommand[1]}: Download using qBittorrent and unzip before upload.

/{BotCommands.BtSelectCommand}: Select files from torrents by gid or reply.
/{BotCommands.CategorySelect}: Change upload category for Google Drive.

<b>Use Yt-Dlp commands for YouTube or any videos:</b>
/{BotCommands.YtdlCommand[0]} or /{BotCommands.YtdlCommand[1]}: Mirror yt-dlp supported link.
/{BotCommands.YtdlZipCommand[0]} or /{BotCommands.YtdlZipCommand[1]}: Mirror yt-dlp supported link as zip.

<b>Use Leech commands for upload to Telegram:</b>
/{BotCommands.LeechCommand[0]} or /{BotCommands.LeechCommand[1]}: Upload to Telegram.
/{BotCommands.ZipLeechCommand[0]} or /{BotCommands.ZipLeechCommand[1]}: Upload to Telegram as zip.
/{BotCommands.UnzipLeechCommand[0]} or /{BotCommands.UnzipLeechCommand[1]}: Unzip before upload to Telegram.
/{BotCommands.QbLeechCommand[0]} or /{BotCommands.QbLeechCommand[1]}: Download using qBittorrent and upload to Telegram(For torrents only).
/{BotCommands.QbZipLeechCommand[0]} or /{BotCommands.QbZipLeechCommand[1]}: Download using qBittorrent and upload to Telegram as zip(For torrents only).
/{BotCommands.QbUnzipLeechCommand[0]} or /{BotCommands.QbUnzipLeechCommand[1]}: Download using qBittorrent and unzip before upload to Telegram(For torrents only).
/{BotCommands.YtdlLeechCommand[0]} or /{BotCommands.YtdlLeechCommand[1]}: Download using Yt-Dlp(supported link) and upload to telegram.
/{BotCommands.YtdlZipLeechCommand[0]} or /{BotCommands.YtdlZipLeechCommand[1]}: Download using Yt-Dlp(supported link) and upload to telegram as zip.

/leech{BotCommands.DeleteCommand} [telegram_link]: Delete replies from telegram (Only Owner & Sudo).

<b>G-Drive commands:</b>
/{BotCommands.CloneCommand}: Copy file/folder to Cloud Drive.
/{BotCommands.CountCommand} [drive_url]: Count file/folder of Google Drive.
/{BotCommands.DeleteCommand} [drive_url]: Delete file/folder from Google Drive (Only Owner & Sudo).

<b>Cancel Tasks:</b>
/{BotCommands.CancelMirror[0]} or /{BotCommands.CancelMirror[1]}: Cancel task by gid or reply.
/{BotCommands.CancelAllCommand[0]} : Cancel all tasks which added by you /{BotCommands.CancelAllCommand[1]} to in bots.

<b>Torrent/Drive Search:</b>
/{BotCommands.ListCommand} [query]: Search in Google Drive(s).
/{BotCommands.SearchCommand} [query]: Search for torrents with API.

<b>Bot Settings:</b>
/{BotCommands.UserSetCommand}: Open User settings.
/{BotCommands.UsersCommand}: show users settings (Only Owner & Sudo).
/{BotCommands.BotSetCommand}: Open Bot settings (Only Owner & Sudo).

<b>Authentication:</b>
/{BotCommands.AuthorizeCommand}: Authorize a chat or a user to use the bot (Only Owner & Sudo).
/{BotCommands.UnAuthorizeCommand}: Unauthorize a chat or a user to use the bot (Only Owner & Sudo).
/{BotCommands.AddSudoCommand}: Add sudo user (Only Owner).
/{BotCommands.RmSudoCommand}: Remove sudo users (Only Owner).

<b>Bot Stats:</b>
/{BotCommands.StatusCommand[0]} or /{BotCommands.StatusCommand[1]}: Shows a status of all active tasks.
/{BotCommands.StatsCommand[0]} or /{BotCommands.StatsCommand[1]}: Show server stats.
/{BotCommands.PingCommand[0]} or /{BotCommands.PingCommand[1]}: Check how long it takes to Ping the Bot.

<b>Maintainance:</b>
/{BotCommands.RestartCommand[0]}: Restart and update the bot (Only Owner & Sudo).
/{BotCommands.RestartCommand[1]}: Restart and update all bots (Only Owner & Sudo).
/{BotCommands.LogCommand}: Get a log file of the bot. Handy for getting crash reports (Only Owner & Sudo).

<b>Extras:</b>
/{BotCommands.ShellCommand}: Run shell commands (Only Owner).
/{BotCommands.EvalCommand}: Run Python Code Line | Lines (Only Owner).
/{BotCommands.ExecCommand}: Run Commands In Exec (Only Owner).
/{BotCommands.ClearLocalsCommand}: Clear {BotCommands.EvalCommand} or {BotCommands.ExecCommand} locals (Only Owner).

<b>RSS Feed:</b>
/{BotCommands.RssCommand}: Open RSS Menu.

<b>Attention: Read the first line again!</b>
'''


async def bot_help(_, message):
    reply_message = await sendMessage(message, help_string)
    await auto_delete_message(message, reply_message)


async def restart_notification():
    if await aiopath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
    else:
        chat_id, msg_id = 0, 0

    async def send_incompelete_task_message(cid, msg):
        try:
            if msg.startswith('Restarted Successfully!'):
                await bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text='Restarted Successfully!')
                await bot.send_message(chat_id, msg, disable_web_page_preview=True, reply_to_message_id=msg_id)
                await aioremove(".restartmsg")
            else:
                await bot.send_message(chat_id=cid, text=msg, disable_web_page_preview=True,
                                       disable_notification=True)
        except Exception as e:
            LOGGER.error(e)
    if DATABASE_URL:
        if INCOMPLETE_TASK_NOTIFIER and (notifier_dict := await DbManger().get_incomplete_tasks()):
            for cid, data in notifier_dict.items():
                msg = 'Restarted Successfully!' if cid == chat_id else 'Bot Restarted!'
                for tag, links in data.items():
                    msg += f"\n\n👤 {tag} Do your tasks again. \n"
                    for index, link in enumerate(links, start=1):
                        msg += f" {index}: {link} \n"
                        if len(msg.encode()) > 4000:
                            await send_incompelete_task_message(cid, msg)
                            msg = ''
                if msg:
                    await send_incompelete_task_message(cid, msg)

        if STOP_DUPLICATE_TASKS:
            await DbManger().clear_download_links()


    if await aiopath.isfile(".restartmsg"):
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text='Berhasil, Selamat!')
        except:
            pass
        await aioremove(".restartmsg")


async def main():
    await gather(start_cleanup(), torrent_search.initiate_search_tools(), restart_notification(), set_commands(bot))
    await sync_to_async(start_aria2_listener, wait=False)

    bot.add_handler(MessageHandler(
        start, filters=command(BotCommands.StartCommand)))
    bot.add_handler(MessageHandler(log, filters=command(
        BotCommands.LogCommand) & CustomFilters.sudo))
    bot.add_handler(MessageHandler(restart, filters=command(
        BotCommands.RestartCommand) & CustomFilters.sudo))
    bot.add_handler(MessageHandler(ping, filters=command(
        BotCommands.PingCommand) & CustomFilters.authorized))
    bot.add_handler(MessageHandler(bot_help, filters=command(
        BotCommands.HelpCommand) & CustomFilters.authorized))
    bot.add_handler(MessageHandler(stats, filters=command(
        BotCommands.StatsCommand) & CustomFilters.authorized))
    LOGGER.info("Selamat, Bot Anda Sudah Bisa Di Gunakan!")
    signal(SIGINT, exit_clean_up)

bot.loop.run_until_complete(main())
bot.loop.run_forever()
