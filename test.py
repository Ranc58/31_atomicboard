import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AtomicPrj(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS('D:\phantomjs-2.1.1-windows\\bin\phantomjs.exe')
        # self.driver = webdriver.Chrome('D:\chromedriver.exe')   TODO del chrome browser
        driver = self.driver
        driver.get("http://atomicboard.devman.org/create_test_user/")
        self.assertIn("Создать тестового пользователя", driver.title)
        create_button = driver.find_element_by_xpath("/html/body/form/button")
        create_button.click()

    def test_load_json_tickets(self):
        self.driver.get("http://atomicboard.devman.org/api/tickets/?format=json")
        assert "Authentication credentials were not provided" not in self.driver.page_source

    def test_view_tickets(self):
        self.driver.get('http://atomicboard.devman.org/#/')
        load_tasks_href = self.driver.find_element_by_css_selector("a[href='/']")
        load_tasks_href.click()
        wait = WebDriverWait(self.driver, 10)  # TODO maybe create var for 10 sec
        tickets_container = "/html/body/div[1]/div[1]/div[2]/span[1]/div/span[2]/div[1]/h3"
        self.assertTrue(wait.until(EC.visibility_of_element_located((By.XPATH, tickets_container))))

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
