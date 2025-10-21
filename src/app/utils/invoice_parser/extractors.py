import fitz # PyMuPDF
import re
from typing import List, Optional, Tuple

_ACCOUNT_RE = re.compile(r"N[ºo]?\s*Conta\s*:\s*(\d+)", flags=re.IGNORECASE)

def extrair_data_emissao(pdf_path: str) -> str | None:
    """
    Extrai a data de emissão do PDF a partir da localização do texto "Data de emissão:".

    Args:
        pdf_path (str): Caminho absoluto ou relativo para o arquivo PDF.

    Returns:
        str | None: A data de emissão extraída do PDF (ex: "2024-11-15"),
        ou None se não for encontrada.
    """
    try:
        documento = fitz.open(pdf_path)

        for pagina in documento:
            texto_procurado = "Data de emissão:"
            areas_encontradas = pagina.search_for(texto_procurado)

            if areas_encontradas:
                for area in areas_encontradas:
                    _0, y0, _1, y1 = area
                    # Define a região onde o valor da data é esperado
                    area_valor = fitz.Rect(140, y0, 230, y1)
                    issue_date = pagina.get_textbox(area_valor)
                    if issue_date:
                        return issue_date.strip()

        return None

    except Exception as e:
        print(f"Erro ao extrair data de emissão de {pdf_path}: {e}")
        return None
    
def extrair_contribuinte(pdf_path: str) -> str | None:
    """
    Extrai o número do contribuinte (NIF) do PDF.

    Procura pelo texto "Nº Contribuinte:" e lê o valor numérico à direita
    dessa expressão dentro de uma região delimitada.

    Args:
        pdf_path (str): Caminho do arquivo PDF.

    Returns:
        str | None: O número de contribuinte (ex: "123456789"),
        ou None se não for encontrado.
    """
    try:
        documento = fitz.open(pdf_path)

        for pagina in documento:
            texto_procurado = "Nº Contribuinte:"
            areas_encontradas = pagina.search_for(texto_procurado)

            if areas_encontradas:
                for area in areas_encontradas:
                    _0, y0, _1, y1 = area
                    # Define a região onde o valor do contribuinte aparece
                    area_valor = fitz.Rect(140, y0, 230, y1)
                    taxpayer_number = pagina.get_textbox(area_valor)
                    if taxpayer_number:
                        return taxpayer_number.strip()

        return None

    except Exception as e:
        print(f"Erro ao extrair contribuinte de {pdf_path}: {e}")
        return None
    
def extrair_valor_total_da_fatura(pdf_path: str) -> float | None:
    """
    Extrai e converte o valor total da fatura a partir de um ficheiro PDF.

    Procura o texto "Valor total da fatura" e lê o valor à direita,
    removendo símbolos, espaços e formatando para número decimal.

    Args:
        pdf_path (str): Caminho do ficheiro PDF.

    Returns:
        float | None: Valor total da fatura em formato numérico, ou None se não encontrado.
    """
    try:
        documento = fitz.open(pdf_path)
    except Exception as e:
        print(f"Erro ao abrir o PDF '{pdf_path}': {e}")
        return None

    for pagina in documento:
        texto_procurado = "Valor total da fatura"
        for area in pagina.search_for(texto_procurado) or []:
            _, y0, _, y1 = area  
            texto_valor = _extrair_texto_valor(pagina, y0, y1)
            if texto_valor:
                return _converter_valor_para_float(texto_valor)

    return None

def _extrair_texto_valor(pagina, y0: float, y1: float) -> str | None:
    """Extrai o texto na região onde o valor numérico é esperado."""
    try:
        area_valor = fitz.Rect(510, y0, 620, y1)
        texto_valor = pagina.get_textbox(area_valor)
        return texto_valor.strip() if texto_valor else None
    except Exception as e:
        print(f"Erro ao ler texto da página: {e}")
        return None

def _converter_valor_para_float(texto_valor: str) -> float | None:
    """Limpa e converte o valor de texto para float."""
    try:
        valor_limpo = (
            texto_valor.replace("€", "")
            .replace(",", ".")
            .replace(" ", "")
            .strip()
        )

        # Corrige pontos a mais (ex: "1.234.56" → "1234.56")
        if valor_limpo.count(".") > 1:
            partes = valor_limpo.split(".")
            valor_limpo = "".join(partes[:-1]) + "." + partes[-1]

        return float(valor_limpo)
    except ValueError:
        print(f"Valor inválido: '{texto_valor}'")
        return None
    
