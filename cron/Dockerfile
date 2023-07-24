FROM alpine:latest

WORKDIR /app

COPY trigger_recurring_sales.sh /app/trigger_recurring_sales.sh

RUN chmod +x /app/trigger_recurring_sales.sh

COPY create_reccurent_sale_document_cron /etc/cron.d/create_reccurent_sale_document_cron

RUN chmod 0644 /etc/cron.d/create_reccurent_sale_document_cron

CMD crond && tail -f /var/log/cron.log
