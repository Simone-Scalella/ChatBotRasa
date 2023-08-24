# ChatBotRasa

# Introduzione
In questa relazione illustreremo gli aspetti peculiari della progettazione e dell’implementazione di un chatbot che ha come scopo finale quello di informare i consumatori circa i prodotti della Mulino Bianco. Entrando nel dettaglio esso permetterà di conoscere le informazioni nutrizionali dei vari prodotti, i loro ingredienti, i loro allergeni e simili, oltre a consentire all’utente finale di visionare un’immagine del prodotto.

## Chatbot
Un chatbot è un software che simula ed elabora le conversazioni umane (scritte o parlate), consentendo agli utenti di interagire con i dispositivi digitali come se stessero comunicando con altri esseri umani. Per rendere tutto ciò possibile un chatbot sfrutta diverse tecniche di intelligenza artificiale, insieme a tecniche di machine learning e alla teoria del Natural Language Processing. Ci sono alcune caratteristiche di base che un buon assistente virtuale dovrebbe avere e queste sono:

  - **Interattività**: devono permettere un interazione bidirezionale, in quanto dovrebbero comprendere l’input fornito dall’utente e fornire ad esso dei risultati utilizzando il deep learning e l’elaborazione del linguaggio naturale;
  -  **Iteratività**: : il chatbot dovrebbe avere memoria delle precedenti iterazioni avute con l’utente e restituire le informazioni adatte all’iterazione specifica che si sta avendo in un dato momento;
  -  **Additività**: un chatbot non deve essere programmato per un singolo task, ma dovrebbe essere dinamico imitando le capacità di un cervello umano ed adattandosi all’ambiente circostante;
  -  **Contestualizzazione**: al fine di fornire un output adeguato secondo quanto richiesto dall’utente, i chatbot devono essere in grado di identificare ed estrarre gli elementi contestuali dall’input come il task, l’obiettivo, il tempo, il luogo.

I chatbot portano numerosi vantaggi alle aziende che li utilizzano in quanto sono disponibili 24/7 e impiegano meno tempo di un operatore umano per completare un task.

Esistono due principali tipi di chatbot:
  - **I chatbot dedicati alle attività (dichiarativi)** sono programmi monouso che si concentrano sull'esecuzione di una funzione. Usando regole, NLP e pochissima ML, generano risposte automatizzate ma colloquiali alle richieste degli utenti. Le interazioni con questi chatbots sono altamente specifiche e strutturate e sono per lo più applicabili alle funzioni di assistenza e di servizio: pensa a domande frequenti interattive e consolidate. I chatbot dedicati alle attività sono in grado di gestire domande comuni, ad esempio query riguardo gli orari lavorativi o semplici transazioni che non coinvolgono una varietà di variabili. Sebbene utilizzino la NLP in modo tale che gli utenti finali possano sperimentarli in modo semplice, le loro capacità sono abbastanza basilari. Attualmente, questi sono i chatbot più usati.
  - **I chatbot predittivi basati sui dati (di conversazione)** sono spesso indicati come assistenti virtuali o assistenti digitali e sono molto più sofisticati, interattivi e personalizzati rispetto ai chatbot dedicati alle attività. Questi chatbot sono consapevoli del contesto di riferimento e sfruttano la comprensione della lingua naturale (NLU), la NLP e la ML per imparare. Applicano intelligenza predittiva e analisi dei dati per consentire la personalizzazione in base ai profili degli utenti e al comportamento degli utenti precedenti. Gli assistenti digitali possono imparare nel tempo le preferenze di un utente, fornire raccomandazioni e persino anticipare le esigenze. Oltre a monitorare i dati e le linee guida, possono avviare conversazioni. Siri di Apple e Alexa di Amazon sono esempi di chatbot predittivi orientati al consumatore e basati sui dati.

