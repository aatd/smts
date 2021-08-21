FROM balenalib/raspberry-pi-debian:latest

# Install required packages
RUN apt-get update && apt-get -y dist-upgrade && apt-get install mongodb

# Volumes
VOLUME ["/docker-shares"]
VOLUME ["/var/lib/mongodb"]
VOLUME ["/data/db"]

# Define default command.
CMD ["mongod"]

# Expose ports.
EXPOSE 27017
EXPOSE 28017

ENTRYPOINT /usr/bin/mongod
