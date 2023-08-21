import random
import time
import telegram
from telegram.ext import *
from telegram import Bot
import json
import configparser
import tracemalloc
import asyncio


tracemalloc.start()

config = configparser.ConfigParser()
config.read("config.ini")


Agent_TOKEN = '6144752816:AAGclS5JGsSzLMg1_f7dxkiWey3qeEzKBUg'
Bot_Status = config['Setting']['bot_status']
Post_keyword = config['Setting']['post_keyword']

print('Starting up bot...')


def is_admin(username):
    username = '@' + username
    f = open('admins.json')
    admins = json.load(f)
    if username in admins:
        return True
    else:
        return False

def add_admin_command(update,context):
    if is_admin(update.message.chat.username):
        f = open('admins.json')
        admins = json.load(f)
        args = context.args
        if args:
            username = args[0]
            if username not in admins:
                admins.append(username)
                with open('admins.json', 'w') as file:
                    file.write(json.dumps(admins) + '\n')
                    update.message.reply_text(f'User {username} added to admins!')
            else:
                update.message.reply_text('User is  already in the admins list')       
    
# Lets us use the /start command
def start_command(update, context):
    if is_admin(update.message.chat.username):
        update.message.reply_text('/start\n Shows this message again\n➖➖➖➖➖\n/setting\nShows your current setting\n➖➖➖➖➖\n/channels\nShows list of your channels\n➖➖➖➖➖\n/admins\nList of your admins\n➖➖➖➖➖\n/statistics\nShows a summary about your posts\n➖➖➖➖➖\n/show_posts\nShows the posts that has been saved\n➖➖➖➖➖\n/start_rp\nStart Reposting')

def show_setting_command(update, context):  
    if is_admin(update.message.chat.username):
        config = configparser.ConfigParser()
        config.read("config.ini")
        Post_keyword = config['Setting']['post_keyword']
        Bot_status = config['Setting']['bot_status']
        Agent_token = config['Setting']['agent_bot_token']
        if Bot_status == "True":
            Bot_Status = "Enabled"
        elif Bot_status == "False":
            Bot_Status = "Disabled"    
        update.message.reply_text(f"Bot status: \{Bot_status}\n✏️To Edit bot status, use this command:\n`/change\_status NEW_VALUE`\(0 or 1\)\n For Example: \n   `/change\_status 1`\n➖➖➖➖➖\npostKeyword \= \{Post_keyword}\n✏️To Edit post keyword, use this command:\n`/edit\_postkeyword NEW\_VALUE`\n For Example: \n   `/edit\_postkeyword playstaion`\n➖➖➖➖➖", parse_mode='MarkdownV2')
        update.message.reply_text("Agent bot token: ")
        update.message.reply_text(Agent_token)
        update.message.reply_text("✏️To Edit agent bot token\, use this command:\n`/edit\_agentbottoken NEW\_VALUE`\n For Example: \n   `/edit\_agentbottoken asgsngnasnkasf`", parse_mode='MarkdownV2')
def show_channels_command(update, context):
    if is_admin(update.message.chat.username):
        f = open('Channels.json')
        Channels_list = json.load(f)
        Channels_list_str = ""
        for i in range(len(Channels_list)):
            Channels_list_str += Channels_list[i]["username"] + "\n\n\t\t\tID:" + str(Channels_list[i]["id"])+ "\n\n\t\t\tPostInterval: " + str(Channels_list[i]["Interval"]) + " Seconds\n\n\t\t\tPost Delay: " + str(Channels_list[i]["Repost_delay"]) + "Minutes\n\n\n"
        update.message.reply_text(f"You have added {len(Channels_list)} channels \n Your Channels list:\n {Channels_list_str}")
        update.message.reply_text("Channel Commands:\n Add a Channel:\n\t\t To do so you can use the \(`/add_channel USERNAME`\) command\.For example:\n\t\t `/add_channel @fallen_shop`\n\n Edit Interval:\n\t\t To edit a channels interval you can use the \(`edit_interval USERNAME VALUE`\)\.For example:\n `/edit_interval @fallen_shop 15`\n\n Edit Repost Delay:\n To edit a channels repost delay you can use the \(`/edit_repost_delay USERNAME VALUE`\)\.For example:\n `/edit_repost_delay @fallen_shop 5`\tRrmove All Channels:\nTo remove all of the cahnnels use the command \(`/remove_all_channels`\)",parse_mode='MarkdownV2')

