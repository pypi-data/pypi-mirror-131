# DOKUMENT MOŻE BYĆ PRZESTARZAŁY
# HTTPClient
`pymondis._http.HTTPClient`
* Podstawowy client. Do normalnego użytku przeznaczony jest `pymondis._client.Client`

## Metody
1. \_\_init\_\_(timeout: `float | None [None]`, *, base_url: `str ["https://quatromondisapi.azurewebsites.net/api"]`)
   * Jako argument `timeout` można podać liczbę sekund, po której klient zrezygnuje z dalszego czekania na odpowiedź. Domyślnie klient się nie poddaje.
   * Jako **kluczowy** argument `base_url` można podać url, na który będą wysyłane zapytania. Aktualnie nie widzę żadnych zastosowań jego zmiany.
2. `async` get_resource(url: `str`, cache_time: `datetime | None [None]`, cache_content: `bytes | None [None]`) -> `bytes`
   * Metoda używana przez `pymondis._models.Resource.get` do... no... get-owania resource-ów?
   * Jeśli resource na serwerze będzie starszy niż `cache_time` zostanie zwrócony `cache_content`, zamiast pobierać go na nowo
   * Wcześniej do cache-owania był używany hash MD5, porównywany z nagłówkiem zapytania HEAD, ale teraz jest używany conditional `If-Modified-Since`.
3. `async` get_images_galleries(gallery_id: `int`) -> `List[Dict[str, str]]`
   * Metoda używana przez `pymondis._models.Gallery.get_photos` do zdobycia listy zdjęć.
   * Fragment ścieżki nazywa się "Galeries" przez jedno "l" (To nie jedyna literówka w api)... Nie wiem co mam o tym mówić
4. `async` patch_vote(category: `str`, name: `str`)
   * Metoda używana przez `pymondis._models.PlebisciteCandidate.vote` do głosowania
5. `async` post_reservations_manage(pri: `dict`)
   * Metoda używana przez `pymondis._models.PersonalReservationInfo.get_details` do zdobycia szczegółów o rezerwacji.
   * W dict-cie `pri` znajdują się tylko dwa klucze: `ReservationId` i `Surname`, więc się bardzo zastanawiam czy by po prostu tego jako dwa argumenty nie dać.

*Reszta metod jest podobna do tych client-a, tylko zwracają surowe dane, a nie instancje klas z `pymondis._models`*