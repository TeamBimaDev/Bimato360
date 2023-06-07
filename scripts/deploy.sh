
rsync -avz -I --exclude='.git/*' . $1@$2:/home/$1/bima360/backend

ssh $1@$2 << EOF
cd /home/$1/bima360/backend
docker-compose down
docker-compose build --no-cache
docker-compose up -d
EOF