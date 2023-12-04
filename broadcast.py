from pyrogram import Client, filters
from pyrogram.errors import InputUserDeactivated, UserIsBlocked, FloodWait
import datetime
import time
from database.users_chats_db import db
from info import ADMINS
#from utils import broadcast_messages
import asyncio

        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def _private_broadcast(bot, message):
    if message.reply_to_message:
        users = await db.get_all_users()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        async for user in users:
            try:
                await broadcast_msg.copy(user["id"])
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await broadcast_msg.copy(user["id"])
                successful += 1
            except UserIsBlocked:
                await db.delete_user(user["id"])
                blocked += 1
            except InputUserDeactivated:
                await db.delete_user(user["id"])
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply("<code>Use this command as a replay to any telegram message with out any spaces.</code>")
        await asyncio.sleep(8)
        await msg.delete()