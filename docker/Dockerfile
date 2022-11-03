# syntax=docker/dockerfile:1
FROM alpine:latest

# Exposed Environment Variables
ENV DISCORD_BOT_SECRET=""
ENV MC_SERVER_IP="mc.popzi.net"
ENV MC_SERVER_PORT="25565"
ENV GITHUB_REPO_HTTPS="https://github.com/P0pzi/MC-PopziNet-Discord-Bot.git"

# Install software
RUN apk update
RUN apk add --no-cache python3
RUN apk add --no-cache git
RUN apk add --no-cache bash
RUN apk add --no-cache dos2unix
RUN apk add --no-cache nano

# Copy our start script and convert to dos
COPY start.sh /start.sh
RUN dos2unix /start.sh

# Make start script executable
RUN chmod +x /start.sh

ENTRYPOINT ["/bin/bash", "/start.sh"]
