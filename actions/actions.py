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

#Azione che permette di visualizzare l'immagine di un dato prodotto
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
                pl=pl+f' - {elem[0]}, porzione: {elem[1]}, kcal per porzione: {(elem[1]*elem[2])/100}\n'
            dispatcher.utter_message(text=pl)
        #dispatcher.utter_message(text=nome_brand)
        return [{"name":"calorie_slot","event":"slot","value":None}]

# Azione di validazione della form per l'acquisizione degli allergeni dell'utente
class ValidateAllergeniForm(FormValidationAction):

# Prendo tutti i prodotti presenti nel db e proseguo eliminando i risultati non essenziali
    cursor.execute('select name, ingredients, energy_kcal_value, allergens from mulino_bianco')
    Allproduct = cursor.fetchall()
    Filter_result = []

    def name(self) -> Text:
        return "validate_allergeni_form"

    def validate_allergeni_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        nome_allergene=tracker.get_slot('allergeni_slot').lower()
        allergeni_result = list(filter(lambda x: True if nome_allergene in x[3] else False, self.Allproduct)) 

        # Se l'allergene non è presente, allora tutti i prodotti sono buoni
        print(tracker.get_slot('allergeni_slot'))
        print(self.Filter_result)

        if len(allergeni_result) == len(self.Allproduct):
            dispatcher.utter_message(text="Tutti i nostri prodotti sono privi del tuo allergene")
            return {"allergeni_slot": None}
        dispatcher.utter_message(text=f"Ok, ho selezionato tutti i prodotti senza {slot_value}")
        self.Filter_result = allergeni_result # Aggiorno il valore 
        return {"allergeni_slot": slot_value}

    def validate_ingrediente_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        nome_ingrediente=tracker.get_slot('ingrediente_slot').lower()
        ingrediente_result = list(filter(lambda x: True if nome_ingrediente in x[1] else False, self.Filter_result))

        # Se l'ingrediente richiesto non è presente, allora viene allertato l'utente
        print(tracker.get_slot('ingrediente_slot'))
        print(self.Filter_result)

        if len(ingrediente_result) == 0:
            dispatcher.utter_message(text="Non abbiamo prodotti privi del tuo allergene con l'ingrediente richiesto")
            return {"ingrediente_slot": None}
        dispatcher.utter_message(text=f"Ok, ho selezionato tutti i prodotti che contengono {slot_value}")
        self.Filter_result = ingrediente_result # Aggiorno il valore 
        return {"ingrediente_slot": slot_value}

    def validate_calorie_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        calorie=float(tracker.get_slot('calorie_slot').lower())
        calorie_result = list(filter(lambda x: True if x[2] <= calorie else False, self.Filter_result))

        # Se il numero di calorie non genera risultati, allora viene allertato l'utente
        print(tracker.get_slot('calorie_slot'))
        print(self.Filter_result)

        if len(calorie_result) == 0:
            dispatcher.utter_message(text="Le scelte precedenti non sono compatibili con questo numero di kcal, ci dispiace")
            return {"calorie_slot": None}
        dispatcher.utter_message(text=f"Ok, ho selezionato tutti i prodotti che contengono al massimo {slot_value}")
        self.Filter_result = calorie_result # Aggiorno il valore 
        return {"calorie_slot": slot_value}

    def validate_prodotto_slot(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain:DomainDict
    ) -> Dict[Text, Any]:

        prodotto=tracker.get_slot('prodotto_slot').lower()
        prodotto_result = list(filter(lambda x: True if prodotto in x[0] else False, self.Filter_result))

        # Se la categoria di prodotto specificata non genera risultati, allora viene allertato l'utente
        print(tracker.get_slot('prodotto_slot'))
        for a in self.Filter_result:
            print('\n')
            print(a[0])
        
        if len(prodotto_result) == 0:
            dispatcher.utter_message(text="Non abbiamo prodotti che soddisfano i tuoi requisiti, ci dispiace")
            return {"prodotto_slot": None}
        dispatcher.utter_message(text=f"Ok, abbiamo prodotti per la categoria {slot_value}")
        self.Filter_result = [] # Aggiorno il valore 
        return {"prodotto_slot": slot_value}



    