Gli assistenti digitali avanzati sono inoltre in grado di connettere diversi chatbot monouso sotto un unico gruppo, estrarre diverse informazioni da ognuno e combinare queste informazioni per eseguire un'attività mantenendo comunque il contesto: in tal modo il chatbot non si "confonde".

## Il framework RASA
RASA è un framework open source in Python dedicato alla creazione di chatbot conversazionali, si basa sul machine learning supervisionato, insieme alle tecniche di Natural Language Processing (NLP), per comprendere gli intenti degli utenti e fornire ad essi una risposta coerente. A fronte del grande successo riscontato dai chatbot nel contesto aziendale, sono stati sviluppati molti altri framework per creare chatbot (come Dialogflow, Amazon Lex e Luis), ma i vantaggi nell’utilizzo di Rasa sono diversi:
  1. RASA è open source, e ciò quindi permette di avere a disposizione il codice e poter intervenire manualmente sul bot in caso di necessità;
  2. RASA è un progetto in continuo sviluppo, con una vasta community di sviluppatori a supporto. Gli stessi creatori sono disponibili a fornire chiarimenti e a risolvere bug e problemi vari;
  3. RASA non è un servizio cloud e poter quindi essere ospitato in locale sulle macchine aziendali e questo è un vantaggio soprattutto nel caso in cui nelle chat con gli utenti passassero dati sensibili che, per motivi di privacy, non dovrebbero essere esposti all’esterno. La privacy dell’utente viene così garantita, avendo tutti i dati in locale.

L’architettura RASA è costituita da due componenti fondamentali, che sono:
  - RASA NLU: si occupa di capire e classificare la volontà dell’utente (chiamato anche intente), prendendo come input del testo "libero" scritto da quest’ultimo e restituendo dati strutturati;
  - RASA CORE: dopo aver classificato il messaggio dell’utente, elabora quella che sarà la risposta sulla base di ciò che è stato recepito al momento presente, ma anche in passato.

Come detto in precedenza RASA si basa sull’apprendimento supervisionato e quindi è necessario fornirgli dati di training, in particolare i cosiddetti intent, che altro non sono che frasi di esempio che mappano le possibili motivazioni che un utente può avere per utilizzare il chatbot in questione. Ad ogni frase scritta dall’utente, infatti, corrisponde un’intenzione e l’obiettivo del chatbot, in prima istanza, sarà proprio quello di individuare e classificare correttamente tale aspetto, quindi si dovrà addestrare il chatbot fornendogli un opportuno numero di esempi per ciascuna tipologia di richiesta Una volta aver incluso tutti i possibili intent relativi al dominio di interesse, il chatbot sarà in grado di classificare un input ricevuto associandogli l’intent che più si addice, sulla base di un punteggio.

Quindi una volta che la componente RASA NLU rileva l’intent dell’input, si attiva il RASA Core che crea un modello di machine learning per imparare dagli esempi forniti e predire la risposta più adatta da restituire all’utente, scegliendola tra le **utterences**. Se invece la risposta prevede un’elaborazione più articolata, come ad esempio l’invocazione di una API o una query su database si deve ricorrere alle **Actions**. Tutti i file da utilizzare hanno estensione .yml, tranne le actions che sono un file Phyton.

