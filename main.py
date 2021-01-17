from time import sleep

from pygtail import Pygtail
import sys
import requests
import os

msg_for_discord = [
    "joined the game",
    "left the game",
    "made the advancement",
    # Death messages from https://minecraft.gamepedia.com/Death_messages
    "death",
    "slain",
    "fell",
    "shot",
    "starved",
    "killed",
    "was pummeled by",
    "drowned",
    "experienced kinetic energy",
    "blew up",
    "was blown up by",
    "was killed by",
    "hit the",
    "squashed",
    "squished",
    "flames",
    "fire",
    "burned",
    "burnt",
    "went off with a bang",
    "tried to swim",
    "was struck",
    "floor was lava",
    "danger zone",
    "was killed"
    "fell"
]

server_info_msg = [
    "Stopping server",
    "Starting the Minecraft server..."
]

logs_dir = '/logs/latest.log'
discord_url = os.getenv('DISCORD_URL')
admin_user = os.getenv('SERVER_ADMIN_DISCORD_ID')


def send_to_discord(msg):
    body = {
        'content': msg
    }
    req = requests.post(discord_url, data=body)


def is_msg_for_discord(msg):
    if msg[0] == "<":
        return False  # This is an in game message
    for for_discord in msg_for_discord:
        if for_discord in msg:
            return True
    return False


def is_server_info_msg(msg):
    for for_discord in server_info_msg:
        if for_discord in msg:
            return True
    return False


def format_log_msg(msg):
    if len(msg) > 31:
        return msg[31:]


def read_log_file():
    try:
        for line in Pygtail(logs_dir):
            sys.stdout.write(line)

            if is_server_info_msg(line):
                send_to_discord(admin_user + " " + format_log_msg(line))

            if is_msg_for_discord(line):
                send_to_discord(format_log_msg(line))
    except OSError as err:
        print(format(err) + "an error occurred. waiting 5 seconds before trying again")
        sleep(5)


if discord_url is None or admin_user is None:
    print("env vars not set correctly")
else:
    while True:
        read_log_file()