def extract_client_by_coordinates(pdf_path: str, coordinates: fitz.Rect) -> str | None:
    """
    Extrai o nome do cliente de uma fatura PDF com base nas coordenadas indicadas.

    Esta função abre o PDF, lê o texto presente na área definida por `coordinates`
    e remove caracteres inválidos para nomes de ficheiros (ex: \ / : * ? < > |).

    Args:
        pdf_path (str): Caminho absoluto ou relativo para o ficheiro PDF.
        coordinates (fitz.Rect): Objeto `Rect` que define a área onde o nome do cliente se encontra.

    Returns:
        str | None: Nome do cliente extraído (limpo e formatado), ou None se não encontrado.
    """
    try:
        # Abre o PDF e seleciona a primeira página
        documento = fitz.open(pdf_path)
        if not documento or len(documento) == 0:
            print(f"O ficheiro PDF '{pdf_path}' está vazio ou corrompido.")
            return None

        pagina = documento[0]
        texto_extraido = pagina.get_textbox(coordinates)

        if not texto_extraido:
            return None

        # Remove caracteres inválidos para nomes de ficheiros
        texto_limpo = re.sub(r'[\\/:"*?<>|]+', "_", texto_extraido)
        return texto_limpo.strip() if texto_limpo else None

    except Exception as e:
        print(f"Erro ao extrair cliente do PDF '{pdf_path}': {e}")
        return None
    
def extract_address_by_coordinates(pdf_path: str, coordinates: fitz.Rect) -> str | None:
    """
    Extrai o endereço de um cliente a partir de um ficheiro PDF,
    com base nas coordenadas fornecidas.

    Esta função lê o texto da primeira página do documento, na
    área definida por `coordinates`, e devolve o conteúdo limpo.

    Args:
        pdf_path (str): Caminho absoluto ou relativo para o ficheiro PDF.
        coordinates (fitz.Rect): Área da página (objeto Rect) onde o endereço se encontra.

    Returns:
        str | None: Endereço extraído (sem espaços adicionais),
        ou None se o texto não for encontrado ou ocorrer um erro.
    """
    try:
        documento = fitz.open(pdf_path)
        if not documento or len(documento) == 0:
            print(f"O ficheiro PDF '{pdf_path}' está vazio ou corrompido.")
            return None

        pagina = documento[0]
        texto_extraido = pagina.get_textbox(coordinates)

        if texto_extraido:
            return texto_extraido.strip()

        return None

    except Exception as e:
        print(f"Erro ao extrair endereço do PDF '{pdf_path}': {e}")
        return None
    

def extract_account(text: str) -> str | None:
    """
    Extrai o número de conta a partir do texto.
    Aceita variantes como: 'Nº Conta: 123', 'Nº Conta : 123', 'No Conta: 123' etc.
    """
    try:
        m = _ACCOUNT_RE.search(text)
        return m.group(1) if m else None
    except Exception as e:
        print(f"Erro ao extrair número de conta: {e}")
        return None
    
def verificar_tarifario(pdf_path: str, tarifario: str) -> bool:
    """
    Verifica se o tarifário especificado está presente no conteúdo do PDF.

    Args:
        pdf_path (str): Caminho para o ficheiro PDF a ser analisado.
        tarifario (str): Texto do tarifário a procurar dentro do documento.

    Returns:
        bool: 
            - True se o tarifário for encontrado em qualquer página do PDF.
            - False caso contrário ou em caso de erro ao processar o ficheiro.
    """
    try:
        with fitz.open(pdf_path) as documento:
            for pagina in documento:
                texto = pagina.get_text("text")
                if tarifario in texto:
                    return True
        return False

    except Exception as e:
        print(f"⚠️ Erro ao verificar tarifário no arquivo '{pdf_path}': {e}")
        return False
    
def verificar_conta(pdf_path: str, contas: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Verifica se alguma das contas especificadas está presente no conteúdo do PDF.

    Args:
        pdf_path (str): Caminho para o ficheiro PDF a ser analisado.
        contas (List[str]): Lista de números de conta a procurar no texto do PDF.

    Returns:
        Tuple[bool, Optional[str]]:
            - O primeiro elemento indica se alguma conta foi encontrada (True/False).
            - O segundo elemento é o número da conta encontrada ou extraída (str ou None).
    """
    try:
        with fitz.open(pdf_path) as documento:
            for pagina in documento:
                texto = pagina.get_text("text")

                # Tenta extrair um número de conta diretamente
                conta_extr = extract_account(texto)

                # Verifica se alguma das contas conhecidas aparece no texto
                for conta in contas:
                    if conta in texto:
                        return True, conta

        # Caso nenhuma conta conhecida tenha sido encontrada
        return False, conta_extr.group(1) if conta_extr else None

    except Exception as e:
        print(f"⚠️ Erro ao verificar conta no arquivo '{pdf_path}': {e}")
        return False, None