# Chatbot mulino bianco
Il chatbot oggetto di questo progetto ha l’obiettivo di informare i consumatori sui prodotti della Mulino Bianco (e delle altre imprese ad essa legate: Pan di Stelle e Gran Cereale). Il chatbot è stato realizzato per parlare e rispondere in italiano. Ci si è focalizzati su un set di possibili informazioni che l’utente potrebbe voler conoscere, anche in base ai dati che si avevano a disposizione nel dataset utilizzato. Con il dataset a disposizione sono state individuate tutte le informazioni che maggiormente interessano i consumatori. Essendo molte le informazioni si è deciso di raggrupparle in più funzionalità, in maniera tale da non avere delle conversazioni troppo lunghe. Le informazioni considerate sono relative ai gusti del consumatore, come ad esempio la categoria o un certo tipo di ingredienti. Inoltre, si è tenuta in considerazione anche la salute del consumatore, inserendo tra le informazioni anche gli allergeni. Le possibili azioni che gli utenti potranno fare sono le seguenti:
  - Visualizzare tutte le categorie dei prodotti presenti (ad es. torte, biscotti, …);
  - Visualizzare come è composto il packaging del prodotto (ad es. plastica, carta, …);
  - Visualizzare un prodotto, le diverse dimensioni dei pacchi disponibili, la porzione consigliata, la categoria in cui rientra il prodotto e gli ingredienti;
  - Visualizzare un prodotto, i suoi ingredienti, i suoi allergeni e le sue kcal;
  - Visualizzare i vari brand presenti, e una volta selezionato uno di essi tutti i prodotti di tale brand;
  - Visualizzare tutti i prodotti che hanno meno calorie di quelle inserite dall’utente, per porzione;
  - Comprare un dato prodotto.

Le funzioni che abbiamo descritto prima richiedono di accedere ad un dataset che consente al chatbot di trovare le informazioni che l’utente richiede e di registrare quelle relative alle vendite dei prodotti. Il dataset è stato memorizzato in un database con all’interno due tabelle, una per gli ingredienti e una per gli acquisti.

## Il dataset
Ai fini del progetto si è utilizzato un database gestito con MySQL che è un relational database management system (RDBMS) composto da un client a riga di comando che permette l’interrogazione del database e un server nel quale il database è ospitato. I dati per popolare tale database sono stati reperiti effettuando una ricerca sul sito [it.openfoodfacts.org](https://it.openfoodfacts.org/) e scaricando i risultati. Si è poi provveduto ad aggiornare il dataset così ottenuto aggiungendo i prodotti nuovi e andando a rimuovere quelli che non sono più in commercio, inoltre si è effettuato anche una fase di ETL che è consistita soprattutto nella rimozione delle colonne inutili e nella rimozione delle righe riguardanti i prodotti non esistenti in Italia. Infine, è stata aggiunto un attributo ad ogni riga per associare ad ogni prodotto la sua immagine.

## La struttura
Una volta che si è creato un a ambiente virtuale tramite conda e una directory per lo sviluppo del progetto, si può inizializzare il progetto mediante il comando **rasa init** (messo a disposizione del framework) che crea la struttura per il progetto completa di tutte le componenti che sono necessarie per poter sviluppare un chatbot.
Le componenti sono:
  - **actions.py** che è uno script Python in cui sono definite tutte le classi che mappano le azioni che sono riportate nel file domain.yml e che richiedono un’elaborazione maggiore per costruire la risposta, quindi permettono di avere risposte che sono frutti di calcoli e non già predefinite;
  - **nlu.yml** è un file nel quale vengono definiti gli esempi che saranno poi usati in fase di addestramento
sia per gli intent che per le entities;
  - **rules.yml** file che contiene regole predefinite per le policy di dialogo;
  - **stories.yml** file che contiene esempi di conversazione, chiamati path, che il chatbot seguirà;
  - **config.yml** file che contiene la configurazione del modello di machine learning;
  - **domain.yml** file che contiene tutte le informazioni che sono necessarie al chatbot per poter operare, nello specifico in questo file è possibile vedere una lista di tutti gli intent che potranno essere espressi durante una conversazione insieme alle entities che saranno valorizzate, gli slot utilizzati per memorizzare i dati necessari per l’elaborazione, le utterences con le risposte predefinite che il chatbot fornirà, la lista contenente tutte le azioni e la lista dove vengono definite le form.

# Funzionalità del chatbot
Procederemo in questo capitolo illustrando le varie funzionalità del chatbot e per ognuna di esse spiegando le scelte e le strategie applicate per svilupparle.

## Visualizzare tutte le categorie dei prodotti presenti

[test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/avviobot.png)
