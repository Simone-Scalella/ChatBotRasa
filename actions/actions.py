# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import mysql.connector as sql
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


'''class TellTime(Action):
    
    def name(self) -> Text:
        return "Hai utilizzato la funzione tell time"'''

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        '''dispatcher.utter_message(text="Hello World!")
        return []'''
        mydb = sql.connect(
        host="localhost",
        user="root",
        password="",
        database = "provasimone"
        )
        cursor = mydb.cursor()
        cursor.execute("Select nome_citta FROM citta where cittaID = 0")
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("Sorry we couldn't find Email in our database")
        else:
            dispatcher.utter_message("il risultato e': "+result[0])
        # dispatcher.utter_message(text="Hello World!")

        return []
