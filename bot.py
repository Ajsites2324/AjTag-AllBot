import os, logging, asyncio

from telegraph import Telegraph, upload_file, exceptions
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.events import NewMessage



logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

moment_worker = []


#start
@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("^_^ Hey, Welcome To TAG Help Bot's Menu\nI can tag 15,000 Members in Group and 300 Members In Channel.\nNeed Help /help ",
                    buttons=(
                      [
                         Button.url('📣 𝐔𝐏𝐃𝐀𝐓𝐄𝐒', 'https://t.me/THE_PROFESSOR_NETWORK'), 
                         Button.url('⭐𝐒𝐔𝐏𝐏𝐎𝐑𝐓', 'https://t.me/TPN_CHATROOM'), 
                      ], 
                      [
                        Button.url('➕𝐀𝐃𝐃 𝐌𝐄 𝐓𝐎 𝐘𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏➕ ', 'https://t.me/MEMBER_TAGERBOT?startgroup=true'),   
                      ]
                   ), 
                    link_preview=False
                   )

#help
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Tag Help Bot's Help Menu**\n\nCommand: /all \n You can use this command with text you want to tell others. \n`Example: /all Good morning!` \nYou can use this command as an answer. any message Bot will tag users to replied message"
  await event.reply(helptext,
                    buttons=(
                      [
                         Button.url('📣 𝐔𝐏𝐃𝐀𝐓𝐄𝐒', 'https://t.me/THE_PROFESSOR_NETWORK'), 
                         Button.url('⭐𝐒𝐔𝐏𝐏𝐎𝐑𝐓', 'https://t.me/TPN_CHATROOM'), 
                      ], 
                      [
                        Button.url('➕𝐀𝐃𝐃 𝐌𝐄 𝐓𝐎 𝐘𝐎𝐔𝐑 𝐆𝐑𝐎𝐔𝐏➕', 'https://t.me/MEMBER_TAGERBOT?startgroup=true'),   
                      ]
                   ), 
                    link_preview=False
                   )

#Wah bhaiya full ignorebazzi

#bsdk credit de dena verna maa chod dege

#tag
@client.on(events.NewMessage(pattern="^/tagall|/call|/tall|/all|#all|@all?(.*)"))
async def mentionall(event):
  global moment_worker
  if event.is_private:
    return await event.respond("Use This In Channel or Group!")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("Only Admin can use it.")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("I can't Mention Members for Old Post!")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Give me can an Argument. Ex: `/tag Hey, Where are you`")
  else:
    return await event.respond("Reply to Message or Give Some Text To Mention!")
    
  if mode == "text_on_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("Stopped!")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    moment_worker.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("Stopped")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


#yaha kuch kachra tha ya fr extra features 🥲🥲removed now

print("Started Successfully Join Support")
print("¯\_(ツ)_/¯ Need Help Join @The_Professor_Network")
client.run_until_disconnected()
