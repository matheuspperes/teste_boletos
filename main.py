import datetime
import json
from pathlib import Path

from playwright.sync_api import Playwright, sync_playwright

from constants import CURRENT_FOLDER, JSON_FOLDER, PDF_FOLDER
from extraction import extract_bill_info


def check_folders():
    pdf_path = Path(CURRENT_FOLDER) / PDF_FOLDER
    json_path = Path(CURRENT_FOLDER) / JSON_FOLDER
    if not pdf_path.exists():
        pdf_path.mkdir(parents=True, exist_ok=True)
    if not json_path.exists():
        json_path.mkdir(parents=True, exist_ok=True)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Ensure the folders exists
    check_folders()

    page.goto("https://devtools.com.br/gerador-boleto/")

    with page.expect_popup() as page1_info:
        page.get_by_role("button", name="Gerar Boleto").click()
    page1 = page1_info.value
    page1.wait_for_load_state("networkidle")

    pdf_file_name = f"boleto_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_file_path = Path(CURRENT_FOLDER) / PDF_FOLDER / pdf_file_name
    page1.pdf(path=pdf_file_path)

    # ---------------------
    context.close()
    browser.close()

    # Extract structured data from the saved PDF
    result = extract_bill_info(str(pdf_file_path))
    print(result)

    # Save extracted data to a JSON file
    json_file_name = f"{result['cpf_cnpj']}-{result['numero_documento']}.json"
    json_file_path = Path(CURRENT_FOLDER) / JSON_FOLDER / json_file_name

    json_payload = {
        "Nome/Razão Social": result.get("nome_razao_social"),
        "Documento Federal (CPF/CNPJ)": result.get("cpf_cnpj"),
        "Data Vencimento": result.get("data_vencimento"),
        "Valor (R$)": result.get("valor"),
        "Número Documento": result.get("numero_documento"),
    }

    # Save JSON file
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(json_payload, f, ensure_ascii=False, indent=2)


with sync_playwright() as playwright:
    run(playwright)
