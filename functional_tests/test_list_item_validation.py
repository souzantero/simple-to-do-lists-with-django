from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith acessa a página inicial e acidentalmente tenta submeter
        # um item vazio na lista. Ela tecla Enter na caixa de entrada vazia
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # O navegador intercepta a requisição e não carrega a página da lista
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:invalid')
        )

        # Ela começa a digitar um texto para o novo item e o erro desaparece
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:valid')
        )

        # Ela pode submeter o item com sucesso
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # De forma perversa, ela agora decide submeter um segundo item em branco na lista
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Novamente, o navegador não concordará
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda:
            self.browser.find_elements_by_css_selector('#id_text:invalid')
        )

        # E ela pode corrigir isso preenchendo o item com um texto
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda:
            self.browser.find_elements_by_css_selector('#id_text:valid')
        )

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