def add_channels_command(update, context) -> str:
    if is_admin(update.message.chat.username):
        f = open('Channels.json')
        Channels_list = json.load(f)
        Channels_username_list = []
        for i in range(len(Channels_list)):
            Channels_username_list.append(Channels_list[i]["username"])
        args = context.args
        if args:
            channel_username = args[0]
            if channel_username not in Channels_username_list:
                Channel = {
                'id': random.randint(0,9999999999999999999999),
                'username' : channel_username,
                'Interval': str(5), #Senconds
                'Repost_delay' : str(1), #Minutes
                }
                Channels_list.append(Channel)    
                with open('Channels.json', 'w') as file:
                    file.write(json.dumps(Channels_list) + '\n')
                f = open('posts.json')
                posts = json.load(f)
                for i in range(len(posts)):
                    if channel_username not in posts[i]['message_id'].keys():
                        posts[i]['message_id'][channel_username] = ''
                    with open('posts.json', 'w') as file:
                        file.write(json.dumps(posts) + '\n')
                update.message.reply_text("Cahnnel added!")
            else:
                update.message.reply_text("Cahnnel already exists!")
        else:
            update.message.reply_text("No Username provided")  

def remove_all_posts_command(update,context):
    if is_admin(update.message.chat.username):
        with open('posts.json', 'w') as file:
            file.write(json.dumps([]) + '\n')
    update.message.reply_text('All posts has benn deleted')    

def remove_all_channels_command(update,context):
    if is_admin(update.message.chat.username):
        with open('Channels.json', 'w') as file:
            file.write(json.dumps([]))
        f = open('posts.json')    
        posts = json.load(f)
        for i in range(len(posts)):
            posts[i]['message_id'] = {}
        with open('posts.json', 'w') as file:
            file.write(json.dumps(posts) + '\n')    
    update.message.reply_text('All channels has benn deleted') 

def remove_channel_command(update,context):
        if is_admin(update.message.chat.username):
            args = context.args
            if args:
                channel_username = args[0]
                f = open('Channels.json')
                Channels_list = json.load(f)
                print(Channels_list)
                file = open('posts.json')
                posts = json.load(file)
                for i in range(len(Channels_list)):
                    
                    if Channels_list[i]['username'] == channel_username:
                        Channels_list.pop(i)
                        for j in range(len(posts)):
                            del posts[j]['message_id'][channel_username]    
                        update.message.reply_text(f"Channel {channel_username} has been removed")
                        break
                with open('posts.json', 'w') as file:
                    file.write(json.dumps(posts) + '\n')    
                with open('Channels.json', 'w') as file:
                    file.write(json.dumps(Channels_list) + '\n')
                
def edit_post_keyword_command(update, context):
    if is_admin(update.message.chat.username):
        args = context.args
        if args:
            keyword = args[0]
            config.set("Setting", "post_keyword", keyword)
            with open("config.ini", "w") as configfile:
                config.write(configfile)
            update.message.reply_text(f"The Post Keyword has been updated to: {keyword}")
        else:
            print("No keyword provided")   

def edit_agent_bot_token_command(update, context):
    if is_admin(update.message.chat.username):
        args = context.args
        if args:
            bot_token = args[0]
            config.set("Setting", "agent_bot_token", bot_token)
            with open("config.ini", "w") as configfile:
                config.write(configfile)
            update.message.reply_text(f"The agent bot token has been updated to: \n {bot_token}")
        else:
            print("No token provided")  

