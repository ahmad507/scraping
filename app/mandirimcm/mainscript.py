from datetime import datetime
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.webdriver.support.wait import WebDriverWait as Wait

import app
from app.remote.errorhandler import MyException, log


class MainScript(object):
    def __init__(self, rekening='ss_test'):
        self._url = 'https://mcm2.bankmandiri.co.id'
        self.rekening = rekening
        self.is_login = False
        self.driver = None
        self.headless = True  # Bila ingin jalankan Web headless=False (jangan di Production)

    # def __screenshot(self):
    #     try:
    #         if self.driver is not None:
    #             self.driver.save_screenshot("ss/mandirimcm/{}-autorun-fail.png".format(self.rekening))
    #

    def autorun(self, company, username, password, rekening=None, from_date=None, to_date=None):
        result = []
        if rekening is not None:
            self.rekening = rekening
        if from_date is None:
            from_date = datetime.strptime(datetime.now(), '%Y-%m-%d').strftime('%d/%m/%Y')
        if to_date is None:
            to_date = from_date
        try:
            log.info('MULAI')
            self.start_driver()
            # self.close_popup()  # bila ada popup
            self.ganti_bahasa()
            self.login(company, username, password)
            # self.ambil_mutasi(from_date, to_date)
            self.logout()
        except MyException as e:
            self.driver.save_screenshot("ss/mandirimcm/{}-autorun-fail.png".format(rekening))
            log.error(e.args)
        finally:  # driver selalu di quit/close
            if self.is_login:
                self.logout()
            log.info('SELESAI')
            self.quit_driver()

        return result

    def start_driver(self):
        try:
            driver = app.ChromeDriver()  # Pilih driver: ChromeDriver() atau FirefoxDriver()
            headless = self.headless
            self.driver = driver.set_driver(headless=headless, write_log=False)
            self.driver.get(self._url)
        except MyException as e:
            self.driver.save_screenshot("ss/mandirimcm/{}-start_driver-fail.png".format(self.rekening))
            raise log.error(e.args)  # Stop bila gagal
        finally:
            log.info('Start Driver')

    def ganti_bahasa(self):
        try:
            Wait(self.driver, 15).until(condition.presence_of_element_located(
                (By.XPATH, "//h4[contains(.,'Please Login')]")
            ))
            button = self.driver.find_elements_by_xpath('//button')
            # [0] Bahasa [1] English [2] Login
            button[0].click()
        except MyException as e:
            self.driver.save_screenshot("ss/mandirimcm/{}-ganti_bahasa-fail.png".format(self.rekening))
            raise log.error(e.args)  # Stop bila gagal
        finally:
            log.info('Ganti Bahasa')

    def ambil_mutasi(self, from_date, to_date):
        self.driver.save_screenshot("ss/mandirimcm/{}-ambil_mutasi-fail.png".format(self.rekening))
        pass

    def login(self, company, username, password):
        try:
            log.info('Mencoba Login')
            Wait(self.driver, 5).until(condition.element_to_be_clickable(
                (By.XPATH, "//label[contains(.,'ID Perusahaan')]//following::input[1]")
            ))
            form = self.driver.find_element_by_xpath(".//ancestor::form")  # Batasi dari <form hingga </form>
            form.find_element_by_xpath("//label[contains(.,'ID Perusahaan')]//following::input[1]").send_keys(
                company)
            form.find_element_by_xpath("//label[contains(.,'ID Pengguna')]//following::input[1]").send_keys(
                username)
            form.find_element_by_xpath("//label[contains(.,'Kata Sandi')]//following::input[1]").send_keys(
                password)
            form.find_element_by_xpath(".//*[@type='submit']").click()
            Wait(self.driver, 10).until(condition.element_to_be_clickable(
                (By.CLASS_NAME, 'icon-logout')
            ))
            self.is_login = True
        except MyException as e:
            self.driver.save_screenshot("ss/mandirimcm/{}-login-fail.png".format(self.rekening))
            raise log.error(e.args)  # Stop bila tidak bisa login
        finally:
            if self.is_login:
                log.info('Login Berhasil')
            else:
                log.info('Login Gagal')

    def logout(self):
        try:
            Wait(self.driver, 5).until(condition.element_to_be_clickable(
                (By.CLASS_NAME, 'icon-logout')
            ))
            sleep(0.5)  # sering ada warning sebelum logout
            self.driver.find_element_by_class_name('icon-logout').click()
            # Tunggu sampai benar-benar keluar
            Wait(self.driver, 5).until(condition.presence_of_element_located(
                (By.XPATH, "//h2[contains(.,'Keluar')]")
            ))
            self.is_login = False
        except MyException as e:
            self.driver.save_screenshot("ss/mandirimcm/{}-logout-fail.png".format(self.rekening))
            log.error(e.args)
        finally:
            log.info('Logout')

    def close_popup(self):
        try:
            self.driver.find_element_by_id('prompting-button').click()
        except MyException as e:
            self.driver.save_screenshot("ss/mandirimcm/{}-close_popup-fail.png".format(self.rekening))
            log.error(e.args)
        finally:
            log.info('Close Popup')

    def close_tab(self):
        try:
            self.driver.close()
        except MyException as e:
            log.error(e.args)

    def quit_driver(self):
        try:
            self.driver.quit()
        except MyException as e:
            log.error(e.args)
