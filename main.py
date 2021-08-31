import csv
import time
import discord

d_token = ""


def get_all_students(student_list):
    mat_num_dict = {}
    with open(student_list, encoding="utf-8") as csv_file:
        data = csv.reader(csv_file, delimiter=";")
        next(data)  # skip 1 line
        for line in data:
            name = line[1]
            mat_num = line[2]
            mat_num_dict[name] = mat_num
    return mat_num_dict


def get_added_students():
    mat_num_list = []
    with open("added.txt", encoding="utf-8") as file:
        for line in file:
            mat_num_list.append(line.strip())
    return mat_num_list


def write_added_students(student):
    with open("added.txt", "a", encoding="utf-8") as file:
        file.write(f"{student}\n")


client = discord.Client()


@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = client.get_guild(payload.guild_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

    # only work if it is the client
    if payload.member.id == client.user.id:
        return

    # welcome message check
    if payload.message_id == 876478679876767824:
        if reaction.emoji == "🇪🇪":
            role = discord.utils.get(guild.roles, name='EE')
            await payload.member.add_roles(role)
        elif reaction.emoji == "🇬🇧":
            role = discord.utils.get(guild.roles, name='ENG')
            await payload.member.add_roles(role)
        elif reaction.emoji == "🇷🇺":
            role = discord.utils.get(guild.roles, name='RU')
            await payload.member.add_roles(role)

        # remove reaction
        await reaction.remove(payload.member)


@client.event
async def on_message(message):
    if message.author == client.user:
        if message.author.bot:
            return
        return

    channels_list = [881980743872565268, 881980719545585725, 881980694237184030, 881578607590408243]

    if message.channel.id in channels_list:

        msg_splitted = message.content.split("\n")

        # check message format
        if len(msg_splitted) == 2:

            # check name format
            if len(msg_splitted[1].split(" ")) >= 2:

                msg_code_uppered = msg_splitted[0].upper()

                if len(msg_code_uppered) == 10 and msg_code_uppered[6] == "I":
                    student_group = msg_code_uppered[6:]
                    students_list = get_all_students(f"{student_group}.csv")
                    added_students = get_added_students()

                    try:
                        if msg_code_uppered == students_list[msg_splitted[1]]:
                            if msg_code_uppered not in added_students:
                                write_added_students(msg_code_uppered)
                                user = message.author
                                await user.add_roles(discord.utils.get(user.guild.roles, name="Student"))
                                botmsg = await message.channel.send("Role added!")
                            else:
                                botmsg = await message.channel.send(
                                    "Your data was already used, please contact with administration!")
                        else:
                            botmsg = await message.channel.send("Student not found!")
                    except KeyError:
                        botmsg = await message.channel.send("Student not found!")
                else:
                    botmsg = await message.channel.send("Wrong student code format!")
            else:
                botmsg = await message.channel.send("Wrong name format!")
        else:
            botmsg = await message.channel.send("Wrong message format!")

        time.sleep(20)
        await message.delete()
        await botmsg.delete()


if __name__ == '__main__':
    print("SSC\nVersion: 0.9 Release\nCopyright (C) 2021 EblanSoftware\nRunning...\n")

    try:
        client.run(d_token)
    except discord.errors.LoginFailure:
        print("Error!\nPlease check your bot token settings!")
        input("Press Enter to continue")