async def send_message(channel,update):
    config = configparser.ConfigParser()
    config.read("config.ini")
    bot_token = config['Setting']['agent_bot_token']
    bot = Bot(token=bot_token)
    username = channel["username"]
    print(username)
    Interval = channel["Interval"]
    Repost_delay = channel["Repost_delay"]
    f = open('posts.json')
    data = json.load(f)
    for j in range(999999):
        # try:
            config.read("config.ini")
            Bot_Status = config['Setting']['bot_status']
            if Bot_Status == "True":
                for i in range(0, len(data)):
                        config = configparser.ConfigParser()
                        config.read("config.ini")
                        Bot_Status = config['Setting']['bot_status']
                        if Bot_Status != "True":
                            print("Bot has been disabled")
                            break
                        if data[i]["message_id"][username] != '':
                            try:
                                bot.delete_message(chat_id=username, message_id=data[i]["message_id"][username])
                            except:
                                pass   
                        # try:    
                        message = bot.send_message(chat_id=username, text=f"<code>#{data[i]['fid']}</code>\n{data[i]['message']}",parse_mode='HTML')
                        # except:
                        #     print(error)
                        #     pass
                        with open('posts.json') as file:
                            data = json.load(file)
                            data[i]["message_id"][username] = str(message.message_id)
                        with open('posts.json', 'w') as file:
                            file.write(json.dumps(data))

                        await asyncio.sleep(int(Interval)) 
                await asyncio.sleep(60*int(Repost_delay))     
            else:
                update.message.reply_text('Bot Disabled')
                break    
        # except:
        #     pass          
           
async def send_messages_to_channels(channels,update):
    tasks = []
    for channel in channels:
        task = asyncio.create_task(send_message(channel,update))
        tasks.append(task)
        await asyncio.sleep(int(channel["Repost_delay"]))
    await asyncio.gather(*tasks)

async def main(data,update):   
    await send_messages_to_channels(data,update)

def start_reposting_command(update, context):
    if is_admin(update.message.chat.username):
        config = configparser.ConfigParser()
        config.read("config.ini")
        Bot_Status = config['Setting']['bot_status']
        f = open('Channels.json')
        channels_list = json.load(f)
        if Bot_Status == "True":
            update.message.reply_text('Reposting Started!')
            asyncio.run(main(channels_list,update))   
        else:
            update.message.reply_text('Bot Disabled')
                
def change_status_command(update,context):
    if is_admin(update.message.chat.username):
        args = context.args
        if args:
            status = args[0]
            try:
                if status == str(1):
                        config.set("Setting", "bot_status", "True")
                        update.message.reply_text('Enabled!')
                        with open("config.ini", "w") as configfile:
                            config.write(configfile)
                elif status == str(0):
                    config.set("Setting", "bot_status", "False")
                    update.message.reply_text('Disabled!')
                    with open("config.ini", "w") as configfile:
                        config.write(configfile)
                else:
                    update.message.reply_text('Invalid Input for chaning the state of the Bot.(please enter between 0 and 1)')
            except:
                    print(error)
                    update.message.reply_text('Invalid Input for chaning the state of the Bot.(please enter between 0 and 1)شسبشسبش')
        else:
            update.message.reply_text("No status provided")

def handle_response(update, text) -> str:
    # Create your own response logic
    # with  open('karo.txt', 'w', encoding='utf-8') as file:
    #     file.write(text)
    if is_admin(update.message.chat.username):
        config = configparser.ConfigParser()
        config.read("config.ini")
        Post_keyword = config['Setting']['post_keyword']
        last_id = int(config['Setting']['last_post_id'])
        if Post_keyword.lower() in text or Post_keyword.upper() in text:
            f = open('Channels.json')
            channels_list = json.load(f)
            a = {}
            for i in range(0, len(channels_list)):
                a[channels_list[i]['username']] = ''

            config = configparser.ConfigParser()
            config.read("config.ini")
            Post_keyword = config['Setting']['post_keyword']
            f = open('posts.json')
            posts = json.load(f)
            last_id += 1
            data = {
                'fid': str(last_id),
                'message': text,
                'message_id' : a
            }
            config.set("Setting", "last_post_id", str(last_id))
            with open("config.ini", "w") as configfile:
                config.write(configfile)
            posts.append(data)
            with open('posts.json', 'w') as file:
                file.write(json.dumps(posts) + '\n')
            
            update.message.reply_text("message saved")
        else:     
            update.message.reply_text('I don\'t understand')
        
def handle_message(update, context: CallbackContext):
        # Get basic info of the incoming message
        if is_admin(update.message.chat.username):
            message_type = update.message.chat.type
            text = str(update.message.text)
            # Print a log for debugging
            # print(f'User ({update.message.chat.id}) says: "{text}" in: {message_type}')

            # React to group messages only if users mention the bot directly
            if message_type == 'group':
                # Replace with your bot username
                if '@bot19292bot' in text:
                    new_text = text.replace('@bot19292bot', '').strip()
                    handle_response(new_text)
            else:
                handle_response(update,text)



