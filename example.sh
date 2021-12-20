#!/bin/sh
# Run docker in background
docker-compose up --detach

# check status=running
running="$(docker-compose ps --services --filter "status=running")"

# check all services
services="$(docker-compose ps --services)"

while [ "$running" != "$services" ]; do
  echo "Waiting for all services are running..."
  sleep 5s
  running="$(docker-compose ps --services --filter "status=running")"
  services="$(docker-compose ps --services)"
done

# Just to prevent from virtual running status.
sleep 5s
running="$(docker-compose ps --services --filter "status=running")"
services="$(docker-compose ps --services)"

if [ "$running" != "$services" ]; then
  echo "Following services are running..."
  # Bash specific
  echo $running
else
  echo "All services are running..."
fi

python -m venv venv
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  source venv/bin/activate
elif [[ "$OSTYPE" == "msys" ]]; then
  .\\venv\\Scripts\\activate
else
  exit 1
fi

pip install pika
eval $(cat .env.dev | sed 's/^/export /')
python example.py
rm -rf venv
docker-compose down
