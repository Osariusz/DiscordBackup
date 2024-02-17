# DiscordBackup
Backs up all messages in a discord server with attachments!

## Limits:
- Can't backup more than 536,870,912 messages in a single channel (python array size limit for a 32-bit system i implemented in get_channel_messages method).
- Can't copy contents of forum channels (will implement them later)

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

## Variables

The currently working variables in this bot are stored as JSON files and work as follows:

### `allowed_users.json`
This is a list of user IDs that are allowed to execute commands.

### `backuped_categories.json`
This is a list of IDs for the categories that have been backed up.

### `backuped_channels.json`
This is a list of IDs for the channels that have been backed up.

### `timezone.json`
This is your timezone. It's used to ensure that timestamps and other time-related data are accurate for your location.
