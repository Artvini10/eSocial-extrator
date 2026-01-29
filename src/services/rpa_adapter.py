from playwright.sync_api import sync_playwright

class RPAGovBR:
    def executar(self, cnpj):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state=f".auth/{cnpj}.json")
            page = context.new_page()
            page.goto("https://www.gov.br/esocial")
            page.pause()
            context.storage_state(path=f".auth/{cnpj}.json")
            browser.close()