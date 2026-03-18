import unicodedata

def normalizar_nome(nome):
    if not nome:
        return ""
    
    nome = str(nome).strip().upper()
    
    nome = unicodedata.normalize('NFKD', nome)
    nome = "".join(c for c in nome if not unicodedata.combining(c))
    
    return nome


def normalizar_valor(valor):
    if valor is None:
        return 0.0

    if isinstance(valor, (int, float)):
        return float(valor)

    valor = str(valor).strip()

    # remove R$ e espaços
    valor = valor.replace("R$", "").replace(" ", "")

    # formato brasileiro
    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")

    try:
        return float(valor)
    except:
        return 0.0