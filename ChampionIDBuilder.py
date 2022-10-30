from cgitb import reset
import json
import os

class DartFileBuilder:
    def dictToDartEnumString(self, dataDict):
        result = ""
        for key in dataDict:
            result += f"@JsonValue({dataDict[key]})\n"
            result += f"{key.lower()},\n"
        if len(result) > 0:
            result = result[:len(result) - 1]
        return result 

    def makeDartEnumFileString(self, entityName, enumString):
        dartFile = f"""import 'package:json_annotation/json_annotation.dart';

enum {entityName} {{
{enumString}
}}
            """
        
        with open(f"./{entityName}.dart", "w") as file:
            file.write(dartFile) 

class ChampionIDBuilder:
    championIDDict = {}

    def __init__(self):
        pass

    def setData(self, jsonData):
        data = jsonData["data"]
        for championKey in data:
            championID = data[championKey]["key"]
            self.championIDDict[championKey] = championID

class JSONManager:
    def save_json(self, json_data, file_name, directory_name="."):
        os.makedirs(directory_name, exist_ok=True)
        with open(f"{directory_name}/{file_name}", "w") as json_file:
            json.dump(json_data, json_file)
    
    def load_json(self, file_name, directory_name="."):
        with open(f"{directory_name}/{file_name}", "r") as json_file:
            print(f"{directory_name}/{file_name}")
            data = json.load(json_file)
            return data

jsonManager = JSONManager()
builder = ChampionIDBuilder()

rawChampionJsonData = jsonManager.load_json("rawChampion.json")
builder.setData(rawChampionJsonData)
jsonManager.save_json(builder.championIDDict, "champion.json")

dartFileBuilder = DartFileBuilder()
enumString = dartFileBuilder.dictToDartEnumString(builder.championIDDict)
dartFileBuilder.makeDartEnumFileString("Champion", enumString)

