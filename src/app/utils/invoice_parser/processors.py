def process_amount_to_pay(amount_str: str) -> float | None:
    """
    Processa o valor de amount_to_pay e converte para float.
    Exemplo: "1 234,56 €" → 1234.56

    Args:
        amount_str (str): O valor a ser processado.

    Returns:
        float | None: O valor concertido em float, ou None senão for possível
    """
    if not amount_str:
        return None

    try:
        cleaned = (
            amount_str.replace("€", "")
            .replace(",", ".")
            .replace(" ", "")
            .strip()
        )
        return float(cleaned)
    except ValueError as e:
        print(f"Erro ao converter amount_to_pay para float: {amount_str} - {e}")
        return None
    
