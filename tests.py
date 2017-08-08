import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

CREATE_USER_URL = "http://atomicboard.devman.org/create_test_user/"
JQUERY_URL = "http://code.jquery.com/jquery-1.11.2.min.js"
TIMEOUT = 10


class AtomicPrj(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        driver = self.driver
        driver.get(CREATE_USER_URL)
        self.assertIn("Создать тестового пользователя", driver.title)
        driver.find_element_by_xpath("/html/body/form/button").click()
        driver.get('http://atomicboard.devman.org/#/')
        load_tasks = driver.find_element_by_css_selector("a[href='/']")
        load_tasks.click()
        wait = WebDriverWait(driver, TIMEOUT)
        self.tasks = '//span[@class="col-md-10 js-board-wrapper"]'
        wait.until(EC.visibility_of_element_located
                   ((By.XPATH, self.tasks)))

    def test_view_tasks(self):
        self.assertTrue(self.driver.find_element_by_xpath
                        (self.tasks))

    def test_ticket_condition_switch(self):
        driver = self.driver
        wait = WebDriverWait(driver, TIMEOUT)
        switcher = '//span[@class="badge ticket_status ng-binding"]'
        wait.until(EC.visibility_of_element_located
                   ((By.XPATH, switcher)))
        switcher_button = driver.find_element_by_xpath(switcher)
        switcher_button.click()
        switch_menu = '//*[@id="changeStatusModal"]/div/div'
        wait.until(EC.visibility_of_element_located
                   ((By.XPATH, switch_menu)))
        close_task_button = driver.find_element_by_xpath(
            '//*[@id="changeStatusModal"]//div[2]/div[3]/button')
        close_task_button.click()
        self.assertEqual('closed', switcher_button.text)

    def test_edit_task(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        task_text = "//span[1]/div/span[2]/div[2]/div[1]/span[1]"
        wait.until(EC.
                   element_to_be_clickable
                   ((By.XPATH, task_text)))
        task_text_field = self.driver.find_element_by_xpath(task_text)
        task_text_field.click()
        task_text_field_for_edit = self.driver.find_element_by_xpath(
            '//span[1]/div/span[2]/div[2]/div[1]/form/div/input')
        task_text_field_for_edit.clear()
        task_text_field_for_edit.send_keys('Test edit')
        submit_text_change_button = self.driver.find_element_by_xpath(
            '//span[2]/div[2]/div[1]/form/div/span/button[1]')
        submit_text_change_button.click()
        self.assertEqual('Test edit', task_text_field.text)

    def test_moving_tasks(self):
        with open("jquery_load_helper.js") as f:
            load_jquery_js = f.read()
        with open("drag_and_drop_helper.js") as f:
            drag_and_drop_js = f.read()
        wait = WebDriverWait(self.driver, TIMEOUT)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[2]/span[1]/div/span[2]/div[1]/h3")))
        srcipt_timeout_secononds = 30
        self.driver.set_script_timeout(srcipt_timeout_secononds)
        self.driver.execute_async_script(load_jquery_js, JQUERY_URL)
        # disregard PEP8 because selenium don't support drag&drop,
        # need JS
        self.driver.execute_script(
            drag_and_drop_js + "$('div.ticket__compact:eq(0)').simulateDragDrop({ dropTarget: 'span.tickets-column:eq(1)'});")
        moved_ticket = self.driver.find_element_by_xpath(
            '//span[1]/div/span[2]/div[2]/div[1]/span[1]')
        expected = 'Расчет радиационной стойкости. Пнуть математиков'
        self.assertEqual(expected, moved_ticket.text)

    def test_create_new_task(self):
        wait = WebDriverWait(self.driver, TIMEOUT)
        add_task_field_xpath = "//span[1]/div/span[2]/div[3]/span"
        wait.until(EC.element_to_be_clickable((
            By.XPATH, add_task_field_xpath)))
        add_task_field = self.driver.find_element_by_xpath(
            add_task_field_xpath)
        add_task_field.click()
        new_task_text_field_xpath = '//span[2]/div[3]/form/div/input'
        new_task_text_field = self.driver.find_element_by_xpath(
            new_task_text_field_xpath)
        new_task_text_field.send_keys('New test ticket')
        submit_new_task = '//span[2]/div[3]/form/div/span/button[1]'
        submit_new_task_button = self.driver.find_element_by_xpath(
            submit_new_task)
        submit_new_task_button.click()
        added_task_xpath = '//div/span[2]/div[3]/div[1]/span[1]'
        wait.until(EC.visibility_of_element_located((
            By.XPATH, added_task_xpath)))
        added_task = self.driver.find_element_by_xpath(
            added_task_xpath)
        self.assertEqual('New test ticket', added_task.text)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
