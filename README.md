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
Procederemo in questo capitolo illustrando le varie funzionalità del chatbot e per ognuna di esse spiegando le scelte e le strategie applicate per svilupparle. Inoltre, riporteremo le immagini con i risultati ottenuti.

## Visualizzare tutte le categorie dei prodotti presenti
Funzione del chatbot che permette di visualizzare tutte le categorie dei prodotti presenti (ad es. torte, biscotti, …). Il primo step per realizzare tale funzionalità è stato fornire al modello di machine learning alcuni esempi di frasi che l’utente potrebbe scrivere al chatbot con l’intento di vedere le categorie dei vari prodotti e su questi il modello è stato poi allenato.
Per realizzare tale funzione è stata definita una classe di azione che, mediante una connessione al database, effettua una query in grado di estrarre distintamente tutte le categorie presenti all’interno del database ed associate a ciascun prodotto. Il risultato che si ottiene è una lista riportante tutte le categorie presenti nel database.

![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/allcat.png)

## Visualizzare da cosa è composto il packaging del prodotto
Funzione del chatbot che permette di visualizzare come è composto il packaging del prodotto (ad es. plastica, carta, …). Il primo step per realizzare tale funzionalità è stato fornire al modello di machine learning alcuni esempi di frasi che l’utente potrebbe scrivere al chatbot con l’intento di vedere il packaging (utile ai fini di un corretto riciclo) di un dato prodotto e su questi il modello è stato poi allenato.
Per realizzare tale funzione è stata definita una classe di azione che, mediante una connessione al database, effettua una query in grado di estrarre il packaging associato ad un dato prodotto, passato in input dall’utente. Viene effettuato un ulteriore controllo sulla presenza del prodotto nel database.

![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/package.png)

## Visualizzare informazioni sul prodotto
Funzione del chatbot che permette di visualizzare un prodotto, le diverse dimensioni dei pacchi disponibili, la porzione consigliata, la categoria in cui rientra il prodotto e gli ingredienti.
Questa funzione è una funzione articolata e richiede diverse informazioni all’utente. In fase di implementazione si è tenuta in considerazione la possibilità che l’utente non volesse specificare tutte le informazioni che sono state considerate, quindi, su quattro all'utente ne interessano due. Di conseguenza si è deciso di realizzare questa funzione rendendo le richieste di informazioni facoltative. Sono state realizzate due classi di azioni, una per l’inserimento di valori da parte dell’utente e una per costruire la query da fare al database. Tutte le azioni sono state riportate nel file domain.

La prima azione è quella di verifica dell’input inserito dall’utente. All’utente viene comunicata la possibilità di inserire tutte o solo una parte delle informazioni richieste. L’input inserito dall’utente viene controllato, infatti, se inserisce la stringa “no” o “skip” lo slot corrispondente verrà valorizzato con un valore di controllo. Tale valore è la stringa “no” che useremo per fare ulteriori controlli in fase di invio della query. Si offre la possibilità di inserire più ingredienti nella richiesta, infatti, lo slot degli ingredienti è stato definito come una lista. Infine, sono stati realizzati alcuni controlli di sicurezza, ad esempio controlliamo se per le calorie è stato inserito un numero, altrimenti, avvisiamo l’utente, oppure controlliamo se la categoria inserita esiste, tramite una semplice query e poi, successivamente, controllandone il risultato.
Al termine della storia viene attivata l’action di invio della query.

In questa azione, in base a ciò che è stato inserito all’utente, viene realizzata la query che verrà inviata al database. La query viene costruita in maniera incrementale, controllando il valore presente nello slot. Se nello slot è presente la stringa “no”, allora, non si aggiunge la condizione nel where relativa a quell’informazione. Invece, se è presente l’input dell’utente si costruisce un pezzo della query, e lo si aggiunge alla where. Per evitare errori nella costruzione della query sono state utilizzate diverse guardie, in quanto l’utente ha il massimo grado di libertà nel rispondere al chatbot. Ad esempio, un caso limite, è quello in cui l’utente inizia la story ma inserisce solo no o skip, quindi, in questo caso il chatbot non deve inviare nessuna query al database.

### Immagini della visualizzazione delle informazioni dei prodotti
![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/prodottiok2.png)
![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/prodottoOk.png)

### Immagini della visualizzazione delle informazioni dei prodotti con errore d'inserimento