# Azione che effettua la submit di un acquisto
class SubmitAllergeni(FormValidationAction):
    def name(self) -> Text:
        return "submit_allergeni"

    def run(self,
            #slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Adesso riproduciamo i risultati ottenuti: \n")
        print('Sono dentro')
        if(tracker.get_slot('ingrediente_slot') is None ):
            print('Sono dentro 1')
            query = "select name, ingredients, energy_kcal_value, allergens from mulino_bianco where allergeni not like "+"'%"+tracker.get_slot('allergeni_slot')+"%'"
            cursor.execute(query)
            result = cursor.fetchall()

            for a in result:
                dispatcher.utter_message(text= "Nome prodotto "+result[a][0]+"\n"+"Ingredienti: "+"\n"+result[1]+"\n"+"kcal "+result[2]+"\n"+"allergeni: "+"\n"+result[3]+"\n")
            return [{"name":"allergene_slot","event":"slot","value":None}]

        if(tracker.get_slot('calorie_slot') is None ):
            print('Sono dentro 2')
            query = "select name, ingredients, energy_kcal_value, allergens from mulino_bianco where allergeni not like "+"'%"+tracker.get_slot('allergeni_slot')+" and ingredients like "+"'%"+tracker.get_slot('ingrediente_slot')+"%'"
            cursor.execute(query)
            result = cursor.fetchall()

            for a in result:
                dispatcher.utter_message(text= "Nome prodotto "+result[a][0]+"\n"+"Ingredienti: "+"\n"+result[1]+"\n"+"kcal "+result[2]+"\n"+"allergeni: "+"\n"+result[3]+"\n")
            return [{"name":"allergene_slot","event":"slot","value":None},{"name":"ingrediente_slot","event":"slot","value":None}]

        if(tracker.get_slot('prodotto_slot') is None ):
            print('Sono dentro 3')
            value = tracker.get_slot('calorie_slot')
            query = "select name, ingredients, energy_kcal_value, allergens from mulino_bianco where allergeni not like "+"'%"+tracker.get_slot('allergeni_slot')+" and ingredients like "+"'%"+tracker.get_slot('allergeni_slot')+"%'"+f' and energy_kcal_value <={value}'
            cursor.execute(query)
            result = cursor.fetchall()

            for a in result:
                dispatcher.utter_message(text= "Nome prodotto "+result[a][0]+"\n"+"Ingredienti: "+"\n"+result[1]+"\n"+"kcal "+result[2]+"\n"+"allergeni: "+"\n"+result[3]+"\n")
            return [{"name":"allergene_slot","event":"slot","value":None},{"name":"ingrediente_slot","event":"slot","value":None},{"name":"calorie_slot","event":"slot","value":None}]

        value = tracker.get_slot('calorie_slot')
        query = "select name, ingredients, energy_kcal_value, allergens from mulino_bianco where allergeni not like "+"'%"+tracker.get_slot('allergeni_slot')+" and ingredients like "+"'%"+tracker.get_slot('allergeni_slot')+"%'"+f' and energy_kcal_value <={value}'+" and name like "+tracker.get_slot('prodotto_slot')+"%'"
        
        for a in result:
            dispatcher.utter_message(text= "Nome prodotto "+result[a][0]+"\n"+"Ingredienti: "+"\n"+result[1]+"\n"+"kcal "+result[2]+"\n"+"allergeni: "+"\n"+result[3]+"\n")
        return [{"name":"allergene_slot","event":"slot","value":None},{"name":"ingrediente_slot","event":"slot","value":None},{"name":"calorie_slot","event":"slot","value":None},{"name":"prodotto_slot","event":"slot","value":None}]