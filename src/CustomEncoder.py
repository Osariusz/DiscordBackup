import json
from Message import Message
from Reaction import Reaction
from Attachment import Attachment

class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if(isinstance(obj,Message)):
            return vars(obj.message_data)
        if(isinstance(obj,Reaction)):
            return vars(obj)
        if(isinstance(obj,Attachment)):
            return obj.to_json()
        return json.JSONEncoder.default(self,obj)