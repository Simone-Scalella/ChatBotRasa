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

        #print(result)
        print(nome_prodotto)
        if nome_prodotto not in result:
            dispatcher.utter_message(text="prodotto inesistente")
            return {'tipo_prodotto': None}
        dispatcher.utter_message(text=f'Ok, hai scelto il prodotto {nome_prodotto}')
        return {'tipo_prodotto': nome_prodotto}

    def validate_dimensione_prodotto(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict):

        dimensione=tracker.get_slot('dimensione_prodotto')
        tipo_prodotto = tracker.get_slot('tipo_prodotto').lower()
        query = f'SELECT quantity FROM mulino_bianco WHERE name = \'{tipo_prodotto}\''
        cursor.execute(query)
        result = [row for [row] in cursor.fetchall()]
        if dimensione not in result:
            print("validazione fallita")
            dispatcher.utter_message(text="Il valore della dimensione inserita non va bene")
            validStr = ''
            for content in result:
                validStr += content+','
            dispatcher.utter_message(text="I valori ammissibili sono: "+validStr[:-1])
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
        
        tipo_prod = tracker.get_slot('tipo_prodotto')
        dim_prod = tracker.get_slot('dimensione_prodotto')
        query = "INSERT INTO acquisti (prodotto, dimensione) VALUES (%s,%s);"
        try:
            cursor.execute(query,(tipo_prod,dim_prod))
            mydb.commit()
            dispatcher.utter_message(text="Acquisto avvenuto con successo !!")
        except:
            dispatcher.utter_message(text="Errore database")
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
            pl=f"I prodotti con meno di {cal_serSize} a porzione sono: \n"
            for elem in result:
                if not elem[0] in pl:
                    pl=pl+f' - {elem[0]}, porzione: {elem[1]}, kcal per porzione: {(elem[1]*elem[2])/100}\n'
            dispatcher.utter_message(text=pl)
        #dispatcher.utter_message(text=nome_brand)
        return [{"name":"calorie_slot","event":"slot","value":None}]


