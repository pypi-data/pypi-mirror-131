# DOKUMENT MOŻE BYĆ PRZESTARZAŁY
# Client
`pymondis._client.Client`
* `Client` ułatwia wysyłanie zapytań i otrzymywanie odpowiedzi z wykorzystaniem modeli z modułu `pymondis._client.models`

## Metody
1. \_\_init\_\_(http: `HTTPClient [None]`)
   * Jako argument `http` można podać instancję `pymondis._api.HTTPClient` która będzie wykorzystana do wysyłania zapytań. Jeśli nie podana, zostanie stworzona bez argumentów.
2. `async` get_camps() -> `List[pymondis._models.Camp]`
   * Na zwróconej liście powinny znajdować się wszystkie obozy widoczne na stronie.

3. `async` get_galleries(castle: `pymondis._enums.Castle`) -> `List[pymondis._models.Gallery]`
   * Na liście znajdują się wszystkie galerie widoczne na stronie.

4. `async` get_crew() -> `List[pymondis._models.CrewMember]`
   * Na liście znajduje się cała załoga kolonii (psorzy, kierownicy).
   * Na liście **nie znajdują się**: pracownicy biura i HY.

5. `async` get_plebiscite(year: `int`) -> `List[pymondis._models.PlebisciteCandidate]`
   * Na liście znajdują się wszyscy kandydaci plebiscytu z roku `year`.

### Nietestowane
1. `async` *reserve_inauguration*(reservation: `pymondis._models.EventReservationSummary`)
   * Rezerwuje miejsce w inauguracji

2. `async` *order_fwb*(purchaser: `pymondis._models.Purchaser`)
   * Zamawia książkę „QUATROMONDIS – CZTERY ŚWIATY HUGONA YORCKA. OTWARCIE”

3. `async` *reserve_camp*(reservation: `pymondis._models.WebReservationModel`) -> `List[str]`
   * Rezerwuje miejsce na obozie.
   * Na liście powinny znajdować się kody rezerwacji.
### Niezaimplementowane
1. `async` ~~submit_survey~~(survey_hash: `str`, result: `pymondis._models.ParentSurveyResult`)
    * To jest coś w stylu ankiety.
    * Nie potrafię znaleźć, czemu to odpowiada na stronie.

2. `async` ~~apply_for_job~~()
   * Zgłasza chęć pracy.
   * W swagger-ze nie udokumentowali, co trzeba wysłać.
   * Dane najprawdopodobniej są wysyłane jako form.

## Atrybuty
1. `http`
   * Atrybut `http` to przypisany w konstruktorze korespondujący `pymondis._api.HTTPClient`

## Użycie:
1. Context manager (`async with`)
   * Kiedy program się wysypie to nie zostawiasz otwartego połączenia 
```
async with Client() as client:
    ...
```