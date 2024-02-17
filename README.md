# DiscordBackup
Backs up all messages in a discord server with attachments!

## Slash Commands

### `/add_channel [channel_id]`
Adds a channel to the list of channels for backup. If no `channel_id` is provided, the current channel is added.

### `/remove_channel [channel_id]`
Removes a channel from the list of channels for backup. If no `channel_id` is provided, the current channel is removed.

### `/list_channels`
Lists all backed up channels by their IDs.

### `/list_channels_names`
Lists all backed up channels by their names.

### `/backup_channels`
Starts the backup process. This command retrieves all messages and media from the backed up channels and outputs them into a local folder.
