import time
from pygtail import Pygtail
import sys
import requests
import os

msg_for_discord = [
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

last_log_out = {}

logs_dir = '/logs/'

discord_url = os.getenv('DISCORD_URL')
admin_user = os.getenv('SERVER_ADMIN_DISCORD_ID')

log_in_out_timeout = 60  # Seconds
start_time = time.time()


def send_to_discord(msg):
    if (time.time() - start_time) < 10:
        # Wait for 10 seconds from program loading before we send anything to Discord
        # This will prevent the program from spamming chats when first loaded and pygtail is catching up
        print("Skipping sending: " + msg)
        return
    body = {
        'content': msg
    }
    req = requests.post(discord_url, data=body)
    print("Sending: " + format(body))


def is_msg_for_discord(msg):
    if msg[0] == "<":
        # In game message. Only return True if the message contains "note" (so that messages can be purposefully sent
        # to Discord
        words = msg.split(" ")
        return words[1] == "note"
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
    if len(msg) > 33:
        return msg[33:]


# Set the last_log_out for username to the current time
def left_the_game(msg):
    username = get_username(msg)
    if username is not None:
        last_log_out[username] = time.time()
    else:
        print("could not get username from left game msg")


def joined_the_game(msg):
    username = get_username(msg)
    if username is not None:
        last_log_out_time = last_log_out.get(username)
        if last_log_out_time is not None:
            if (time.time() - last_log_out_time) < log_in_out_timeout:
                # Is user has been logged out for less than log_in_out_timeout return without sending msg to discord
                return

    # Couldn't get username from joined msg, so print anyway
    send_to_discord(format_log_msg(msg))


def get_username(msg):
    trimmed_msg = format_log_msg(msg)
    words = trimmed_msg.split(" ")
    return words[0]


def clear_offset():
    if os.path.exists(logs_dir + "latest.log.offset"):
        os.remove(logs_dir + "latest.log.offset")
        print("offset file found and deleted")
    else:
        print("offset file not found - already deleted")


def read_log_file():
    try:
        for line in Pygtail(logs_dir + "latest.log"):
            sys.stdout.write(line)

            if "left the game" in line:
                left_the_game(line)
            elif "joined the game" in line:
                joined_the_game(line)
            elif is_msg_for_discord(format_log_msg(line)):
                send_to_discord(format_log_msg(line))
            elif is_server_info_msg(line):
                send_to_discord(admin_user + " " + format_log_msg(line))
    except OSError as err:
        print(format(err) + "an error occurred. waiting 5 seconds before trying again")
        clear_offset()
        time.sleep(5)


if discord_url is None or admin_user is None:
    print("env vars not set correctly")
else:
    while True:
        read_log_file()
