# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import mysql.connector as sql
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

Dimensioni = ['piccolo','media','grande']
Tipo = ['biscotti','merendine','taralli']

class ValidateProdottoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_prodotto_form"

    def validate_dimensione(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        if slot_value.lower() not in Dimensioni:
            dispatcher.utter_message(text='Il valore della dimensione inserita non va bene')
            return {'dimensione_prodotto': None}
        dispatcher.utter_message(text=f'Ok, tu hai scelto la dimensione {slot_value}')
        return {'dimensione_prodotto': {slot_value}}

    def validate_tipo(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        if slot_value.lower() not in Tipo:
            dispatcher.utter_message(text="Noi abbiamo: '{'/'.join(Tipo)}.")
            return {'tipo_prodotto': None}
        dispatcher.utter_message(text=f'Ok, tu hai scelto il prodotto del tipo {slot_value}')
        return {'tipo_prodotto': {slot_value}}
    



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
        host="5.135.165.96",
        user="chatbot",
        password="kaffeehouse",
        database = "chatbot"
        )
        cursor = mydb.cursor()
        cursor.execute("Select name FROM mulino_bianco where id = 1")
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("Sorry we couldn't find Email in our database")
        else:
            dispatcher.utter_message("il risultato e': "+result[0][0])
        # dispatcher.utter_message(text="Hello World!")

        return []

        '''result = db.query('Select nome_citta FROM citta where cittaID = 0')
        dispatcher.utter_message(result)
        return []'''
