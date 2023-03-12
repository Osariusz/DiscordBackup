import json
from Message import Message
from Reaction import Reaction

class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if(isinstance(obj,Message)):
            return vars(obj.message_data)
        if(isinstance(obj,Reaction)):
            return vars(obj)
        return json.JSONEncoder.default(self,obj)