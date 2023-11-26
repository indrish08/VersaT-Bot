FROM ubuntu:16.04

WORKDIR /app

RUN apt-get update
# RUN apt-get install curl htop git zip nano ncdu build-essential chrpath libssl-dev libxft-dev pkg-config glib2.0-dev libexpat1-dev gobject-introspection python-gi-dev apt-transport-https libgirepository1.0-dev libtiff5-dev libjpeg-turbo8-dev libgsf-1-dev fail2ban nginx -y

# Install Rclone
RUN curl -sL https://rclone.org/install.sh | bash
RUN rclone version

# Cleanup
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y