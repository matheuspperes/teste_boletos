## teste_boletos

Gera um boleto de exemplo no site devtools.com.br, salva o PDF em `pdf_files/`, extrai campos principais do boleto e grava um JSON em `json_files/`.

Campos extraídos:
- Nome / Razão Social
- Documento Federal (CPF/CNPJ)
- Data Vencimento
- Valor (R$)
- Número Documento

### Requisitos
- Python 3.9+
- Google Chromium (instalado pelo Playwright automaticamente)

### Instalação (Windows / PowerShell)
- Há um processo automático em `run.bat`

```powershell
pipenv install
pipenv run python -m playwright install chromium
```

### Como executar
```powershell
python main.py
```

O script:
1. Abre o site gerador de boleto;
2. Gera o boleto em uma nova aba e salva o PDF em `pdf_files/` com timestamp;
3. Lê o PDF e extrai os dados usando `pdfplumber` e regras simples em `extraction.py`;
4. Salva um arquivo JSON ao lado do PDF (mesmo nome, extensão `.json`).

Exemplo de JSON gerado:
```json
{
	"Nome/Razão Social": "ACME LTDA",
	"Documento Federal (CPF/CNPJ)": "12.345.678/0001-90",
	"Data Vencimento": "10/11/2025",
	"Valor (R$)": "123,45",
	"Número Documento": "000123"
}
```

### Estrutura do projeto
```
constants.py        # Constantes usadas no projeto
extraction.py       # Função de extração de campos do PDF
main.py             # Gera o PDF via Playwright e grava o JSON com os dados extraídos
Pipfile             # Dependências Python (playwright, pdfplumber)
pdf_files/          # Pasta para PDFs
json_files/         # Pasta para JSONs
```

### Configuração e ajustes
- Em `constants.py` você pode ajustar:
	- `PDF_FOLDER`: pasta de saída dos PDFs (padrão: `pdf_files`)
	- `JSON_FOLDER`: pasta de saída dos JSONs (padrão: `json_files`)
	- `PREVIOUS_ITEM_TO_GET_NAME` e `PREVIOUS_ITEM_TO_GET_DATA`: gatilhos de texto usadas para localizar as linhas no PDF
	- `NAME_REGEX`: regex para isolar o nome/razão social

Feito com Playwright (para gerar/baixar o PDF) e pdfplumber (extração de PDF).