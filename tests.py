import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CREATE_USER_URL = "http://atomicboard.devman.org/create_test_user/"
JQUERY_URL = "http://code.jquery.com/jquery-1.11.2.min.js"
TIMEOUT = 10


class AtomicPrj(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get(CREATE_USER_URL)
        self.assertIn("Создать тестового пользователя", driver.title)
        driver.find_element_by_xpath("/html/body/form/button").click()
        driver.get('http://atomicboard.devman.org/#/')
        load_tasks = driver.find_element_by_css_selector("a[href='/']")
        load_tasks.click()
        wait = WebDriverWait(driver, TIMEOUT)
        self.tasks = 'span.col-md-10.js-board-wrapper'
        wait.until(EC.visibility_of_element_located
                   ((By.CSS_SELECTOR, self.tasks)))

    def test_view_tasks(self):
        self.assertTrue(self.driver.find_element_by_css_selector(
                        self.tasks))

    def test_ticket_condition_switch(self):
        driver = self.driver
        wait = WebDriverWait(driver, TIMEOUT)
        switcher = 'span.badge.ticket_status.ng-binding'
        wait.until(EC.visibility_of_element_located
                   ((By.CSS_SELECTOR, switcher)))
        switcher_button = driver.find_element_by_css_selector(switcher)
        switcher_button.click()
        switch_menu = 'div.js-change-status-form.change-status-form'
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                     switch_menu)))
        close_task_button = driver.find_element_by_css_selector(
            'button.btn.btn-lg.btn-primary.change-status-form__button')
        close_task_button.click()
        self.assertEqual('closed', switcher_button.text)

    def test_edit_task(self):
        test_edit_task_title = 'Test edit'
        wait = WebDriverWait(self.driver, TIMEOUT)
        task_text = "span.panel-heading_text.js-panel-heading_text"
        wait.until(EC.
                   element_to_be_clickable
                   ((By.CSS_SELECTOR, task_text)))
        task_text_field = self.driver.find_element_by_css_selector(
            task_text)
        task_text_field.click()
        text_field_for_edit = self.driver.find_element_by_css_selector(
            'input.editable-has-buttons')
        text_field_for_edit.clear()
        text_field_for_edit.send_keys(test_edit_task_title)
        submit_button = self.driver.find_element_by_css_selector(
            'span.editable-buttons > button.btn.btn-primary')
        submit_button.click()
        self.assertEqual(test_edit_task_title, task_text_field.text)

    def test_moving_tasks(self):
        with open("jquery_load_helper.js") as f:
            load_jquery_js = f.read()
        with open("drag_and_drop_helper.js") as f:
            drag_and_drop_js = f.read()
        wait = WebDriverWait(self.driver, TIMEOUT)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             "div.panel-heading-no-padding.ticket__importance-5")))
        srcipt_timeout_secononds = 30
        self.driver.set_script_timeout(srcipt_timeout_secononds)
        self.driver.execute_async_script(load_jquery_js,
                                         JQUERY_URL)
        # disregard PEP8 because selenium don't support drag&drop,
        # need JS.
        # https://stackoverflow.com/a/29381532/8106659
        self.driver.execute_script(
            drag_and_drop_js +
            "$('div.ticket__compact:eq(0)').simulateDragDrop({ dropTarget: 'span.tickets-column:eq(1)'});")
        moved_ticket = self.driver.find_element_by_css_selector(
            'span.js-panel-heading_text:nth-child(2)')
        expected = 'Расчет радиационной стойкости. Пнуть математиков'
        self.assertEqual(expected, moved_ticket.text)

    def test_create_new_task(self):
        test_task_title = 'New test task'
        wait = WebDriverWait(self.driver, TIMEOUT)
        add_task_field_css = "span.add-ticket-block_button"
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                               add_task_field_css)))
        add_task_field = self.driver.find_element_by_css_selector(
            add_task_field_css)
        add_task_field.click()
        new_task_text_field_css = 'input.editable-has-buttons'
        new_task_text_field = self.driver.find_element_by_css_selector(
            new_task_text_field_css)
        new_task_text_field.send_keys(test_task_title)
        new_task_text_field.send_keys(Keys.ENTER)
        mounth_tasks = self.driver.find_element_by_css_selector(
            'span.col-md-4.tickets-column')
        new_task_xpath = '//span[contains(.,"New test task")]'
        wait.until(EC.visibility_of_element_located((By.XPATH,
                                                     new_task_xpath)))
        added_task_index = -1
        new_task = mounth_tasks.find_elements_by_css_selector(
            'span.panel-heading_text')[added_task_index]
        self.assertEqual(test_task_title, new_task.text)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
