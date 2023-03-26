import discord
import os

class Attachment:

    channel_file_limit = 100000

    def __init__(self, bot):
        self.bot = bot

    def copy_from_attachment(self, attachment: discord.Attachment):
        self.attachment = attachment
        self.filename = attachment.filename

    def to_json(self) -> dict:
        return {
            "filename" : self.filename
        }

    async def save_to_free_name(self, path):
        result = self.filename
        files_in_path = []
        for file in os.listdir(path):
            file_path = os.path.join(path,file)
            if(os.path.isfile(file_path)):
                files_in_path.append(file)
        if(self.filename in files_in_path):
            for i in range(self.channel_file_limit):
                split_filename = os.path.splitext(self.filename)
                new_filename = f"{split_filename[0]}{i}"
                if(len(split_filename)>0):
                    new_filename += split_filename[1]
                if(not new_filename in files_in_path):
                    result = new_filename
                    break
                
        if(result in files_in_path):
            raise Exception("All filenames taken")
        
        self.filename = result

        await self.attachment.save(os.path.join(path,self.filename))

        return result