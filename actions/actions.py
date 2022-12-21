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

# Connessione al database 
mydb = sql.connect(
        host="5.135.165.96",
        user="chatbot",
        password="kaffeehouse",
        database = "chatbot"
        )
cursor = mydb.cursor()

Dimensioni = ["piccolo","media","grande"]
Tipo = ["biscotti","merendine","taralli"]

# Azione di validazione della form per l'acquisto di un prodotto
class ValidateProdottoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_prodotto_form"

    def validate_dimensione_prodotto(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        print("validate dimensione prodotto")
        print(slot_value)
        if slot_value.lower() not in Dimensioni:
            print("validazione fallita")
            dispatcher.utter_message(text="Il valore della dimensione inserita non va bene")
            return {"dimensione_prodotto": None}
        print("validazione successa")
        dispatcher.utter_message(text=f"Ok, tu hai scelto la dimensione {slot_value}")
        return {"dimensione_prodotto": slot_value}

    def validate_tipo_prodotto(
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
        return {'tipo_prodotto': slot_value}
    
# Azione che effettua la submit di un acquisto
class SubmitAcquisto(FormValidationAction):
    def name(self) -> Text:
        return "submit_acquisto"

    def run(self,
            #slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Acquisto avvenuto con successo !!")
        #'tipo_prodotto': None
        
        return [{"name":"dimensione_prodotto","event":"slot","value":None},{"name":"tipo_prodotto","event":"slot","value":None}]

# Azione che richiede di ripetere se il charbot non ha capito
class NonHoCapito(Action):
    def name(self) -> Text:
        return "non_ho_capito"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Scusa puoi ripetere ? non ho capito quello che mi hai detto.")
        return []

#Azione che permette di visualizzare l'immagine di un dato prodotto
class GetImageFromDB(Action):
    def name(self) -> Text:
        return "get_image_from_db"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict):
        
        nome_prodotto=tracker.get_slot('prodotto').lower()
        query = 'SELECT image FROM mulino_bianco WHERE name=%s'

        cursor.execute(query,(nome_prodotto,))
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("Questo prodotto non esiste!")
        else:
            dispatcher.utter_message(text=f"Ecco a te un immagine di {nome_prodotto}:",image=result[0][0])

        return [{"name":"prodotto","event":"slot","value":None}]

#Azione che permette di visualizzare l'immagine di un dato prodotto
class GetCategorie(Action):
    def name(self) -> Text:
        return "action_categoria"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict):
        
        query = 'SELECT DISTINCT category FROM mulino_bianco'

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("Non ci sono categorie di prodotto!")
        else:
            cat='Le categorie di prodotti sono le seguenti: \n'
            for elem in result:
                cat=cat+f' - {elem[0]}\n'
            dispatcher.utter_message(text=cat)

        return []

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []