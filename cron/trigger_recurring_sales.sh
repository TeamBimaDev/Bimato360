#!/bin/sh

echo "Task started at $(date)" >> /var/log/cron.log

URL="http://51.83.40.92:8500/api/erp/sale_document/generate_recurring_sale_documents"

AUTHORIZATION_TOKEN="${AUTHORIZATION_TOKEN}"

echo "Hitting URL: $URL" >> /var/log/cron.log

curl -X GET -H "Authorization: $AUTHORIZATION_TOKEN" "$URL"

echo "Task completed at $(date)" >> /var/log/cron.log