# risultato delle informazioni prodotti
class RisultatoDellaRicerca(Action):
    def name(self) -> Text:
        return "query_result"

    def run(self,
            #slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        emptyQuery = True
        beofore = False
        BasicQueryString = 'SELECT name,quantity,servin_size,category,ingredients FROM mulino_bianco WHERE '
        info_ingredienti=tracker.get_slot('info_ingredienti')
        if(len(info_ingredienti)>0 and info_ingredienti[0] != 'no'):
            emptyQuery = False
            beofore = True
            regexStr = '\''
            for ingredienti in info_ingredienti:
                regexStr += ingredienti.lower()+'|'
            BasicQueryString += 'ingredients REGEXP ' + regexStr[:-1]+'\''

        info_serving=tracker.get_slot('info_serving')
        if(info_serving.lower() != 'no'):
            emptyQuery = False
            if(beofore):
                BasicQueryString += ' AND servin_size >=' + info_serving
            else:
                BasicQueryString += 'servin_size >=' + info_serving
            beofore = True

        
        info_categoria=tracker.get_slot('info_categoria').lower()
        if(info_categoria != 'no'):
            emptyQuery = False
            if(beofore):
                BasicQueryString += ' AND category REGEXP \''+info_categoria+'\''
            else:
                BasicQueryString += ' category REGEXP \''+info_categoria+'\''
            beofore = True

            
        
        info_quantity=tracker.get_slot('info_quantity')
        if(info_quantity.lower() != 'no'):
            emptyQuery = False
            if(beofore):
                BasicQueryString += ' AND quantity >= '+ info_quantity
            else:
                BasicQueryString += ' quantity >= '+ info_quantity
            beofore = True

            

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

#Validazione informazione prodotti
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
            return {'info_quantity': slot_value}
        else:
            dispatcher.utter_message("Valore quantity non e' valido.")
            return {'info_quantity': None}

# Azione di validazione della form per l'acquisizione degli allergeni dell'utente
class ValidateAllergeniForm(FormValidationAction):

# Prendo tutti i prodotti presenti nel db e proseguo eliminando i risultati non essenziali

    def name(self) -> Text:
        return "validate_allergeni_form"

    def validate_allergeni_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        print("validate allergene")
        print(slot_value)
        if(slot_value == 'no' or slot_value == 'skip'):
            print('skip slot')
            dispatcher.utter_message("A che tipo di ingredienti sei interessato? Puoi rispondere skip, o no, se non ti interessa il filtro su questo campo")
            return {"allergeni_slot": 'no'}
        
        query = f'SELECT name,allergens FROM mulino_bianco WHERE allergens LIKE \'%{slot_value}%\''

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("L'allergene non è presente nei nostri prodotti"+"\n")
            dispatcher.utter_message("A che tipo di ingredienti sei interessato ? Puoi rispondere skip, o no, se non ti interessa il filtro su questo campo")
            return {'allergeni_slot': 'no'}
            
        dispatcher.utter_message("A che tipo di ingredienti sei interessato ? Puoi rispondere skip, o no, se non ti interessa il filtro su questo campo")
        return {'allergeni_slot': slot_value}

    def validate_ingrediente_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        print("validate info ingredienti")
        if(slot_value[0] == 'no' or slot_value[0] == 'skip'):
            print('skip slot')
            dispatcher.utter_message("Quante calorie deve contenere al massimo ? Puoi rispondere skip, o no, se non interessa il filtro su questo campo")
            return {"ingrediente_slot": ['no']}
        
        arrayfied = slot_value[0].replace(' ',',')
        arrayfied = arrayfied.split(',')
        arrayfied = list(filter(lambda x: len(x)>0,arrayfied))
        dispatcher.utter_message("Quante calorie deve contenere al massimo ? Puoi rispondere skip o no se non interessa il filtro su questo campo")
        return {"ingrediente_slot": arrayfied}

    def validate_calorie_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        print("validate calorie")
        print(slot_value)
        if(slot_value == 'no' or slot_value == 'skip'):
            print('skip slot')
            dispatcher.utter_message("A che prodotto sei interessato ? Puoi rispondere skip, o no, se non ti interessa il filtro su questo campo")
            return {"calorie_slot": 'no'}
        
        if (slot_value.isdigit()):
            dispatcher.utter_message("A che prodotto sei interessato ? Puoi rispondere skip, o no, se non ti interessa il filtro su questo campo")
            return {'calorie_slot': slot_value}
        else:
            dispatcher.utter_message("Il valore delle calorie non e' valido.")
            return {'calorie_slot': None}

    def validate_prodotto_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        print("validate prodotto")
        print(slot_value)
        if(slot_value == 'no' or slot_value == 'skip'):
            print('skip slot')
            return {"prodotto_slot": 'no'}
        
        query = f'SELECT name FROM mulino_bianco WHERE name LIKE \'%{slot_value}%\''

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            dispatcher.utter_message("Il nome del prodotto richiesto non è presente")
            return {'prodotto_slot': None}

        return {'prodotto_slot': slot_value}



    
# Azione che effettua la submit di un acquisto
class SubmitAllergeni(FormValidationAction):
    def name(self) -> Text:
        return "submit_allergeni"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        emptyQuery = True
        beofore = False
        BasicQueryString = 'SELECT name,ingredients,energy_kcal_value,allergens FROM mulino_bianco WHERE '
        info_ingredienti=tracker.get_slot('ingrediente_slot')
        if(len(info_ingredienti)>0 and info_ingredienti[0] != 'no'):
            emptyQuery = False
            beofore = True
            regexStr = '\''
            for ingredienti in info_ingredienti:
                regexStr += ingredienti.lower()+'|'
            BasicQueryString += 'ingredients REGEXP ' + regexStr[:-1]+'\''

        info_calorie=tracker.get_slot('calorie_slot')
        if(info_calorie.lower() != 'no'):
            emptyQuery = False
            if(beofore):
                BasicQueryString += ' AND energy_kcal_value <=' + info_calorie
            else:
                beofore = True
                BasicQueryString += 'energy_kcal_value <=' + info_calorie
        
        info_allergeni=tracker.get_slot('allergeni_slot').lower()
        if(info_allergeni != 'no'):
            emptyQuery = False
            if(beofore):
                BasicQueryString += ' AND allergens NOT REGEXP \''+info_allergeni+'\''
            else:
                beofore = True
                BasicQueryString += 'allergens NOT REGEXP \''+info_allergeni+'\''
                
        info_prodotto=tracker.get_slot('prodotto_slot')
        if(info_prodotto.lower() != 'no'):
            emptyQuery = False
            if(beofore):
                BasicQueryString += ' AND name REGEXP \''+info_prodotto+"'"
            else:
                beofore = True
                BasicQueryString += ' name REGEXP \''+info_prodotto+"'"

        if(not emptyQuery):
            print(BasicQueryString)
            cursor.execute(BasicQueryString)
            result = cursor.fetchall()
            if len(result) == 0:
                dispatcher.utter_message("Non ci sono prodotti che soddisfano le tue richieste !")
            else:
                pl=f"I prodotti con le condizioni proposte sono: \n"
                dispatcher.utter_message(text=pl)
                for elem in result:
                    pout=f' - {elem[0]}, ingredienti: {elem[1]}. Kcal: {elem[2]}, allergeni: {elem[3]}, \n'
                    dispatcher.utter_message(text=pout)


        print("risultato query")
        return [{"name":"ingrediente_slot","event":"slot","value":None},{"name":"calorie_slot","event":"slot","value":None},{"name":"allergeni_slot","event":"slot","value":None},{"name":"prodotto_slot","event":"slot","value":None}]