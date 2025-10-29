import webcolors
class Converter:
    def __init__(self):
        pass
        
    def get_coordinates_by_index(self,index, width=8):
        """Gibt die (x,y)-Koordinaten für einen gegebenen Index in einer Matrix der angegebenen Breite zurück."""
        if index < 0:
            raise ValueError("Index muss eine nicht-negative Ganzzahl sein.")
        x = index % width
        y = index // width
        return (x, y)
    def convert2Integer(self,value, default_value=None, min=None, max=None):
        try:
                if isinstance(value, str):
                    cleaned = value.strip()  # führende/trailing Spaces weg
                    cleaned = cleaned.replace(" ", "")  # Spaces löschen
                    cleaned = cleaned.replace("'", "")  # Tausendertrenner löschen
                    cleaned = cleaned.replace(",", "")  # Kommas löschen (z. B. 1,234 → 1234)
                    ret_val = int(float(cleaned))  # zuerst float, dann int
                else:
                    ret_val = int(float(value))  # auch bei int/float/anderen Typen

                # Min-/Max-Prüfung
                if min is not None and ret_val < min:
                    return min
                if max is not None and ret_val > max:
                    return max

                return ret_val

        except (TypeError, ValueError):
                return default_value
            
    def convert2Float(self,value, default_value=None, min=None, max=None):
        try:
            if isinstance(value, str):
                cleaned = value.strip()  # führende/trailing Spaces weg
                cleaned = cleaned.replace(" ", "")  # Spaces löschen
                cleaned = cleaned.replace("'", "")  # Tausendertrenner löschen
                cleaned = cleaned.replace(",", ".")  # Komma durch Punkt ersetzen
                ret_val = float(cleaned)
            else:
                # int, float und andere direkt versuchen
                ret_val = float(value)

            # Min-/Max-Prüfung
            if min is not None and ret_val < min:
                return min
            if max is not None and ret_val > max:
                return max

            return ret_val

        except (TypeError, ValueError):
            return default_value
    def convert2Boolean(self,value, default_value=None):
        try:
            if isinstance(value, str):
                cleaned = value.strip().lower()  # führende/trailing Spaces weg + lowercase
                if cleaned in ('1', 'true', 'yes', 'y'):
                    return True
                elif cleaned in ('0', 'false', 'no', 'n'):
                    return False
                else:
                    return default_value
            elif isinstance(value, (int, float)):
                return bool(value)  # 0 -> False, alles andere -> True
            elif isinstance(value, bool):
                return value
            else:
                return default_value
        except Exception:
            return default_value

    def convert2RGB(self,value, default_value=None):
        """
            print(convert2RGB((255,0,128)))        # (255, 0, 128)
            print(convert2RGB([0,128,255]))        # (0, 128, 255)
            print(convert2RGB("255,0,128"))        # (255, 0, 128)
            print(convert2RGB("0 128 255"))        # (0, 128, 255)
            print(convert2RGB("#ff00ff"))          # (255, 0, 255)
            print(convert2RGB("ff00ff"))           # (255, 0, 255)
            print(convert2RGB("red"))              # (255, 0, 0)
            print(convert2RGB("lightblue"))        # (173, 216, 230)
            print(convert2RGB(100))                # (100, 100, 100)
            print(convert2RGB("unknown", default_value=(0,0,0)))  # (0, 0, 0)
        """
        try:
            # Bereits Tuple/List mit 3 Elementen
            if isinstance(value, (tuple, list)) and len(value) == 3:
                return tuple(int(min(max(0, v), 255)) for v in value)

            # String-Verarbeitung
            elif isinstance(value, str):
                cleaned = value.strip().replace(" ", "").replace("'", "").lower()

                # Hex-Farbe
                if cleaned.startswith('#'):
                    cleaned = cleaned[1:]
                if len(cleaned) == 6 and all(c in '0123456789abcdef' for c in cleaned):
                    r = int(cleaned[0:2], 16)
                    g = int(cleaned[2:4], 16)
                    b = int(cleaned[4:6], 16)
                    return (r, g, b)

                # CSS3-Farbname
                try:
                    rgb = webcolors.name_to_rgb(cleaned)
                    return (rgb.red, rgb.green, rgb.blue)
                except ValueError:
                    pass  # kein bekannter Name, weitermachen

                # RGB-Komma- oder Leerzeichen-Format
                cleaned = cleaned.replace("(", "").replace(")", "")
                print(f'--> cleaned:{cleaned}')
                if ',' in cleaned:
                    parts = cleaned.split(',')
                else:
                    parts = cleaned.split()

                print(f'--> parts:{parts}')
                if len(parts) != 3:
                    return default_value
                return tuple(int(min(max(0, int(p)), 255)) for p in parts)

            # Einzelzahl → Grau
            elif isinstance(value, (int, float)):
                v = int(min(max(0, int(value)), 255))
                return (v, v, v)

            else:
                return default_value

        except Exception:
            return default_value

if __name__ == "__main__":
    conv = Converter()

    # Testfälle
    test_values = [
        (255, 0, 128),
        [0, 128, 255],
        "255,0,128",
        "0 128 255",
        "#ff00ff",
        "ff00ff",
        "red",
        "lightblue",
        100,
        "unknown"
    ]

    for val in test_values:
        rgb = conv.convert2RGB(val)
        print(f'convert2RGB({val!r}) = {rgb}')