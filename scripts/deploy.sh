
scp -r . $1@$2/home/ubuntu/bima360/backend

ssh $1@$2 << EOF
cd /home/ubuntu/bima360/backend
docker-compose down
docker-compose build --no-cache
docker-compose up
EOF