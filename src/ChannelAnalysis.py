import datetime
import json
import os
from Channel import Channel
import pandas as pd
from CustomEncoder import CustomEncoder
from Message import Message
from VariableTypeEnum import VariableTypeEnum
from VarsManager import VarsManager

class ChannelAnalysis():

    def __init__(self, content_matters: bool = False):
        self.vars_manager = VarsManager()
        self.initialize_channel_analysis(content_matters)
        self.current_channels: list[int] | None = None

    def initialize_channel_analysis(self, content_matters: bool):
        self.channels_messages: dict[Channel, list[Message]] = {}
        for channel_id, channel_json in self.get_from_all_channels().items():
            channel: Channel = Channel(None, str(self.vars_manager.vars[VariableTypeEnum.BACKUP_PATH]))
            channel.id = int(channel_id)
            channel.load_messages(channel_json)

            if(not content_matters):
                def remove_message_content(msg: Message):
                    msg.message_data.content = ""
                    return msg
                channel.messages = [remove_message_content(msg) for msg in channel.messages]
                
            self.channels_messages[channel] = channel.messages
        self.initialize_messages_df()

    def get_from_all_channels(self) -> dict[str, str]:
        result: dict[str, str] = {}
        for root, dirs, files in os.walk(str(self.vars_manager.vars[VariableTypeEnum.BACKUP_PATH])):
            for file in files:
                name_split = os.path.splitext(file)
                root_split = root.split(os.sep)
                if(name_split[1] == ".json" and root_split[-1] == name_split[0]):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as json_file:
                            result[name_split[0]] = json_file.read()
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
        return result
        
    def initialize_messages_df(self):
        all_messages = []
        for channel, messages in self.channels_messages.items():
            for message in messages:
                message_json: str = json.dumps(message, cls=CustomEncoder)
                message_dict: dict = json.loads(message_json)
                message_dict['channel_id'] = channel.id
                all_messages.append(message_dict)
        self.messages_df = pd.DataFrame(all_messages)
        self.messages_df.loc[self.messages_df["pinned"] == False, "pinned"] = None
        self.messages_df.loc[self.messages_df["attachments"].str.len() == 0, "attachments"] = None

    def restrict_to_channels(self, channels_ids: list[int]):
        self.current_channels = channels_ids
    
    def set_content_matters(self, content_matters: bool):
        self.content_matters = content_matters

    def copy_messages_df_current_channels(self) -> pd.DataFrame:
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
        cleaned_df = self.copy_messages_df_current_channels()
        cleaned_df["created_at"] = pd.to_datetime(cleaned_df["created_at"], utc=True, format="%Y-%m-%d %H:%M:%S.%f%z", errors='coerce').fillna(
                pd.to_datetime(cleaned_df["created_at"], utc=True, format="%Y-%m-%d %H:%M:%S%z", errors='coerce')
            )
        cleaned_df["weekday"] = cleaned_df['created_at'].dt.weekday
        return cleaned_df.groupby("weekday").count()