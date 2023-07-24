FROM rabbitmq:3.8-management

ENV RABBITMQ_DEFAULT_USER=bimauser
ENV RABBITMQ_DEFAULT_PASS=bimapass

COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

EXPOSE 15672
EXPOSE 5672