![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/testprodotti.png)
![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/prodottotest2.png)

## Visualizzare un prodotto, i suoi ingredienti, i suoi allergeni e le sue kcal
Descriviamo la funzione che realizza la visualizzazione dei prodotti, prendendo in considerazione gli allergeni, gli ingredienti, il tipo di prodotto e le sue kcal. Per realizzare questa funzione si è deciso di inserire un nuovo intent, nel quale andiamo a riportare gli esempi di frasi che una persona con allergie o intolleranze alimentari può scrivere al chatbot.
Successivamente sono state realizzate le due azioni che servono per recuperare l’input inserito dall’utente e per realizzare la query da inviare al database. Durante la realizzazione di questa funzione si è tenuto conto di tutte le considerazioni fatte precedentemente, quindi, l’utente ha la facoltà di inserire tutte o solo alcune delle informazioni richieste. Di seguito riportiamo un’immagine contenente il codice utilizzato per realizzare la funzione.

Anche in questa funzione sono stati inseriti dei controlli, ad esempio se l’utente inserisce un allergene che non esiste, viene allertato con un messaggio, che gli comunica l’assenza di quell’allergene in tutti i nostri prodotti. Le informazioni richieste all’utente sono l’allergene, gli ingredienti che gli interessano, infatti, l’utente può inserire più ingredienti che vengono inseriti in uno slot di tipo List, il valore massimo di kcal che deve contenere, e infine, il tipo di prodotto che gli interessa. L'azione termina quando l’utente ha inserito tutte le informazioni richieste. Al termine di questa storia viene attivata la funzione di invio della query al database. Di seguito riportiamo un’immagine contente il codice utilizzato per realizzare questa funzione.

Questa funzione costruisce la query in maniera incrementale, basandosi sulle informazioni inserite dall’utente. Si controllano gli slot valorizzati con gli input dell’utente, se il valore è “no”, perché l’utente ha deciso di non inserire quell’informazione, allora, la funzione non inserirà nella query la condizione corrispondente, altrimenti, se è stato inserito un valore corretto, la funzione aggiunge la condizione corrispondente alla where della query. Una volta terminata la query si mostra il risultato all’utente e a tutti gli slot viene assegnato il valore “None”, altrimenti, continuerebbero a contenere i vecchi valori, e se l’utente riattiva la storia ottiene sempre lo stesso risultato. In questo modo gli slot sono pronti per essere utilizzati nella riattivazione successiva della storia. Di seguito riportiamo un’immagine dell’output ottenuto al termine della storia.

### Immagine della visualizzazione dei prodotti, degli ingredienti, dei suoi allergeni e le sue kcal

![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/allergeni1.png)

### Immagine della visualizzazione dei prodotti, degli ingredienti, dei suoi allergeni e le sue kcal con errore d'inserimento

![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/testallergeni.png)

## Visualizzare i vari brand presenti e i relativi prodotti
Funzione del chatbot che permette di visualizzare i vari brand presenti, e una volta selezionato uno di essi tutti i prodotti di tale brand. Il primo step per realizzare tale funzionalità e stato fornire al modello di machine learning alcuni esempi di frasi che l’utente potrebbe scrivere al chatbot con l’intento di conoscere i brand che sono presenti nel dataset e su questi il modello è stato poi allenato.
Successivamente si è definita l’azione che connettendosi al database prende tutti i diversi brand (mediante una query SQL) e fa restituire al chatbot tali brand sottoforma di bottone.
Si è deciso di utilizzare un bottone per rendere più user-friendly lo step successivo ovvero quello di conoscere tutti i prodotti di tale brand, cosicché l’utente non debba digitare nuovamente il brand rischiando di fare un errore.

![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/brand.png)

## Visualizzare prodotti in relazione alle calorie
Funzione del chatbot che permette di visualizzare tutti i prodotti che hanno meno calorie di quelle inserite dall’utente, per porzione. Il primo step per realizzare tale funzionalità e stato fornire al modello di machine learning alcuni esempi di frasi che l’utente potrebbe scrivere al chatbot con l’intento di visualizzare la lista delle merendine che hanno meno calorie di quelle specificate dall’utente per porzione consigliata. Il modello è stato poi allenato con questi esempi. A differenza degli altri intent qua si può notare che vi è un valore tra parentesi quadre, affiancato a uno tra parentesi tonde. Questo è fatto per creare l’entità “calorie”, mediante la quale il chatbot capirà che tale valore riguarda le calorie che saranno poi utilizzate per fare la query.
Successivamente si è definita l’azione che connettendosi al database prende tutti i prodotti che rispettano la condizione posta (mediante una query SQL) e fa restituire al chatbot la lista di tali prodotti con il nome, la porzione (in grammi) e le kcal per porzione.

