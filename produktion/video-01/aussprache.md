# Ausspracheliste — Video 1, „Who Built the First Roads and Why?"

> Für die TTS-QA vor dem Rendern. Grundlage: der Sprechtext in
> `skript.md` (Stand: fünfte Fassung) und die Stolperliste aus
> Prüfrunde 1 (`pruefprotokoll-runde-1.md`, Agent A3).
>
> Erzählsprache ist **Englisch**. Die Spalte **Respelling** ist das,
> was in der QA tatsächlich gehört und abgehakt wird — Großbuchstaben
> markieren die betonte Silbe. Die IPA-Spalte gibt die Herkunftsform,
> die Respelling-Spalte die im englischen Erzählfluss **empfohlene**
> Realisierung. Wo beides auseinanderfällt, steht der Grund in der
> letzten Spalte.
>
> Prüfweg: Jeden Eintrag im generierten Audio einzeln anhören. Bei
> Abweichung entweder Lexikon-Eintrag im TTS setzen oder die Stelle
> im Sprechtext umschreiben — **nicht** die Schreibung im Skript
> „phonetisch" verfälschen, sonst bricht der Abgleich mit
> `faktencheck.py`.

## Eigennamen aus A3s Stolperliste

| Name | Herkunft | IPA (Herkunft) | Respelling (empfohlen) | Vorkommen | Hinweis für die QA |
|---|---|---|---|---|---|
| **Dümmer** | Deutsch (See in Niedersachsen) | /ˈdʏmɐ/ | **DUEM-uh** — „ue" wie in französisch *tu*, Lippen gerundet | Absatz 6 | **Kritisch.** Englisch gelesen klingt es wie *dumber*. Wenn das TTS das ü nicht trifft, ist /ˈdiːmər/ („DEE-mer") die bessere Notlösung — *dumber* darf nie stehen bleiben. |
| **Campemoor** | Deutsch (Moor bei Vechta) | /ˈkampəmoːɐ̯/ | **KAHM-puh-mohr** | Absatz 6 | Nicht englisch „camp-uh-moor" mit /uː/. Das zweite Glied ist *Moor*, nicht *moor* wie im Englischen. |
| **Widan el-Faras** | Arabisch (Steinbruch, Ägypten) | /wiˈdaːn el ˈfaras/ | **wih-DAAN el FA-rass** | Absatz 10 | Betonung auf der zweiten Silbe von *Widan*; *Faras* mit kurzem a, Endung stimmlos. Bedeutet „Ohren der Stute". |
| **Nebuchadnezzar** | Englische Bibelform | /ˌnɛbjʊkədˈnɛzər/ | **neb-yoo-kad-NEZ-er** | Absatz 11 | Vier unbetonte Silben vor der Hauptbetonung — klassischer Vorlese-Stolperer. Im Text folgt „the Second": als *the second*, nicht *II*. |
| **Ishtar** | Akkadisch (Göttin, Stadttor) | /ˈɪʃtɑːr/ | **ISH-tar** | Absatz 11 | Erste Silbe betont, nicht *ish-TAR*. |
| **Susa** | Altpersisch (Stadt) | /ˈsuːsə/ | **SOO-suh** | Absatz 12 | Nicht *SYOO-*. |
| **Sardis** | Griechisch (Stadt) | /ˈsɑːrdɪs/ | **SAR-diss** | Absatz 12 | Steht direkt neben *Susa* — zwei S-Namen in Folge, hier braucht es eine hörbare Pause zwischen den beiden. |
| **Chaco** | Spanisch/Indigen (Canyon, New Mexico) | /ˈtʃɑːkoʊ/ | **CHAH-koh** | Absatz 13 | Nicht *SHAH-koh* und nicht *CHAK-oh*. |
| **Pueblo** | Spanisch | /ˈpwɛbloʊ/ | **PWEB-loh** | Absatz 13 | Erste Silbe einsilbig („pweb"), nicht *poo-EB-loh*. Im Text: „the Native Pueblo peoples". |
| **Wari** | Quechua (Kultur, Peru) | /ˈwɑːri/ | **WAH-ree** | Absatz 14 | Nicht *WOR-ee*. |
| **Tiwanaku** | Aymara (Kultur, Bolivien) | /ˌtiwɑːˈnɑːku/ | **tee-wah-NAH-koo** | Absatz 14 | Betonung auf der **dritten** Silbe. Steht unmittelbar hinter *Wari* — beide zusammen sind die schwerste Stelle des Absatzes. |
| **Westhay** | Englisch (Somerset) | /ˈwɛstheɪ/ | **WEST-hay** | Absatz 4 | Zwei klare Silben; das h wird gesprochen. |
| **Shapwick** | Englisch (Somerset) | /ˈʃæpwɪk/ | **SHAP-wick** | Absatz 4 | Nicht *shape-wick*. |
| **Qhapaq Ñan** | Quechua (Inka-Straßennetz) | /ˈqʰapaq ˈɲan/ | **KAH-pahk NYAHN** | — | **Kommt im Sprechtext nicht vor** (nur im Kopfteil von `skript.md`). Hier gelistet, falls eine spätere Fassung den Begriff aufnimmt. |

## Weitere QA-Punkte aus A3 (keine Eigennamen)

| Stelle | Problem | Vorgabe für die QA |
|---|---|---|
| **„Pr 31"** (Absatz 6) und **„Pr 7"** (Absatz 8) | Label ohne etablierte Sprechweise | Beide als **„P-R thirty-one"** bzw. **„P-R seven"** sprechen — Buchstaben einzeln, dann die Zahl. Einheitlich, sonst klingen die beiden Wege nach zwei verschiedenen Systemen. |
| **„3807 BC — or 3806"**, „3838 BC", „569 BC", „312 BC" | Vierstellige Jahreszahlen sind mehrdeutig sprechbar | Durchgängig als Ziffernpaare: **„thirty-eight-oh-seven B C"**, „thirty-eight-thirty-eight", „five-sixty-nine", „three-twelve". Nicht *three thousand eight hundred and seven*. |
| **„50.5 kilometres"** (Absatz 13) | Dezimalzahl im Fließtext | **„fifty point five"**. |
| **„the 25th century BC"** (Absatz 8) | Ordinalzahl | **„the twenty-fifth century B C"**. |
| **„BC"** generell | Buchstabenpaar | Immer **„B C"** als zwei Buchstaben, nie *before Christ* ausgeschrieben. |
| **„less than five centimetres thick"** (Absatz 4) | war vorher einheitenlos | Einheit ist seit der fünften Fassung im Text — in der QA nur prüfen, dass sie **mitgesprochen** wird. |
| **„But the day it was dressed for came once a year"** (Absatz 11) | Garden-Path-Syntax | Betonung auf **„for"**, danach kurze Pause vor „came". Ohne die Pause hört man „dressed for came" als Einheit. |
| **„work, war, worship, politics"** (Absatz 13) | drei w-Alliterationen mit Bruch | Gleichmäßiges Tempo, kein Beschleunigen; die Aufzählung ist bewusst viergliedrig. |
| **„wooden wedges, wooden mallets"** (Absatz 4) | w-Häufung | Bei zu hohem Tempo verschleift das zu einem Wort. |

## Abnahme

- [ ] Jeder Eintrag der oberen Tabelle einzeln im Audio gehört
- [ ] „Dümmer" klingt **nicht** wie *dumber*
- [ ] „Pr 31" und „Pr 7" gleich gesprochen
- [ ] Alle Jahreszahlen im Ziffernpaar-Format
- [ ] Keine Änderung an der Schreibung im Sprechtext von `skript.md`
