import discord
import sqlite3
from key import key


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.content.startswith('!') or message.content.startswith('§') or message.content.startswith('?') or message.content.startswith('^') or message.content.startswith('/'):
        print("message start with strange caratere, maybe a command")
        if message.content.startswith('!top_words'):
            if message.author.id == int(1083891932872319087):
                print("It's the bot")
            else:

                if len((message.content).split(" ")) == 2:
                    user_select = ((message.content).split(" ")[1]).strip("@<>")
                elif len((message.content).split(" ")) == 1:
                    user_select = message.author.id

                connexion = sqlite3.connect("base.db")
                cursor = connexion.cursor()

                cursor.execute('SELECT word, number_of_time FROM data WHERE user_id=? ORDER BY number_of_time DESC', (user_select,))
                rows = cursor.fetchall()

                if not rows:
                    await message.channel.send("Aucune donnée trouvée pour cet utilisateur.")
                    return

                message2 = f"Top mots utilisés par {message.author} :\n"
                for i, row in enumerate(rows):
                    message2 += f"{i+1}. {row[0]} ({row[1]} fois)\n"
                    if i == 9:
                        break

                await message.channel.send(message2)
    else:
        if message.author.id == int(1083891932872319087):
            print("It's the bot")
        else:
            connexion = sqlite3.connect("base.db")
            cursor = connexion.cursor()

            words = message.content.split(" ")
            for word in words:
                cursor.execute('SELECT * FROM data WHERE user_id=? AND word=?', (message.author.id, word))
                data = cursor.fetchone()
                if data:
                    new_count = data[2] + 1
                    cursor.execute('UPDATE data SET number_of_time=? WHERE user_id=? AND word=?',
                                   (new_count, message.author.id, word))
                else:
                    new_data = (message.author.id, word, 1)
                    cursor.execute('INSERT INTO data VALUES(?,?,?)', new_data)
                connexion.commit()


client.run(key())
