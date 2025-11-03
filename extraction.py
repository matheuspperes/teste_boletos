import re
import traceback
from typing import Dict

import pdfplumber

from constants import NAME_REGEX, PREVIOUS_ITEM_TO_GET_DATA, PREVIOUS_ITEM_TO_GET_NAME


def extract_bill_info(pdf_path: str) -> Dict[str, str]:
    """
    Extract specific information from a Brazilian bill (boleto) PDF.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        Dict containing extracted information
    """

    # Result dictionary
    result = {
        "nome_razao_social": None,
        "numero_documento": None,
        "cpf_cnpj": None,
        "data_vencimento": None,
        "valor": None,
    }

    try:
        # OPENS PDF, EXTRACTS TEXT AND SPLITS INTO LINES
        with pdfplumber.open(pdf_path) as pdf:
            full_text = pdf.pages[0].extract_text()
            lines_list = full_text.split("\n")

        # FIND DEFAULT INDICES
        item_before_name = (
            lines_list.index(PREVIOUS_ITEM_TO_GET_NAME)
            if PREVIOUS_ITEM_TO_GET_NAME in lines_list
            else -1
        )
        name_item = (
            lines_list[item_before_name + 1]
            if item_before_name != -1 and item_before_name + 1 < len(lines_list)
            else None
        )

        name = re.search(NAME_REGEX, name_item)
        if name:
            result["nome_razao_social"] = name.group(1).strip()

        # FIND DEFAULT INDICES
        item_before_data = (
            lines_list.index(PREVIOUS_ITEM_TO_GET_DATA)
            if PREVIOUS_ITEM_TO_GET_DATA in lines_list
            else -1
        )
        data_item = (
            lines_list[item_before_data + 1]
            if item_before_data != -1 and item_before_data + 1 < len(lines_list)
            else None
        )
        data = data_item.split(" ") if data_item else []

        result["numero_documento"] = data[0]
        result["cpf_cnpj"] = data[1]
        result["data_vencimento"] = data[2]
        result["valor"] = data[3]

        return result

    except Exception:
        print(f"Error extracting data: {traceback.format_exc()}")
        return result
