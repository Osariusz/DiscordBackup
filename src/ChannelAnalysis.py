import datetime
import json
import logging
import os
from Channel import Channel
import pandas as pd
from CustomEncoder import CustomEncoder
from Message import Message
from VariableTypeEnum import VariableTypeEnum
from VarsManager import VarsManager

class ChannelAnalysis():

    def __init__(self, content_matters: bool = False, message_df: pd.DataFrame | None = None):
        self.vars_manager = VarsManager()
        self.current_channels: list[int] | None = None
        if(message_df is None):
            self.initialize_channel_analysis(content_matters)
        else:
            self.messages_df = message_df

    def initialize_channel_analysis(self, content_matters: bool):
        logging.getLogger().info(f"Initializing channel analysis")
        if self.current_channels is None:
            self.current_channels = []
        self.channels_messages: dict[Channel, list[Message]] = {}
        for channel_path in self.get_all_channels():
            
            channel_file_name = channel_path.split(os.sep)[-1]
            channel_id = os.path.splitext(channel_file_name)[0]
            logging.getLogger().info(f"Loading channel {channel_id}")
            channel: Channel = Channel(None, str(self.vars_manager.vars[VariableTypeEnum.BACKUP_PATH])) 
            channel.id = int(channel_id)
            channel_json = ""

            try:
                with open(channel_path, 'r', encoding='utf-8') as json_file:
                    channel_json = json_file.read()
            except Exception as e:
                logging.getLogger().error(f"Error reading {channel_path}: {e}")

            if self.current_channels is None:
                self.current_channels.append(channel.id)
            channel.load_messages(channel_json)

            if(not content_matters):
                def remove_message_content(msg: Message):
                    msg.message_data.content = ""
                    return msg
                channel.messages = [remove_message_content(msg) for msg in channel.messages]

            self.channels_messages[channel] = channel.messages
        self.initialize_messages_df()
        logging.getLogger().info(f"Initialized channel analysis")

    def get_all_channels(self) -> list[str]:
        logging.getLogger().info(f"Getting from all channels")
        result: list[str] = []
        for root, dirs, files in os.walk(str(self.vars_manager.vars[VariableTypeEnum.BACKUP_PATH])):
            for file in files:
                name_split = os.path.splitext(file)
                root_split = root.split(os.sep)
                if(name_split[1] == ".json" and root_split[-1] == name_split[0]):
                    file_path = os.path.join(root, file)
                    result.append(file_path)
        logging.getLogger().info(f"Got from all channels")
        return result
        
    def initialize_messages_df(self):
        logging.getLogger().info(f"Initializing messages df")
        message_generator = (
            {**json.loads(json.dumps(message, cls=CustomEncoder)), 'channel_id': channel.id}
            for channel, messages in self.channels_messages.items()
            for message in messages
        )

        self.messages_df = pd.DataFrame(message_generator)
        self.messages_df.loc[self.messages_df["pinned"] == False, "pinned"] = None
        self.messages_df.loc[self.messages_df["attachments"].str.len() == 0, "attachments"] = None
        logging.getLogger().info(f"Initialized messages df")

    def restrict_to_channels(self, channels_ids: list[int]):
        self.current_channels = channels_ids
    
    def set_content_matters(self, content_matters: bool):
        self.content_matters = content_matters

    def copy_messages_df_current_channels(self) -> pd.DataFrame:
        logging.getLogger().info(f"Copying messages from current channels")
        new_df = self.messages_df.copy()
        if(self.current_channels is None):
            return new_df
        return new_df[new_df["channel_id"].isin(self.current_channels)]

    # All operations should be done on copy_messages_df_current_channels
    def number_of_messages(self) -> int:
        return len(self.copy_messages_df_current_channels())
    
    def number_of_messages_per_channel(self):
        cleaned_df = self.copy_messages_df_current_channels()
        return cleaned_df.groupby("channel_id").count()
    
    def weekday_number_of_messages(self):
        logging.getLogger().info(f"Getting number of messages by week day")
        cleaned_df = self.copy_messages_df_current_channels()
        cleaned_df["created_at"] = pd.to_datetime(cleaned_df["created_at"], utc=True, format="%Y-%m-%d %H:%M:%S.%f%z", errors='coerce').fillna(
                pd.to_datetime(cleaned_df["created_at"], utc=True, format="%Y-%m-%d %H:%M:%S%z", errors='coerce')
            )
        cleaned_df["weekday"] = cleaned_df['created_at'].dt.weekday
        return cleaned_df.groupby("weekday").count()
    
    def strftime_number_of_messages(self, strftime: str):
        logging.getLogger().info(f"Getting number of messages by day")
        cleaned_df = self.copy_messages_df_current_channels()
        cleaned_df["created_at"] = pd.to_datetime(cleaned_df["created_at"], utc=True, format="%Y-%m-%d %H:%M:%S.%f%z", errors='coerce').fillna(
                pd.to_datetime(cleaned_df["created_at"], utc=True, format="%Y-%m-%d %H:%M:%S%z", errors='coerce')
            ).dt.date
        #cleaned_df.sort_values(by="created_at")
        #cleaned_df["created_at"] = cleaned_df["created_at"].dt.strftime("%d.%m.%Y")
        return cleaned_df

    def day_number_of_messages(self):
        logging.getLogger().info(f"Getting number of messages by day")
        cleaned_df = self.copy_messages_df_current_channels()
        cleaned_df["created_at"] = pd.to_datetime(cleaned_df["created_at"], utc=True, format="%Y-%m-%d %H:%M:%S.%f%z", errors='coerce').fillna(
                pd.to_datetime(cleaned_df["created_at"], utc=True, format="%Y-%m-%d %H:%M:%S%z", errors='coerce')
            ).dt.date
        #cleaned_df.sort_values(by="created_at")
        #cleaned_df["created_at"] = cleaned_df["created_at"].dt.strftime("%d.%m.%Y")
        return cleaned_df