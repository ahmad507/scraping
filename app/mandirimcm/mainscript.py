from datetime import datetime
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.webdriver.support.wait import WebDriverWait as Wait

import app
from app.remote.errorhandler import log, err_catch


class MainScript(object):
    def __init__(self, rekening='ss_test'):
        self._url = 'https://mcm2.bankmandiri.co.id'
        self.rekening = rekening
        self.is_login = False
        self.driver = None
        self.headless = True  # Bila ingin jalankan Web headless=False (jangan di Production)

    def __ss(self, funct_name):
        result = False
        try:
            if self.driver is not None:
                result = self.driver.save_screenshot('ss/mandirimcm/{}-{}.png'.format(self.rekening, funct_name))
        except Exception as e:
            log.error('Gagal capture!!!')
            log.error(str(e.args) + ', ' + str(result))
        # finally:
        #     if result is True:
        #         log.info('mandirimcm/{}-{}.png berhasil disimpan'.format(self.rekening, funct_name))
        #     else:
        #         log.info('mandirimcm/{}-{}.png GAGAL dicapture'.format(self.rekening, funct_name))

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
        except Exception as e:
            self.__ss('autorun-except')
            log.error(err_catch(e))
        finally:  # driver selalu di quit/close
            if self.is_login:
                self.logout()
            log.info('SELESAI')
            self.quit_driver()

        return result

    def start_driver(self):
        try:
            log.info('Start Driver')
            driver = app.ChromeDriver()  # Pilih driver: ChromeDriver() atau FirefoxDriver()
            headless = self.headless
            self.driver = driver.set_driver(headless=headless, write_log=False)
            self.driver.get(self._url)
        except Exception as e:
            log.error(err_catch(e))
            raise Exception(e)  # Stop bila gagal
        finally:
            # self.__ss('start_driver')
            pass  # Jarang gagal

    def ganti_bahasa(self):
        try:
            log.info('Ganti Bahasa')
            Wait(self.driver, 15).until(condition.presence_of_element_located(
                (By.XPATH, "//h4[contains(.,'Please Login')]")
            ))
            button = self.driver.find_elements_by_xpath('//button')
            # [0] Bahasa [1] English [2] Login
            button[0].click()
        except Exception as e:
            log.error(err_catch(e))
            raise Exception(e)  # Stop bila gagal
        finally:
            self.__ss('ganti_bahasa')

    def ambil_mutasi(self, from_date, to_date):
        self.__ss('ambil_mutasi')
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
        except Exception as e:
            self.__ss('login-fail')
            log.error(err_catch(e))
            raise Exception(e)  # Stop bila tidak bisa login
        finally:
            self.__ss('login')
            if self.is_login:
                log.info('Login Berhasil')
            else:
                log.info('Login Gagal')

    def logout(self):
        try:
            log.info('Logout')
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
        except (AttributeError, Exception) as e:
            log.error(err_catch(e))
        finally:
            self.__ss('logout')

    def close_popup(self):
        # noinspection PyBroadException
        try:
            log.info('Close Popup')
            self.driver.find_element_by_id('prompting-button').click()
        except Exception as e:
            self.driver.save_screenshot("ss/mandirimcm/{}-close_popup-fail.png".format(self.rekening))
            log.error(err_catch(e))
        finally:
            self.__ss('close_popup')

    def close_tab(self):
        # noinspection PyBroadException
        try:
            self.driver.close()
        except Exception as e:
            log.error(err_catch(e))

    def quit_driver(self):
        # noinspection PyBroadException
        try:
            self.driver.quit()
        except Exception as e:
            log.error(err_catch(e))
