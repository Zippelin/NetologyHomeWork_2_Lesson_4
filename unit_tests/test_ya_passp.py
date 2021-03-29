from selenium import webdriver
import time
import pytest

from selenium.common.exceptions import NoSuchElementException


class TestYaPassp:
    __VALID_LONG = '12345678'
    __VALID_PWD = '12345678'
    __URL = 'https://passport.yandex.ru/auth/'

    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.__URL)
        time.sleep(2)
        self.login_button = self.driver.find_element_by_class_name('Button2_type_submit')
        self.login_field = self.driver.find_element_by_name('login')
        self.pwnd_field = ''

    @pytest.mark.order(1)
    def test_empty_login(self):
        self.login_button.click()
        time.sleep(2)
        try:
            self.error_msg = self.driver.find_element_by_class_name('Textinput-Hint_state_error')
        except NoSuchElementException:
            assert True is False, 'Ошибка: неверная реакция на невердный логин'

    @pytest.mark.order(2)
    def test_wrong_login(self):
        self.login_field.send_keys('1234567')
        self.login_button.click()
        time.sleep(2)
        try:
            self.pwnd_field = self.driver.find_element_by_id('passp-field-passwd')
        except NoSuchElementException:
            assert True is False, 'Ошибка: не появилось поле пароля'

    @pytest.mark.order(3)
    def test_wrong_pwd(self):
        self.pwnd_field = self.driver.find_element_by_id('passp-field-passwd')
        self.login_button = self.driver.find_element_by_class_name('Button2_type_submit')
        self.pwnd_field.send_keys('1234567')
        self.login_button.click()
        time.sleep(2)
        try:
            self.error_msg = self.driver.find_element_by_class_name('Textinput-Hint_state_error')
        except NoSuchElementException:
            assert True is False, 'Ошибка: неверная реакция на невердный пароль'

    @pytest.mark.order(4)
    def test_valid_data(self):
        reverse_login = self.driver.find_element_by_class_name('CurrentAccount')
        reverse_login.click()
        time.sleep(2)

        self.login_field = self.driver.find_element_by_name('login')
        self.login_field.send_keys(self.__VALID_LONG)

        self.login_button = self.driver.find_element_by_class_name('Button2_type_submit')
        self.login_button.click()
        time.sleep(2)

        self.pwnd_field = self.driver.find_element_by_id('passp-field-passwd')
        self.pwnd_field.send_keys(self.__VALID_PWD)

        self.login_button = self.driver.find_element_by_class_name('Button2_type_submit')
        self.login_button.click()
        time.sleep(2)

        assert self.driver.current_url != self.__URL, 'Ошибка: не произошел переход при верных данных авторизации'

    def teardown(self):
        self.driver.close()
        self.driver.quit()
