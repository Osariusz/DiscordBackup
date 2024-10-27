import datetime
import shutil
from time import sleep
from tokenize import String
import discord
from Channel import Channel
from OwnerCog import OwnerCog
from discord.ext import commands
import asyncio
import os
import json
from Category import Category
import logging
from enum import Enum
from VariableTypeEnum import VariableTypeEnum

class VarsManager():

    def __init__(self):
        self.vars: dict[str, object] = {}
        self.initialize_var_files()
        self.load_vars()

    def initialize_var_files(self):
        for file in os.listdir("vars"):
            file = os.path.join("vars", file)
            real_file_name: str = file.replace(".example", "")
            if(file.endswith(".example") and not os.path.exists(real_file_name)):
                shutil.copy(file, real_file_name)

    def load_vars(self):
        required_vars = [VariableTypeEnum.ALLOWED_USERS, VariableTypeEnum.TIMEZONE]
        for var in [file[0:file.find(".json")] for file in os.listdir("vars") if os.path.isfile(os.path.join("vars",file))]:
            try:
                var_path = os.path.join("vars",f"{var}.json")
                if(os.path.isfile(var_path)):
                    with open(var_path,"r",encoding="utf-8") as file:
                        self.vars[var.replace(".json","")] = json.load(file)
            except Exception as e:
                logging.getLogger().error(str(e))
        for required_var in required_vars:
            if(not required_var in self.vars):
                logging.getLogger().error(f"Var {required_var} not present in var dictionary!")
        logging.getLogger().info("Vars loaded")

    def update_var(self, name : str):
        if(not name in self.vars):
            logging.getLogger().error(f"Can't update var {name} as it is not present in the dictionary!")
            return
        var_path = os.path.join("vars",f"{name}.json")
        if(os.path.isfile(var_path)):
            with open(var_path, "w", encoding="utf-8") as file:
                file.write(json.dumps(self.vars[name]))