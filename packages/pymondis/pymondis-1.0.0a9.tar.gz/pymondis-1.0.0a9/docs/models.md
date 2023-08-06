# DOKUMENT MOŻE BYĆ PRZESTARZAŁY
Wszystkie modele zbudowane są za pomocą biblioteki `attr`.\
Wszystkie zaimplementowane modele oprócz `Resource`, posiadają metodę `init_from_dict` lub `to_dict`.
Pierwsza tworzy instancję siebie z dict-a podanego jako pierwszy argument (i kwargs-ów), a druga instancję dict-a z siebie.

# Resource
`pymondis._models.Resource`
* Reprezentuje resource-a (najczęściej zdjęcie z serwera hymsresources.blob.core.windows.net)
## Konstrukcja
1. url: `str` (link)
2. http: `HTTPClient | None [None]` (client, który będzie domyślnie używany w get())
### Kluczowe
3. cache_time: `datetime | None [None]` (*Nie zalecane* czas, w którym ostatnio pobrano dane)
4. cache_content: `bytes | None [None]` (*Nie zalecane* ostatnio pobrane dane)
## Metody
1. `async` get(use_cache: `bool [True]`, update_cache: `bool [True]`, http: `HTTPClient | None [None]`) -> `bytes`
    * Zwraca surowe dane w bajtach.
    * Do wykonania zapytania używany jest `http` jeśli podany, w przeciwnym razie `self._http` (podany jako `http` w konstruktorze).
    * Jeśli `use_cache` to `True`, wykorzystane zostaną z-cache-owane danye, jeśli istnieją.
    * Jeśli `update_cache` to `True`, wynik zapytania zostanie zapisany, do późniejszego użytku. Jeśli chcesz ograniczyć zużycie pamięci, wyłącz tę opcję.
    * Metoda wewnętrznie korzysta z `pymondis._http.HTTPClient.get_resource`.

# Gallery
`pymondis._models.Gallery`
* Reprezentuje galerie z fotorelacji.
## Konstrukcja
1. gallery_id: `int` (numer galerii)
2. start: `datetime | None [None]` (data rozpoczęcia galerii)
3. end: `datetime | None [None]` (data zakończenia galerii)
4. name: `str | None [None]` (nazwa galerii)
5. empty: `bool | None [None]` (czy jest pusta)
6. http: `HTTPClient | None [None]` (client, który będzie domyślnie używany w get_photos())
## Metody
1. `async` get_photos(http: `HTTPClient | None [None]`) -> `List[Photo]`
   * Zwraca listę instancji `pymondis._models.Photo`.
   * Do wykonania zapytania używany jest `http` jeśli podany, w przeciwnym razie `self._http` (podany jako `http` w konstruktorze).
   * Metoda wewnętrznie korzysta z `pymondis._http.HTTPClient.get_images_galleries`.

# Photo
`pymondis._models.Gallery.Photo`
* Reprezentuje zdjęcie z galerii z fotorelacji.
## Konstrukcja
1. normal: `Resource` (małe zdjęcie)
2. large: `Resource` (wyższej jakości zdjęcie)

# Camp
`pymondis._models.Camp`
* Reprezentuje zapowiedziany obóz
## Konstrukcja
1. camp_id: `int` (numer obozu)
2. code: `str` (kod obozu - `{Z jeśli w zimę}{skrót zamku}{numer obozu w tym zamku}{skrót programu}`)
3. place: `Castle` (miejsce, w którym odbywa się obóz)
4. price: `int` (cena *bez zniżki*)
5. promo: `int | None` (cena *ze zniżką* jeśli takowa istnieje)
6. active: `bool` (czy są jeszcze miejsca; nie ma jeszcze listy rezerwowej)
7. places_left: `int` (pozostałe miejsca, nie zawsze są prawdziwe. Widziałem obóz, który nie był `active`, a miał tutaj wpisane chyba z 70)
8. program: `str` (temat obozu)
9. level: `CampLevel` (poziom - normalny albo master)
10. world: `World` (świat)
11. season: `Season` (pora roku)
12. trip: `str | None` (wycieczki, jeśli jakieś są)
13. start: `datetme` (data rozpoczęcia)
14. end: `datetime` (data zakończenia)
15. ages: `list[str]` (lista przedziałów wiekowych, nie wiem, do czego to)
16. transports: `list[Transport]` (lista dostępnych transportów)

# Transport
`pymondis._models.Camp.Transport`
* Reprezentuje sposób dojazdu na obóz
## Konstrukcja
1. city: `str` (miasto)
2. one_way_price: `int` (cena przejazdu w jedną stronę)
3. two_way_price: `int` (cena przejazdu w dwie strony)

# Purchaser
`pymondis._models.Purchaser`
* Reprezentuje dane zamawiającego książkę
## Konstrukcja
1. name: `str` (imię)
2. surname: `str` (nazwisko)
3. email: `str` (email)
4. phone: `str` (numer telefonu)
5. parcel_locker: `str` (informacje o paczkomacie/paczkopunkcie, *nie tylko numer*)
6. http: `HTTPClient | None [None]` (client, który będzie domyślnie używany w order_fwb())
## Metody
1. `async` order_fwb(http: `HTTPClient | None [None]`)
   * Zamawia książkę „QUATROMONDIS – CZTERY ŚWIATY HUGONA YORCKA. OTWARCIE”.
   * Do wykonania zapytania używany jest `http` jeśli podany, w przeciwnym razie `self._http` (podany jako `http` w konstruktorze).

# PersonalReservationInfo
`pymondis._models.PersonalReservationInfo`
* Reprezentuje dane potrzebne do dostania informacji o rezerwacji
## Konstrukcja
1. reservation_id: `str` (kod rezerwacji)
2. surname: `str` (nazwisko)
3. http: `HTTPClient | None [None]` (client, który będzie domyślnie używany w get_details())
## Metody
1. `async` get_details(http: `HTTPClient | None [None]`) -> `dict[str, str | bool]`
   * Zwraca dane o rezerwacji

# Reservation
`pymondis._models.Reservation`
* Reprezentuje rezerwację
## Konstrukcja
1. camp_id: `int` (numer obozu)
2. child: `Child` ("Główne" dziecko)
3. parent_name: `str` (imię rodzica)
4. parent_surname: `str` (nazwisko rodzica)
5. nip: `str` (NIP rodzica)
6. email: `str` (email)
7. phone: `str` (numer telefonu)
8. poll: `SourcePoll` (źródło, z którego dowiedziałeś się o Quatromondis)
9. siblings: `list[Child]` ("Rodzeństwo" - reszta dzieci)
10. promo_code: `str` (Kod promocyjny)
11. http: `HTTPClient | None [None]` (client, który będzie domyślnie używany w tworzeniu `pri`)
## Metody
1. `property` pri(**kwargs) -> `PersonalReservationInfo`
   * Tworzy `PersonalReservationInfo` na podstawie siebie.
   * Kwargs zostaną podane dalej do konstruktora
   * Ta metoda może zostać w przyszłości usunięta na rzecz bezpośredniego `get_details`
2. `async` reserve_camp(http: `HTTPClient | None [None]`) -> `list[str]`
   * Rezerwuje obóz
   * Do wykonania zapytania używany jest `http` jeśli podany, w przeciwnym razie `self._http` (podany jako `http` w konstruktorze).

*Więcej dokumentacji później (chyba)*