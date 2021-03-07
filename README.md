# Minecraft Discord Webhook

This docker image provides a webhook app that sends certain messages from a Minecraft server log file to a Discord webhook.

The current configuration sends a message when someone:

- Dies
- Makes an advancement
- Joins the server
- Exits the server

A message will also be sent to the channel when the server stops and starts, and if `SERVER_ADMIN_DISCORD_ID` is set will 
@ the given user/role. 

## Installation
This docker container can run on any machine that has a Minecraft Java server running also. It was implemented running
against this [Minecraft Docker Image](https://hub.docker.com/r/itzg/minecraft-server) and a future implementation may 
put running the server inside the docker-compose setup.

To setup the container all that is required is to clone the repo and run the command:

```docker-compose -f docker-compose.yaml up -d```

