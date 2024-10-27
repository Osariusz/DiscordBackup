import json
import os
from Channel import Channel
import pandas as pd
from CustomEncoder import CustomEncoder
from Message import Message
from VariableTypeEnum import VariableTypeEnum
from VarsManager import VarsManager

class ChannelAnalysis():

    def __init__(self):
        self.vars_manager = VarsManager()
        self.initialize_channel_analysis()

    def initialize_channel_analysis(self):
        self.channels_messages: dict[Channel, list[Message]] = {}
        for channel_id, channel_json in self.get_from_all_channels().items():
            channel: Channel = Channel(None, str(self.vars_manager.vars[VariableTypeEnum.BACKUP_PATH]))
            channel.id = int(channel_id)
            channel.load_messages(channel_json)
            self.channels_messages[channel] = channel.messages
        self.initialize_messages_df()

    def get_from_channel_id(self, channel_id: str) -> str:
        filename = f"{channel_id}.json"
        
        for root, dirs, files in os.walk(str(self.vars_manager.vars[VariableTypeEnum.BACKUP_PATH])):
            if filename in files:
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        return json_file.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    return ""
        
        print(f"File {filename} not found")
        return ""
    
    def get_from_all_channels(self) -> dict[str, str]:
        result: dict[str, str] = {}
        for root, dirs, files in os.walk(str(self.vars_manager.vars[VariableTypeEnum.BACKUP_PATH])):
            for file in files:
                name_split = os.path.splitext(file)
                if(name_split[1] == ".json"):
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

    # All operations should be done on messages_df
    def number_of_messages(self) -> int:
        return len(self.messages_df)
    
    def number_of_messages_per_channel(self) -> dict[int, int]:
        cleaned_df = self.messages_df
        cleaned_df.loc[cleaned_df["pinned"] == False, "pinned"] = None
        cleaned_df.loc[cleaned_df["attachments"].str.len() == 0, "attachments"] = None
        return cleaned_df.groupby("channel_id").count()