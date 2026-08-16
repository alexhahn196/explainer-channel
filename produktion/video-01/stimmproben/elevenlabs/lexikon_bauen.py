#!/usr/bin/env python3
"""Baut die ElevenLabs-Aussprachelexika aus `produktion/video-01/aussprache.md`.

Erzeugt zwei PLS-Dateien, weil ElevenLabs zwei verschiedene Regelarten kennt
und nicht jedes Modell beide versteht:

  lexikon_phoneme.pls  — <phoneme>-Regeln in IPA.
                         Laut Doku nur von Flash v2 / Turbo v2 (und v3)
                         ausgewertet; andere Modelle ueberspringen sie.
  lexikon_alias.pls    — <alias>-Regeln, also Ersatzschreibungen.
                         Von allen Modellen ausgewertet, also die einzige
                         Variante, die mit eleven_multilingual_v2 greift.

Quelle der Werte ist ausschliesslich die Tabelle in `aussprache.md`. Die
IPA-Spalte dort ist die *Herkunftsform*, die Respelling-Spalte die im
englischen Erzaehlfluss empfohlene Realisierung. Wo aussprache.md eine
ausdrueckliche Notloesung nennt (Duemmer), steht sie hier in `notloesung`
und wird fuer die Alias-Regel benutzt — die Alias-Regel muss englische
Orthographie sein, ein "ue" ist darin nicht schreibbar.
"""
from __future__ import annotations

import argparse
import pathlib
import xml.etree.ElementTree as ET

# grapheme, IPA (Herkunft, aus aussprache.md), Alias (englische Ersatzschreibung),
# Notloesung/Bemerkung
EIGENNAMEN = [
    ("Dümmer",         "ˈdʏmɐ",        "Deemer",
     "aussprache.md: engl. gelesen klingt es wie *dumber*; wenn das ue nicht "
     "sitzt, ist /ˈdiːmər/ die bessere Notloesung. Genau die steht im Alias."),
    ("Campemoor",      "ˈkampəmoːɐ̯",  "Kahm-puh-mohr",  ""),
    ("Widan el-Faras", "wiˈdaːn el ˈfaras", "wih-Dahn el Fah-rass", ""),
    ("Nebuchadnezzar", "ˌnɛbjʊkədˈnɛzər", "neb-yoo-kad-Nezzer", ""),
    ("Ishtar",         "ˈɪʃtɑːr",      "Ish-tar",        ""),
    ("Susa",           "ˈsuːsə",       "Soo-suh",        ""),
    ("Sardis",         "ˈsɑːrdɪs",     "Sar-diss",       ""),
    ("Chaco",          "ˈtʃɑːkoʊ",     "Chah-koh",       ""),
    ("Pueblo",         "ˈpwɛbloʊ",     "Pweb-loh",       ""),
    ("Wari",           "ˈwɑːri",       "Wah-ree",        ""),
    ("Tiwanaku",       "ˌtiwɑːˈnɑːku", "tee-wah-Nah-koo", ""),
    ("Westhay",        "ˈwɛstheɪ",     "West-hay",       ""),
    ("Shapwick",       "ˈʃæpwɪk",      "Shap-wick",      ""),
]

# Die Nicht-Eigennamen aus dem zweiten Tabellenblock von aussprache.md.
# Fuer diese gibt es keine sinnvolle Phonemregel — sie sind reine
# Ersatzschreibungen und stehen deshalb nur im Alias-Lexikon.
LESARTEN = [
    ("Pr 31",             "P-R thirty-one"),
    ("Pr 7",              "P-R seven"),
    ("3807 BC",           "thirty-eight-oh-seven B C"),
    ("3806",              "thirty-eight-oh-six"),
    ("3838 BC",           "thirty-eight-thirty-eight B C"),
    ("569 BC",            "five-sixty-nine B C"),
    ("312 BC",            "three-twelve B C"),
    ("50.5 kilometres",   "fifty point five kilometres"),
    ("25th century BC",   "twenty-fifth century B C"),
    ("BC",                "B C"),
]

PLS_NS = "http://www.w3.org/2005/01/pronunciation-lexicon"


def _lexicon(alphabet: str) -> ET.Element:
    root = ET.Element(
        "lexicon",
        {
            "version": "1.0",
            "xmlns": PLS_NS,
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": (
                f"{PLS_NS} "
                "http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"
            ),
            "alphabet": alphabet,
            "xml:lang": "en-US",
        },
    )
    return root


def _lexeme(root: ET.Element, grapheme: str, tag: str, value: str) -> None:
    lex = ET.SubElement(root, "lexeme")
    ET.SubElement(lex, "grapheme").text = grapheme
    ET.SubElement(lex, tag).text = value


def bauen(ziel: pathlib.Path) -> dict[str, int]:
    phon = _lexicon("ipa")
    for name, ipa, _alias, _hinweis in EIGENNAMEN:
        _lexeme(phon, name, "phoneme", ipa)

    alias = _lexicon("ipa")  # Alphabet ist bei reinen Alias-Regeln ohne Wirkung
    for name, _ipa, ersatz, _hinweis in EIGENNAMEN:
        _lexeme(alias, name, "alias", ersatz)
    for wort, ersatz in LESARTEN:
        _lexeme(alias, wort, "alias", ersatz)

    kopf = '<?xml version="1.0" encoding="UTF-8"?>\n'
    for datei, baum in (("lexikon_phoneme.pls", phon), ("lexikon_alias.pls", alias)):
        ET.indent(baum, space="  ")
        (ziel / datei).write_text(
            kopf + ET.tostring(baum, encoding="unicode") + "\n", encoding="utf-8"
        )

    return {
        "phoneme_regeln": len(EIGENNAMEN),
        "alias_regeln": len(EIGENNAMEN) + len(LESARTEN),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ziel", default=".", type=pathlib.Path)
    args = p.parse_args()
    args.ziel.mkdir(parents=True, exist_ok=True)
    zahlen = bauen(args.ziel)
    print(f"lexikon_phoneme.pls — {zahlen['phoneme_regeln']} Phonemregeln")
    print(f"lexikon_alias.pls   — {zahlen['alias_regeln']} Aliasregeln")