def show_posts_command(update, context):
    if is_admin(update.message.chat.username):
        f = open('posts.json')
        posts = json.load(f)
        f.close()  # Don't forget to close the file after reading it
        
        if not posts:
            update.message.reply_text("No post added!")
        else:
            for post in posts:
                update.message.reply_text(f"<code>#{post['fid']}</code>\n\n{post['message']}\n➖➖➖➖➖\n\n", parse_mode='HTML')

        update.message.reply_text('To remove a post use this command:\n`/remove_post ID` for example:\n`/remove_post #123456`\n\nTo remove all posts use this command:\n`/remove_all_posts`', parse_mode='MarkdownV2')


def remove_posts_commad(update,context):
    if is_admin(update.message.chat.username):
        args = context.args
        if args:
            posts_id = args[0].split('#')[-1]
            f = open('posts.json')
            posts = json.load(f)
            for i in range(len(posts)):
                if posts_id == posts[i]['fid']:
                    posts.pop(i)
                    update.message.reply_text('Posts deleted successfully')
                    break    
            with open('posts.json', 'w') as file:
                file.write(json.dumps(posts) + '\n')      


def edit_interval_command(update , context):
    if is_admin(update.message.chat.username):
        f = open('Channels.json')
        Channels_list = json.load(f)
        args = context.args
        if args:
            channel_username = args[0]
            new_interval = args[1]
            for channel in Channels_list:
                if channel['username'] == channel_username:
                    channel['Interval'] = str(new_interval)
                    with open('Channels.json', 'w') as file:
                        file.write(json.dumps(Channels_list) + '\n')
                    update.message.reply_text('Interval Chnged!')   

def edit_repost_delay_command(update , context):
    if is_admin(update.message.chat.username):
        f = open('Channels.json')
        Channels_list = json.load(f)
        args = context.args
        if args:
            channel_username = args[0]
            new_delay = args[1]
            for channel in Channels_list:
                if channel['username'] == channel_username:
                    channel['Repost_delay'] = str(new_delay)
                    with open('Channels.json', 'w') as file:
                        file.write(json.dumps(Channels_list) + '\n')
                    update.message.reply_text('Delay Chnged!')

def show_statics_command(update,context):
    if is_admin(update.message.chat.username):
        f = open('posts.json')
        posts = json.load(f)
        update.message.reply_text(f"You have {len(posts)} ready to repost!\n To remove all of the posts use the command(/remove_all_posts)")
# Log errors
def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Run the program1
if __name__ == '__main__':
    updater = Updater("6239735036:AAFrY2SmPsCrj389r1qYL2REvQIpSUC_dYc")
    dp = updater.dispatcher
    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('start_rp', start_reposting_command,run_async=True))
    dp.add_handler(CommandHandler('show_posts', show_posts_command))
    dp.add_handler(CommandHandler('change_status', change_status_command))
    dp.add_handler(CommandHandler('setting', show_setting_command))
    dp.add_handler(CommandHandler('edit_postkeyword', edit_post_keyword_command))
    dp.add_handler(CommandHandler('edit_agentbottoken', edit_agent_bot_token_command))
    dp.add_handler(CommandHandler('channels', show_channels_command))
    dp.add_handler(CommandHandler('add_channel', add_channels_command))
    dp.add_handler(CommandHandler('edit_interval', edit_interval_command))
    dp.add_handler(CommandHandler('edit_repost_delay', edit_repost_delay_command))
    dp.add_handler(CommandHandler('remove_channel', remove_channel_command))
    dp.add_handler(CommandHandler('add_admin', add_admin_command))
    dp.add_handler(CommandHandler('remove_all_posts', remove_all_posts_command))
    dp.add_handler(CommandHandler('remove_all_channels', remove_all_channels_command))
    dp.add_handler(CommandHandler('statistics', show_statics_command))
    dp.add_handler(CommandHandler('remove_post', remove_posts_commad))

    # Messages
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

    # Add a handler for the input command
    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()

