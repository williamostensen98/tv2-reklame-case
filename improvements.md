# Improvements

På grunn av bakgrunnen min så har jeg som sagt valgt å heller fokusere på å forstå konseptene og detaljene bak kafka
enn å skulle implementere utover en fungerende mvp. Dette for å kunne ta del i en samtale om koden og konseptene, istedenfor
å bare skrive kode hvor jeg ikke nødvendigvis skjønner hva som ligger bak.

Med det sagt ville jeg med mer tid forbedret et par ting for at det skulle være en fungerende Proof-of-concept:
* Mer validering av data for å hvertfall vite at dataen gir mening, og ikke bare er et tomt json object
* Dockerize api-et også og kanskje deploye det til et test miljø så det kan testes utenfor lokal maskin.
* Bedre håndtering av feil fra api og fra kafka som ikke nødvendigvis skal tilbake til klienten. 
* Håndtere Dead letters. 

Andre ting som burde legges til dersom det skulle bli tatt videre til produksjon
* Riktig bruk av api rammeverk og kafka klient? (se journal)
* Autentisering for API-et - sørge for at ikke hvem som helst kan sende requests. 
* Andre api-relaterte ting som må være med: rate limiting, encryption av data, sanitering(unngå angrep), caching og load balancing.
* Logging av events og feil fra både api og kafka gjennom en logger og  bare med ikke print meldinger :). 
* Sette opp mer detaljert config for kafka features som trengs. For eks. retries, idempotency(håndtering av duplikater) og ev. backups av data ved flere brokere, partisjoner osv(replication). 
* Dokumentasjon (Swagger)