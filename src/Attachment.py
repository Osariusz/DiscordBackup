import string
import discord
import os

class Attachment:

    channel_file_limit: int = 100000
    filename_length_limit: int = 255
    max_alphanumeric_filename_length: int = 3

    def __init__(self, bot):
        self.bot = bot

    def copy_from_attachment(self, attachment: discord.Attachment):
        self.attachment = attachment
        self.filename = attachment.filename

    def to_json(self) -> dict:
        return {
            "filename" : self.filename
        }

    def get_all_files_in_path(self, path):
        files_in_path = []
        for file in os.listdir(path):
            file_path = os.path.join(path,file)
            if(os.path.isfile(file_path)):
                files_in_path.append(file)
        return files_in_path
    
    def get_first_free_alphanumeric_filename(self, files_in_path: list[str], current_split_filename: tuple[str, str]) -> str | None:
        queue: list[str] = [""]
        alphanumeric_list = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
        while(len(queue) > 0):
            text: str = queue.pop()
            if(len(text) > self.max_alphanumeric_filename_length):
                return None
            for character in alphanumeric_list:
                new_text = text + character
                new_filename = new_text + current_split_filename[1]
                if(not new_filename in files_in_path):
                    return new_filename
                elif(len(new_text) <= self.max_alphanumeric_filename_length):
                    queue.append(new_text)
        return None

    async def save_to_free_name(self, path) -> str:
        result: str = self.filename
        files_in_path = self.get_all_files_in_path(path)
        split_filename: tuple[str, str] = os.path.splitext(self.filename)

        if(self.filename in files_in_path):
            for i in range(self.channel_file_limit):
                new_filename = f"{split_filename[0]}{i}"
                if(len(split_filename)>0):
                    new_filename += split_filename[1]
                if(not new_filename in files_in_path):
                    result = new_filename
                    break
                
        if(len(self.filename) > self.filename_length_limit):
            free_filename: str | None = self.get_first_free_alphanumeric_filename(files_in_path, split_filename)
            if(free_filename is not None):
                result = free_filename

        if(result in files_in_path):
            raise Exception("All filenames taken")
        
        self.filename = result

        await self.attachment.save(os.path.join(path,self.filename))

        return result