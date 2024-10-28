. src/.env
docker build -t discord-backup .
docker run -d -v $MOUNT_PATH:$BACKUP_PATH discord-backup
