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

nome_prod = ""

# Azione di validazione della form per l'acquisto di un prodotto
class ValidateProdottoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_prodotto_form"

    def validate_tipo_prodotto(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict):

        nome_prodotto=tracker.get_slot('tipo_prodotto').lower()
        query = 'SELECT DISTINCT name FROM mulino_bianco'

        cursor.execute(query)
        result = [row for [row] in cursor.fetchall()]

        print(result)
        print(nome_prodotto)
        if nome_prodotto not in result:
            dispatcher.utter_message(text="Non hai inserito un prodotto presente nel database")
            return {'tipo_prodotto': None}
        dispatcher.utter_message(text=f'Ok, hai scelto il prodotto {nome_prodotto}')
        return {'tipo_prodotto': nome_prodotto}

    def validate_dimensione_prodotto(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict):

        dimensione=tracker.get_slot('dimensione_prodotto').lower()
        query = 'SELECT quantity FROM mulino_bianco WHERE name = {tipo_prodotto}'

        cursor.execute(query,("tipo_prodotto",))
        result = [row for [row] in cursor.fetchall()]
        if dimensione not in result:
            print("validazione fallita")
            dispatcher.utter_message(text="Il valore della dimensione inserita non va bene")
            return {"dimensione_prodotto": None}
        print("validazione successa")
        dispatcher.utter_message(text=f"Ok, hai scelto la dimensione {dimensione}")
        return {"dimensione_prodotto": dimensione}
    
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
        query = 'INSER INTO acquisti (prodotto, dimensione) VALUES ({tipo_prodotto},{dimensione_prodotto})'

        cursor.execute(query)
        #'tipo_prodotto': None
        
        return [{"name":"dimensione_prodotto","event":"slot","value":None},{"name":"tipo_prodotto","event":"slot","value":None}]

# Azione che richiede di ripetere se il chatbot non ha capito
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

#Azione che permette di visualizzare il packaging di un dato prodotto
class GetPackagingFromDB(Action):
    def name(self) -> Text:
        return "action_packaging"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict):
        
        nome_prodotto=tracker.get_slot('prodotto').lower()
        query = 'SELECT packaging FROM mulino_bianco WHERE name=%s'

        cursor.execute(query,(nome_prodotto,))
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("Questo prodotto non esiste!")
        else:
            dispatcher.utter_message(text=f"Ecco a te il packaging di {nome_prodotto}: {result[0][0]}")

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

#Azione che permette di visualizzare lista dei brand
class GetBrand(Action):
    def name(self) -> Text:
        return "get_brand"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict):
        
        
        query = 'SELECT DISTINCT brands FROM mulino_bianco'

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("Non ci sono brand!")
        else:
            brd='I brand presenti sono: \n'
            buttons=[]
            for elem in result:
                brd=brd+f' - {elem[0]}\n'
                buttons.append({"title": elem[0], "payload": f'/viewBrandProduct{{"brand":"{elem[0]}"}}'})
            dispatcher.utter_button_message(brd,buttons)
            #dispatcher.utter_message(text=brd)

        return []

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []

#Azione che permette di visualizzare i prodotti di un brand
class GetProdottiBrand(Action):
    def name(self) -> Text:
        return "get_prodotti_brand"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict):
        
        appo=tracker.get_slot('brand').split('"')
        nome_brand=appo[3]
        query = 'SELECT name FROM mulino_bianco WHERE brands=%s'

        cursor.execute(query,(nome_brand,))
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("Questo brand non ha prodotti!")
        else:
            pb=f"Ecco i prodotti di {nome_brand}: \n"
            for elem in result:
                pb=pb+f' - {elem[0]}\n'
            dispatcher.utter_message(text=pb)
        #dispatcher.utter_message(text=nome_brand)
        return [{"name":"brand","event":"slot","value":None}]

#Azione che permette di visualizzare le merendine con meno di X calorie per porzione
class GetSnackCalLessFromDB(Action):
    def name(self) -> Text:
        return "get_snack_meno_cal"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict):
        
        cal_serSize=tracker.latest_message['entities'][0]['value']
        query = f'SELECT name, servin_size, energy_kcal_value FROM mulino_bianco WHERE energy_kcal_value<({cal_serSize}*100)/servin_size'

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("Non ci sono prodotti che rispettano questa condizione!")
        else:
            pl=f"I prodotti con medo di {cal_serSize} a porzione sono: \n"
            for elem in result:
                if not elem[0] in pl:
                    pl=pl+f' - {elem[0]}, porzione: {elem[1]}, kcal per porzione: {(elem[1]*elem[2])/100}\n'
            dispatcher.utter_message(text=pl)
        #dispatcher.utter_message(text=nome_brand)
        return [{"name":"calorie","event":"slot","value":None}]

