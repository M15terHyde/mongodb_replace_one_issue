#FROM mongo:5.0.3
FROM mongo:5.0.5

VOLUME /var/lib/mongodb

# Give members of mongodb group ability to write to the database persistent storage directory.
RUN mkdir /var/lib/mongodb ; chown :mongodb /var/lib/mongodb ; chmod g+w /var/lib/mongodb

# Provide mongo configuration
COPY mongod.yaml /etc/mongod.conf

# No effect currently since ports are published in docker-compose.yml
EXPOSE 27017

USER mongodb

CMD ["mongod", "-f", "/etc/mongod.conf"]