"""
Implementáld az alábbi függvényeket, melyek egy keresőmotor funkcióit látják el.
Készíthetsz további segédfüggvényeket is.
"""


def preprocess_text(text: str, min_length: int = 4) -> list[str]:
    """A megadott szöveget előkészíti indexeléshez vagy kereséshez.

    A szövegett kisbetűssé alakítja, töröli a nem betű karaktereket, majd
    szavakra bontja, és törli a túl rövid szavakat.

    >>> preprocess_text("Lenni, vagy nem lenni? Ez itt a kérdés...")
    ['lenni', 'vagy', 'lenni', 'kérdés']
    """
    return []


def create_index(list_file: str) -> dict[str, dict[str, int]]:
    """A megadott fájlban szereplő dokumentumokból elkészíti az indexet.

    A `list_file` minden sora egy dokumentum fájlnevét tartalmazza.

    Az index egy kétszintű szótár, melynek az elsődleges kulcsai a dokumentumok szavai,
    a másodlagos kulcsai a dokumentumok nevei, az értékek pedig a szavak gyakoriságai.

    A szöveget előkészíti a `preprocess_text` függvénnyel.

    >>> import json
    >>> index = create_index("articles.txt")
    >>> index == json.load(open("index.json", encoding="utf-8"))
    True
    """
    return {}


def are_similar(word1: str, word2: str) -> bool:
    """Visszaadja, hogy a két megadott szó hasonló-e.

    A két szó hasonló, ha:
        - Megegyeznek
        - Vagy a hosszabb szó tartalmazza a rövidebbet, és max. másfélszer olyan hosszú
        - Vagy a két szó csak egy karakterben tér el egymástól, azaz:
            - A rövidebb szó megkapható a hosszabb szó egy karakterének törlésével
            - Vagy a két szó egyforma hosszú, és csak egy helyen különböznek

    >>> are_similar("tigris", "tigrisek")
    True
    >>> are_similar("tigrisek", "tigris")
    True
    >>> are_similar("tigris", "tiger") == False
    True
    >>> are_similar("tigris", "tigris")
    True
    >>> are_similar("tigris", "tigriseket") == False
    True
    >>> are_similar("tigris", "tiggris")
    True
    >>> are_similar("amiatt", "amiat")
    True
    >>> are_similar("emiatt", "amiatt")
    True
    >>> are_similar("emiatt", "amiat") == False
    True
    >>> are_similar("amiatt", "amit") == False
    True
    """
    return True


def score(
    index: dict[str, dict[str, int]], query: str, similar: bool = False
) -> dict[str, float]:
    """Visszaadja azoknak a dokumentumoknak a neveit és pontszámait, melyek tartalmazzák
    a megadott kifejezést (részben vagy egészben).

    A pontszám a kifejezésben található szavak gyakoriságainak összege.
    A kifejezést előkészíti a `preprocess_text` függvénnyel, és törli az ismétlődéseket.

    Ha a `similar` paraméter igaz, akkor a kifejezésnek az indexben nem szereplő szavai
    helyett megkeresi a hasonló szavakat az `are_similar` függvénnyel, és ezeknek az
    átlagos pontszámát (pont / hasonló szavak száma) adja a dokumentumok pontszámához.

    >>> index = create_index("articles.txt")
    >>> score(index, "tigrisek")
    {'articles/444/megduplazodott-a-tigrisek-szama-2006-ota-indiaban.txt': 8.0, 'articles/index/tigris-india-vadvedelem-populacio-gyarapodas-50-eves-evfordulo.txt': 4.0, 'articles/origo/az-elso-bizonyitek-hogy-kardfogu-tigris-elt-iowa-allamban.txt': 1.0}
    >>> score(index, "tigrisék")
    {}
    >>> score(index, "tigrisék", similar=True)
    {'articles/444/megduplazodott-a-tigrisek-szama-2006-ota-indiaban.txt': 5.0, 'articles/index/tigris-india-vadvedelem-populacio-gyarapodas-50-eves-evfordulo.txt': 3.0, 'articles/origo/az-elso-bizonyitek-hogy-kardfogu-tigris-elt-iowa-allamban.txt': 2.0}
    >>> score(index, "európai tigrisek") == {'articles/444/megduplazodott-a-tigrisek-szama-2006-ota-indiaban.txt': 8.0, 'articles/index/tigris-india-vadvedelem-populacio-gyarapodas-50-eves-evfordulo.txt': 4.0, 'articles/origo/az-elso-bizonyitek-hogy-kardfogu-tigris-elt-iowa-allamban.txt': 1.0, 'articles/index/forint-dollar-euro-svajci-deviza-arfolyam.txt': 2.0}
    True
    """
    return {}


def search(
    index: dict[str, dict[str, int]],
    query: str,
    max_results: int = 3,
    similar: bool = False,
) -> list[str]:
    """Visszaadja a kifejezésre legnagyobb pontszámot elérő dokumentumok fájlneveit,
    pontszám szerint csökkenő sorrendben.

    Ha több találat van, csak az első `max_results` számút adja vissza.

    >>> index = create_index("articles.txt")
    >>> search(index, "európai tigrisek")
    ['articles/444/megduplazodott-a-tigrisek-szama-2006-ota-indiaban.txt', 'articles/index/tigris-india-vadvedelem-populacio-gyarapodas-50-eves-evfordulo.txt', 'articles/index/forint-dollar-euro-svajci-deviza-arfolyam.txt']
    """
    return []


def display_results(results: list[str]) -> None:
    """Megjeleníti a találati listát, a dokumentumok első sorával együtt.

    >>> index = create_index("articles.txt")
    >>> results = search(index, "európai tigrisek")
    >>> display_results(results)
    articles/444/megduplazodott-a-tigrisek-szama-2006-ota-indiaban.txt:
        Megduplázódott a tigrisek száma 2006 óta Indiában
    articles/index/tigris-india-vadvedelem-populacio-gyarapodas-50-eves-evfordulo.txt:
        Gyarapodtak a tigrisek Indiában
    articles/index/forint-dollar-euro-svajci-deviza-arfolyam.txt:
        Egy lépéssel hátrébb lépett a forint, hogy utána kettőt léphessen előre
    """
    pass


def main() -> None:
    """A program vezérlőfüggvénye.

    A program indításkor bekéri a felhasználótól a dokumentumok listáját tartalmazó fájl
    nevét, majd keresési kifejezéseket kér be, és megjeleníti a találatokat.

    Üres kifejezés esetén kilép a program.
    """
    pass


if __name__ == "__main__":
    main()