# risultato
class RisultatoDellaRicerca(Action):
    def name(self) -> Text:
        return "query_result"

    def run(self,
            #slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        emptyQuery = True

        BasicQueryString = 'SELECT name,quantity,servin_size,category,ingredients FROM mulino_bianco WHERE '
        info_ingredienti=tracker.get_slot('info_ingredienti')
        if(len(info_ingredienti)>0 and info_ingredienti[0] != 'no'):
            emptyQuery = False
            regexStr = '\''
            for ingredienti in info_ingredienti:
                regexStr += ingredienti.lower()+'|'
        BasicQueryString += 'ingredients REGEXP ' + regexStr[:-1]+'\''

        info_serving=tracker.get_slot('info_serving')
        if(info_serving.lower() != 'no'):
            emptyQuery = False
            BasicQueryString += ' AND servin_size >=' + info_serving
        
        info_categoria=tracker.get_slot('info_categoria').lower()
        if(info_categoria != 'no'):
            emptyQuery = False
            BasicQueryString += ' AND category REGEXP \''+info_categoria+'\''
        
        info_quantity=tracker.get_slot('info_quantity')
        if(info_quantity.lower() != 'no'):
            emptyQuery = False
            BasicQueryString += ' AND quantity >= '+ info_quantity

        if(not emptyQuery):
            print(BasicQueryString)
            cursor.execute(BasicQueryString)
            result = cursor.fetchall()
            if len(result) == 0:
                dispatcher.utter_message("Non ci sono prodotti che rispettano questa condizione!")
            else:
                pl=f"I prodotti con la condizione proposta sono: \n"
                dispatcher.utter_message(text=pl)
                for elem in result:
                    pout=f' - {elem[0]}, quantita: {elem[1]}, servin size: {elem[2]}, categoria: {elem[3]}, ingredienti:{elem[4]}\n'
                    dispatcher.utter_message(text=pout)


        print("risultato query")
        return [{"name":"info_ingredienti","event":"slot","value":None},{"name":"info_serving","event":"slot","value":None},{"name":"info_categoria","event":"slot","value":None},{"name":"info_quantity","event":"slot","value":None}]


class ValidateProdottoInfoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_prodotto_info_form"

    def validate_info_ingredienti(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        print("validate info ingredienti")
        if(slot_value[0] == 'no' or slot_value[0] == 'skip'):
            print('skip slot')
            return {"info_ingredienti": ['no']}
        
        arrayfied = slot_value[0].replace(' ',',')
        arrayfied = arrayfied.split(',')
        arrayfied = list(filter(lambda x: len(x)>0,arrayfied))
        return {"info_ingredienti": arrayfied}

    def validate_info_serving(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        print("validate info serving")
        print(slot_value)
        if(slot_value == 'no' or slot_value == 'skip'):
            print('skip slot')
            return {"info_serving": 'no'}
        
        if (slot_value.isdigit()):
            return {'info_serving': slot_value}
        else:
            dispatcher.utter_message("Valore serving size non valido.")
            return {'info_serving': None}
    
    def validate_info_categoria(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        print("validate info categoria")
        print(slot_value)
        if(slot_value == 'no' or slot_value == 'skip'):
            print('skip slot')
            return {"info_categoria": 'no'}
        
        query = f'SELECT name,category FROM mulino_bianco WHERE category LIKE \'%{slot_value}%\''

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("la categoria non e' valida.")
            return {'info_categoria': None}

        return {'info_categoria': slot_value}
    
    def validate_info_quantity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        print("validate info quantity")
        print(slot_value)
        if(slot_value == 'no' or slot_value == 'skip'):
            print('skip slot')
            return {"info_quantity": 'no'}
        
        if (slot_value.isdigit()):
            return {'info_serving': slot_value}
        else:
            dispatcher.utter_message("Valore quantity non e' valido.")
            return {'info_serving': None}
