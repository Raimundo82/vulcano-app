import fitz
from app.config import Config


def verificar_tarifario(pdf_path: str, tarifario: str = Config.TARIFARIO) -> bool:
    """
    Verifica se um determinado tarifário está presente no texto da fatura.

    Args:
        pdf_path (str): Caminho completo do ficheiro PDF.
        tarifario (str): Texto do tarifário a verificar.

    Returns:
        bool: True se o tarifário for encontrado, False caso contrário.
    """
    try:
        documento = fitz.open(pdf_path)
        for pagina in documento:
            texto = pagina.get_text("text")
            if tarifario in texto:
                return True
        return False
    except Exception as e:
        print(f"Erro ao verificar tarifário em {pdf_path}: {e}")
        return False


def verificar_conta(pdf_path: str, contas: list[str] = None) -> tuple[bool, str | None]:
    """
    Verifica se uma das contas fornecidas aparece na fatura.

    Args:
        pdf_path (str): Caminho do ficheiro PDF.
        contas (list[str], opcional): Lista de contas válidas.

    Returns:
        tuple[bool, str | None]: (True, conta encontrada) ou (False, None)
    """
    if contas is None:
        contas = Config.BLM_CONTRACT_NUMBERS + Config.VOZ_CONTRACT_NUMBERS

    try:
        documento = fitz.open(pdf_path)
        for pagina in documento:
            texto = pagina.get_text("text")
            for conta in contas:
                if conta in texto:
                    return True, conta
        return False, None
    except Exception as e:
        print(f"Erro ao verificar conta em {pdf_path}: {e}")
        return False, None