import discord
from asyncChatGPT.asyncChatGPT import Chatbot
import os
import json
# Discord の bot トークンを環境変数から取得する
bot_token = os.environ.get("DISCORD_BOT_TOKEN")

# DiscordBOT からの入力を受け取る
intents = discord.Intents.default()
# message_content インテントを有効にする
intents.message_content = True
client = discord.Client(intents=intents)

with open('config.json', 'r') as f:
    data = json.load(f)
config = {
    "email": data['email'],
    "password": data['password'],
}

chatbot = Chatbot(config, conversation_id=None)

@client.event
async def on_ready():
    # bot のログイン時にBOTのユーザー名を出力する
    print(f'{client.user}としてログインしました')

@client.event
async def on_message(message):
    # bot 自身が送信したメッセージは処理しない
    if message.author == client.user:
        return

    # メッセージが送信された場合、OpenAI の API を呼び出して返答する
    if message.content:
        # 入力されたメッセージをプロンプトとして使用する
        prompt = message.content
        response = await chatbot.get_chat_response(prompt)
        await message.channel.send(response["message"])
# bot トークンを使用して bot を起動する
client.run(bot_token)

