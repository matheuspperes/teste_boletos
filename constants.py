from pathlib import Path

CURRENT_FOLDER = Path(__file__).parent

PDF_FOLDER = "pdf_files"
JSON_FOLDER = "json_files"

PREVIOUS_ITEM_TO_GET_NAME = 'Cedente Agência/Código do Cedente Espécie Quantidade Nosso número'
PREVIOUS_ITEM_TO_GET_DATA = 'Número do documento CPF/CNPJ Vencimento Valor documento'

NAME_REGEX = r'^([^\d]+?)(?=\s*\d)'