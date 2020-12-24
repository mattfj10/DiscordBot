
import discord
import random
import asyncio
from googletrans import Translator
import requests
import json

translator = Translator()

class MyClient(discord.Client):

   # @client.event
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

   # @client.event
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$guess'):
            await message.channel.send('Guess a number between 1 and 10.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Sorry, you took too long it was {}.'.format(answer))

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send('Oops. It is actually {}.'.format(answer))

        if message.content.startswith('$translate'):
            text = message.content.split()
            text.pop()

            if(len(text) == 0):
                return await message.channel.send("You didn't include any text after the translation identifier, please try again!")
            
            translation = translator.translate(text, dest='en')
            return await message.channel.send("The translation is: {}".format(translation))

        if message.content.startswith('$puggo'):
            response = requests.get("https://dog.ceo/api/breed/pug/images/random")
            response_json = json.loads(response.text)
            return await message.channel.send(response_json["message"])

        if message.content.startswith('$PUGBOMB'):
            await message.channel.send("PUG BOMB INCOMING!!!")
            for i in range(0, 100):
                response = requests.get("https://dog.ceo/api/breed/pug/images/random")
                response_json = json.loads(response.text)
                await message.channel.send(response_json["message"])





client = MyClient()
with open("token.txt") as token:
    client.run(token.read())
