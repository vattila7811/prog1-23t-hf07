import os.path

def load_lines(filename: str) -> list[str]:
    if not os.path.exists(filename):
        print(f"Nincs ilyen fájl: {filename}")
        return []
         
    with open(filename, "r", encoding="utf-8") as fajl:
       return [line.rstrip() for line in fajl]    

    
