import re
from difflib import SequenceMatcher
import db

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
    return [word.lower() for word in re.sub('[^a-zA-ZáÁéÉíÍóÓőŐúÚűŰ ]', '', text.strip()).split(' ') if len(word) >= min_length]


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

    filelist = db.load_lines(list_file)
    word_index = {}

    for filename in filelist:
        article = db.load_lines(filename)
        for line in article:
            clean_line = preprocess_text(line)
            for word in clean_line:
                word_counts : dict = word_index.get(word, {})
                count = word_counts.get(filename, 0)
                word_counts[filename] = count + 1
                word_index[word] = word_counts

    return word_index


def string_distance(word1: str, word2: str) -> int:
    longer = max([len(word1), len(word2)])
    sm = SequenceMatcher(None, word1, word2)
    return longer - int(sm.ratio()*longer)


def string_consists_and_not_so_longer(word1: str, word2: str) -> bool:
    if len(word1) > len(word2):
        word1, word2 = word2, word1

    if word2.find(word1) > -1 and float(len(word2))/float(len(word1)) < 1.5:
        return True
    return False


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

    if word1.lower() == word2.lower() or string_distance(word1, word2) < 2:
        return True
    
    if string_consists_and_not_so_longer(word1, word2):
        return True

    return False


def collect_keywords(index: dict[str, dict[str, int]]) -> list[str]:
    return [keyword for keyword in index]


def similar_keywords(keylist: list[str], keyword: str) -> list[str]:
    return [keystr for keystr in keylist if are_similar(keystr, keyword) and keystr != keyword]


def collect_simple_scores(index: dict[str, dict[str, int]], querylist: set[str]) -> dict[str, float]:
    scores = {}
    for keyword in querylist:   
        for filename, score in index.get(keyword, {}).items():
            total = scores.get(filename, 0.)
            scores[filename] = float(total + score)
    return scores


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
    index_keywords = collect_keywords(index)
    querylist = set(preprocess_text(query))
    scores =  collect_simple_scores(index, querylist)

    if similar:
        for querystr in querylist:
            similarlist = similar_keywords(index_keywords, querystr)
            similarscores = collect_simple_scores(index, similarlist)
            for filename, score in similarscores.items():
                total = scores.get(filename, 0.)
                scores[filename] = total + score / float(len(similarlist))

    return scores 

def filename_with_max_score(scorelist: dict[str, float]) -> str:
    max_score = 0
    max_filename = ""
    for filename, score in scorelist.items():
        if score > max_score:
            max_filename = filename
            max_score = score
    return max_filename


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

    highscores = []
    scores = score(index, query, similar)
    steps = len(scores)  if max_results > len(scores) else max_results

    while steps > 0:
        filestr = filename_with_max_score(scores)
        scores.pop(filestr)
        highscores.append(filestr)
        steps -= 1

    return highscores


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
    
    for fajlnev in results:
        cikk = db.load_lines(fajlnev)
        print(f"{fajlnev}:")
        print(f"\t{cikk[0]}")

def flip_similar(similar: bool) -> bool:
    print(f'Hasonló: {not similar}')
    return not similar

def main() -> None:
    """A program vezérlőfüggvénye.

    A program indításkor bekéri a felhasználótól a dokumentumok listáját tartalmazó fájl
    nevét, majd keresési kifejezéseket kér be, és megjeleníti a találatokat.

    Üres kifejezés esetén kilép a program.
    """
    doclist = input("Dokumentumok listáját tartalmazó fájl: ")

    keyword_index = create_index(doclist)
    if len(keyword_index) == 0:
        print("Üres indexek! Kilépek!")
        return

    print("Indexek beolvasva!")
    similar = False
    while True:
        query = input(f"[Hasonló KI/BE - 0] [ENTER - kilépés] Keresőkulcs: ")
        match query:
            case "":
                print("Viszlát!")
                break
            case "0":
                similar = flip_similar(similar)
            case _:
                display_results(search(keyword_index, query, similar=similar))






if __name__ == "__main__":
    main()
