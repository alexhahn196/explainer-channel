# Ausspracheliste — Video 2, „How Do We Know How Far Away the Stars Are?"

> Für die TTS-QA vor dem Rendern. Grundlage ist der Abschnitt
> `## Sprechtext` in [`skript.md`](skript.md), 2.044 Wörter.
>
> Erzählsprache ist **Englisch**. Die Spalte **Respelling** ist das, was in
> der QA gehört und abgehakt wird — Großbuchstaben markieren die betonte
> Silbe. Die IPA-Spalte gibt die Herkunftsform, die Respelling-Spalte die im
> englischen Erzählfluss empfohlene Realisierung.
>
> Prüfweg wie bei Video 1: jeden Eintrag im erzeugten Audio einzeln anhören.
> Bei Abweichung entweder einen Lexikoneintrag im TTS setzen oder die Stelle
> im **Sprechtext** umschreiben — **nicht** die Schreibung in `skript.md`
> phonetisch verfälschen, sonst bricht der Abgleich mit den Quellen.
>
> Was hier steht, ist **ungeprüft**. Video 1 hatte einen gemessenen
> Hörbericht mit zwei Spracherkennern; für Video 2 gibt es den noch nicht.
> Die Schreibweisen folgen dem Respelling-Muster der gemessenen Fälle aus
> Video 1, sind aber selbst nicht nachgemessen.

## Eigennamen

| Name | Herkunft | IPA (Herkunft) | Respelling | Vorkommen | Hinweis für die QA |
|---|---|---|---|---|---|
| **Leavitt** | Englisch (Henrietta Swan Leavitt) | /ˈlɛvɪt/ | **LEV-it** | **14×** | **Der kritischste Eintrag, weil der häufigste.** Der naheliegende englische Fehlgriff ist *LEE-vit* — die Familie sprach es kurz, wie *level*. Steht auch als „Miss Leavitt" und „Leavitt's rung". |
| **Königsberg** | Deutsch (Stadt, heute Kaliningrad) | /ˈkøːnɪçsbɛʁk/ | **KOE-nigs-berg** | 8× | Der Umlaut ist die Falle: ein englisches TTS macht daraus je nach Modell *kai-nigs-berg* oder verschluckt das ö. Im Sprechtext steht darum `Koenigsberg` ohne Umlaut — das liest sich als *KOH-nigs-berg* und ist die gängige englische Anglisierung. |
| **Cepheid** / **Cepheids** | Griechisch über Latein (Sternbild Cepheus) | /ˈsɛfiːɪd/ | **SEF-ee-id** | 10× | **Kritisch, weil es der Fachbegriff des halben Videos ist.** Britisch auch /ˈsiːfiːɪd/ *SEEF-ee-id*; beides ist üblich, aber es muss **durchgängig dasselbe** sein. Nie *ke-FAY-id* und nie *SEP-heed*. |
| **Hipparcos** | Akronym der ESA (nach Hipparch) | /hɪˈpɑːrkɒs/ | **hip-AR-koss** | 6× | Betonung auf der zweiten Silbe. Nicht *HIP-ar-kohs* und nicht wie *Hipparchus* mit -kus. |
| **Gaia** | Griechisch (Erdgöttin), ESA-Mission | /ˈɡaɪ.ə/ | **GUY-uh** | 6× | Die ESA selbst sagt *GUY-uh*. Nicht *GAY-uh* und nicht dreisilbig *ga-EE-a*. |
| **Dorpat** | Deutsch/Estnisch (Tartu) | /ˈdɔrpat/ | **DOR-pat** | 5× | Zwei Silben, erste betont, kurzes a. Nicht *dor-PAT*. |
| **Vega** | Arabisch über Latein (Stern) | /ˈviːɡə/ | **VEE-guh** | 3× | Nicht *VAY-guh* — das ist die spanische Lesung. |
| **Pleiades** | Griechisch (Sternhaufen) | /ˈplaɪ.ədiːz/ | **PLY-uh-deez** | 3× | Drei Silben, erste betont. Nicht *PLEE-ah-des* und nicht *play-AH-deez*. |
| **SH0ES** | Akronym mit **Ziffer Null** statt O | /ʃuːz/ | **shoes** | 2× | **Kritisch und leicht zu übersehen.** Das Team schreibt sich mit einer Null: *Supernovae, H0, for the Equation of State*. Ein TTS liest das als *S-H-null-E-S*. Im Sprechtext steht darum `shoes`. |
| **Alpha Centauri** | Latein | /ˈælfə sɛnˈtɔːri/ | **AL-fuh sen-TOR-ee** | 1× | Betonung im zweiten Wort auf *tau*. |
| **Small Magellanic Cloud** | nach Magellan | /mædʒəˈlænɪk/ | **maj-uh-LAN-ik** | 1× | Betonung auf der dritten Silbe. Nicht *ma-GEL-a-nik*. |
| **Planck** | Deutsch (Max Planck), ESA-Mission | /plaŋk/ | **plahnk** | 1× | Das a ist dunkel wie in *palm*, nicht wie in *plank*. Englische Sprecher sagen meist *plank*; das ist hörbar falsch, aber verständlich — im Zweifel akzeptabel. |
| **Cygni** | Latein (Genitiv von *Cygnus*) | /ˈsɪɡnaɪ/ | **SIG-nye** | 1× | Steht als „61 Cygni": **sixty-one SIG-nye**, nicht *six-one* und nicht *SIG-nee*. |