![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/calorie.png)

## Visualizzare l’immagine di un prodotto
Funzione del chatbot che permette di visualizzare l’immagine di un prodotto. Il primo step per realizzare tale funzionalità e stato fornire al modello di machine learning alcuni esempi di frasi che l’utente potrebbe scrivere al chatbot con l’intento di visualizzare un’immagine di un particolare prodotto, che sarà specificato dall’utente nell’interazione successiva. Il modello è stato poi allenato con questi esempi.
Successivamente si è definita l’azione che connettendosi al database prende il link del prodotto di interesse (mediante una query SQL) e fa restituire al chatbot un messaggio di testo insieme al link dell’immagine.
A differenza delle altre risposte qui si ha un attributo image, che serve per consentire la visualizzazione dell’immagine.

![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/imageprod.png)

## Acquistare un dato prodotto
Funzione del chatbot che permette di effettuare l’acquisto di un prodotto. Il primo step per realizzare tale funzionalità è stato fornire al modello di machine learning alcuni esempi di frasi che l’utente potrebbe scrivere al chatbot con l’intento di acquistare un prodotto, che sarà specificato dall’utente nell’interazione successiva, insieme alla dimensione della confezione desiderata. Il modello è stato poi allenato con questi esempi.
Per consentire l’acquisto mediante il chatbot si è dovuto effettuare un primo step nel quale si effettuavano le validazioni degli slot, della form di acquisto riempiti dall’utente; ovvero si andava a vedere se nel database tali prodotti esistevano e se la dimensione del pacco che l’utente richiedeva era effettivamente presente.

Terminata la prima azione, che controlla l’input inserito dall’utente, la storia attiva la seconda azione realizzata per questa funzione, quella che effettua l’invio della query al database. La query viene costruita inserendo nel campo values i valori definiti dall’utente. La submit della query viene realizzata all’interno di un costrutto try except, il quale serve ad avvisare l’utente qualora si presentino problemi legati al database. Se non si sono verificati problemi, l’utente viene avvisato dell’esito positivo, relativo al termine dell’azione.

![test](https://github.com/Simone-Scalella/ChatBotRasa/blob/main/image/acquistook.png)

# Connessione a Telegram e Test
## Connessione
L’ultima fase del progetto consiste nel collegamento del chatbot realizzato ad una piattaforma di messaggistica istantanea, in maniera tale che gli utenti possano interagirci in maniera semplice, da smartphone e soprattutto con un’interfaccia grafica moderna. La piattaforma che si è deciso di utilizzare è Telegram, si è utilizzato il servizio ngrok per finalizzare tale connessione e mandare in esecuzione il chatbot su server locale.

## Testing
Finita l’implementazione e la connessione alla piattaforma di messaggistica istantanea scelta, si è proceduto a testare il chatbot simulando le possibili interazioni che l’utente potrebbe avere con esso. Si è proceduto a simulare anche il comportamento di utente sbadato, cioè, di utente che inserisce, in modo sbadato, degli input errati. Questo ci è servito per verificare il corretto funzionamento dei controlli implementati. Di seguito riportiamo alcune immagini con i risultati ottenuti.

# Conclusioni e sviluppi futuri
Si è utilizzato il framework RASA (AI) per la realizzazione di un chatbot come supporto al cliente, nella fattispecie un chatbot che guidi l’utente nella scelta dei prodotti fra quelli venduti dall’azienda Mulino Bianco. Le funzionalità implementate (descritte nel Capitolo 3 di tale relazione) del chatbot sono rivolte principalmente ai prodotti della Mulino Bianco e di alcune delle sue controllate. Si potrebbe pensare come un possibile sviluppo futuro di ampliare il database dei prodotti, per estenderlo pure a quelli di altre aziende oltre che creare altre funzionalità più incentrate sulle informazioni nutrizionali.
