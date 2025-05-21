# Email Classificatie API

Deze FastAPI-gebaseerde API classificeert e-mails automatisch in één van vier categorieën: **World**, **Sports**, **Business**, of **Sci-Tech**. 
De classificatie helpt bij het automatisch doorsturen van e-mails naar de juiste afdelingen binnen organisatie X.

---

## Functionaliteit

- ✅ Classificeert e-mails op basis van titel en omschrijving
- 🔒 Valideert input met Pydantic (geen lege strings toegestaan)
- 📦 Terugkerende JSON-response met consistente structuur
- 🛑 Robuuste foutafhandeling: ook bij validatiefouten een geldige JSON-response
- 🔄 EmailID wordt teruggegeven (max. 10 karakters) voor tracering

---

## Installatie
- `docker build -t email-classifier .`
- `docker run -p 8000:8000 email-classifier`
- open `localhost:8000/docs`

---

## Gebruik
- Verzend een POST-verzoek naar /classify met de volgende JSON in de Swagger UI:
```
{
  "EmailRequestData": {
    "EmailID": "example123",
    "TitleDescription": "Breaking news in the business world"
  }
}
```

- response
```
{
  "EmailResponseData": {
    "EmailId": "example12",
    "ReturnCode": 0,
    "EmailClass": 3,
    "EmailClassDescrip": "Business"
  }
}
```
