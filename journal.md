# Journal

### 001 - Før jeg begynner
Da jeg ikke har vært borti kafka før og det er en stund siden jeg har jobbet med backend er min
initielle tanke å prøve å løse oppgaven på enklest mulig måte uten å overkomplisere noe og så 
heller bruke tid på å lære meg kafka, flyten og hvordan det ville blitt gjort i produksjon.

Jeg har ikke skrevet Go før og selvom det kanskje er mest relevant for jobben tror jeg det blir 
for tidkrevende å skulle sette seg inn i dette språket for akkurat denne oppgave. Jeg ser også 
for meg at det vil kreve springboot dersom jeg vil løse det i Java og tenker derfor at å bruke
python vil være det letteste for å fokusere læringen mot kafka. 

Med litt søking på disse tingene så står jeg ved at python og Fast api rammeverket vil være en
god løsning. 

### 002
Som sagt har jeg ikke vært borti kafka før og vet ikke så mye om det annet enn at jeg kjenner
til konseptene med event-drevet arkitektur. Derfor bruker jeg først litt tid på å prøve å 
forstå hvordan kafka funker og hva som kreves for å svare på oppgaven.

### 003 
Jeg setter opp et nytt prosjekt med PyCharm. Her putter jeg inn docker-compose filen og lager en main.py fil. 
I denne filen setter jeg opp et endepunkt "/user-data" ved bruke av fastapi sin funksjoner for dette.
Lager så en funksjon som tar i mot en request, leser denne til json i en try/except blokk og returner 200 OK om det ikke feiler. 
request.json() håndterer om det er noe feil med selve formatet til json filen som sendes, ellers håndteres ingen feil
eller valideringer etter oppgavens beskrivelse om å ikke bruke tid på det.

### 004
Jeg startet api ved fastapi dev kommandoen og tester at endepunktet fungerer med noe arbitrær json data:
curl -X POST http://localhost:8000/userdata \
  -H "Content-Type: application/json" \
  -d '{"id": "0", "user_id": "d33y7gd", "subscription": "total"}'

Respons: 200 OK. 
kanon!

### 005
Etter litt undersøking ser det ut som confluent_kafka vil fungere som en god klient i dette prosjektet.
Alternativene var kafka-python og aiokafka. Her valgte jeg egentlig bare basert på at det opprettholdes av Confluent,
har bra performance for mange meldinger og at det støtter avanserte funksjoner i kafka.

### 006
Når dataen er "validert" sender produceren dataen til topic "user-data". I docker filen er det lagt til at 
dersom et topic ikke finnes så blir det opprettet, så trenger ikke å gjøre dette eksplisitt i koden. 
Partisjoner og brokere holdes også til default. 

`
producer.produce(
        topic="user-data",
        value=json.dumps(data).encode("utf-8"),
        callback=delivery_report
`

data-objektet blir gjort om til en str og encodes til bytes så det kan sendes som en kafka melding.
Setter også opp en enkel callback som bare nå printer om meldingen er suksessfullt sendt eller ikke. 
Her burde det nok i produksjon heller brukes en logger og logge mer data om hva som eventuelt gikk gale.

Da det i oppgave var fokus på at dataen skulle bli persistert, kjører jeg også producer.flush() 
med engang etter hvert kall fra produceren for å forsikre at meldingene blir sendt med engang (persistert).
Dette er nok ikke helt holdbart i produksjon da det vil føre til lavere performance ved mange meldinger. 
Her er det nok mer vanlig å batche meldingene før de sendes til kafka streamen. 

På grunn av dette punktet i oppgaven legger jeg også til 
`volumes: - kafka_data:/var/lib/kafka/data` i docker-compose filen for at dataen skal bli lagret selvom containeren 
ikke kjøres.

### 007
Når det gjelder feilhåndtering er jeg nok litt usikker på hva som er vanlig med kafka utover callback, 
men et lite søk sier meg at det fortsatt kan være lurt å ha producer kallet i en try/except blokk i tilfellet 
det skulle være feil med json.dumps, encodingen, eller producer kø som er full. 

Det eneste problemet her er nok at feilen da blir sendt tilbake til klienten, men her er jeg usikker på om det blir riktig 
å gjøre. Jeg kan se for meg i produksjon at feilen burde heller logges og håndteres som dead letter dersom 
det feiler når det skal sendes til kafka da det ikke er klienten sin feil. Dette er vel kanskje mulig å sende
til et dead-letter topic eller lignende i callback funksjonen. 

### 008
Jeg tester at produsenten og kafka funker som det skal ved å kjøre docker containeren med kafka, starte dev serveren,
kjører samme kommando for api kallet og sjekker kafka meldingen gjennom 
docker exec -it kafka kafka-console-consumer.sh \                               
  --bootstrap-server localhost:9092 \
  --topic user-data --from-beginning

Den viser meldingen og flyten fungerer. Dersom jeg stopper docker og starter igjen er meldingen fortsatt persistert. 

### 009
Etter litt mer undersøking om kafka klienten for python så kan det virke som confluent_kafka ikke nødvendigvis er det beste 
sammen med Fast API da førstnevnte er synkront og sistnevnte asynkront. Det kan skape problemer med blokking og etter det jeg 
har lest vil kreve at man kjører consumer og fast api på ulike tråder. (?). Dette ville vært noe å sjekke opp i dersom man skulle 
ha tjenesten ut i produksjon. På grunn av dette så virker det som det er bedre å konfigurere produceren inne i fastapi sin
lifespan funksjon istedenfor utenfor slik jeg originalt hadde det. 

### 010
Det var noen problemer med hvordan jeg først hadde gjort det med å ha en global variabel for produceren,
så jeg endret til å bruke app state i stedenfor, slik at appen bare henter ut prouceren fra denne staten når den brukes.