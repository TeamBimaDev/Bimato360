
rsync -avz -I --exclude='.git/*' . $1@$2:/home/$1/bima360/backend

ssh $1@$2 << EOF
cd /home/$1/bima360/backend/rabbitmq
docker-compose down
docker-compose build
docker-compose up -d
cd ..
docker-compose down
docker-compose build
docker-compose up -d
EOF