Ohne Eintrag, weil im englischen Fluss unproblematisch: Earth, Sun, Moon,
Saturn, Milky Way, Rome, California, Cape of Good Hope, James Webb, Nobel
Prize, Danish, Italian, Swedish, European, January, July.

## Zahlen

| Stelle | Problem | Vorgabe |
|---|---|---|
| **„In 1543"** | Jahreszahl am Satzanfang | **„fifteen forty-three"** — als Ziffernpaare, nicht *one thousand five hundred and forty-three*. |
| **„around 1700"** | Runde Jahreszahl | **„around seventeen hundred"**. |
| **„0.125 arcseconds", „the modern 0.129"** | Dezimalzahl mit führender Null | **„zero point one two five"** und **„zero point one two nine"** — Ziffern einzeln nach dem Punkt, nicht *point one hundred twenty-five*. |
| **„67.4", „73.0", „67.8 to 70.4"** | Die Hubble-Zahlen, der Kern des Streits | **„sixty-seven point four"**, **„seventy-three point oh"**, **„sixty-seven point eight to seventy point four"**. Bei 73.0 muss die Null hörbar bleiben — sie trägt die Genauigkeit, um die der Streit geht. |
| **„118,000 stars"** | Tausendergruppe | **„a hundred and eighteen thousand"**. |
| **„759,000 kilometres"** | Tausendergruppe | **„seven hundred and fifty-nine thousand"**. |
| **„87,000 light-years"** | Tausendergruppe | **„eighty-seven thousand"**. |
| **„61 Cygni"** | Sternkatalognummer | **„sixty-one"**, nicht *six-one*. |
| **„a five-sigma difference"** | Fachausdruck | **„five-SIG-muh"** — als Wort, nicht als griechischer Buchstabe. |
| Jahreszahlen 1792, 1837, 1838, 1839, 1900, 1908, 1912, 1925, 1929, 1952, 1958, 2013, 2014, 2025 und „the 1990s" | vierstellig, aber eindeutig | **Nicht umgeschrieben.** Ein brauchbares TTS liest sie als Ziffernpaare. **In der QA einzeln gegenhören** — wenn eine als *one thousand …* kommt, kommt sie in die Ersetzungsliste in `sprechtext.py`. |
| **„435 to 445", „390", „444"** | Lichtjahre | **Nicht umgeschrieben.** In der QA gegenhören. |

## Was in der QA sonst zu hören ist

| Stelle | Warum |
|---|---|
| **„thirty cents an hour"** | Kommt zweimal vor und trägt beide Male denselben Punkt. Muss beide Male gleich klingen. |
| **„an arcsecond"**, **„arcseconds"** | Fachbegriff, sechsmal. Betonung auf *arc*. |
| **„a light-year"**, **„light-years"** | Achtmal. Als ein Wort mit Betonung auf *light*, nicht *light YEAR*. |
| **„one in four", „one in six"** | Anteile im Fließtext — als Wörter, nicht als Brüche gelesen. |
| **„H0"** | Kommt im Sprechtext **nicht** vor; hier nur notiert, falls eine späte Fassung es aufnimmt. Wäre **„H-nought"** oder **„H-zero"**, nie *ho*. |
