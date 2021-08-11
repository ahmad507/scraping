from copy import deepcopy
from time import sleep

from pyquery import PyQuery as Pq
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as condition
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as Wait

import app
from app.remote.errorhandler import log, err_catch, log_driver, headless_web


class MainScript(object):
    def __init__(self, rekening='ss_test'):
        self._url = 'https://mcm2.bankmandiri.co.id'
        self.rekening = rekening
        self.is_login = False
        self.driver = None

    def __ss(self, funct_name):
        result = False
        try:
            if self.driver is not None:
                result = self.driver.save_screenshot('ss/mandirimcm/{}-{}.png'.format(self.rekening, funct_name))
        except Exception as e:
            log.error('Gagal capture!!!')
            log.error(str(e.args) + ', ' + str(result))

    def autorun(self, company, username, password, rekening=None, from_date=None, to_date=None):
        """autorun get mutasi"""
        if rekening is not None:
            self.rekening = rekening
        """ from_date to_date tidak diperlukan"""
        # if from_date is None:
        #     from_date = datetime.now().strftime('%m/%d/%Y')
        # if to_date is None:
        #     to_date = from_date
        try:
            log.info('MULAI')
            self.start_driver()
            # self.close_popup()  # bila ada popup
            self.ganti_bahasa()
            self.login(company, username, password)
            response = self.ambil_mutasi(rekening=self.rekening, from_date=from_date, to_date=to_date)
            result = {'code': 'OK', 'message': '', 'data': {'mutasi': response}}
            self.logout()
        except Exception as e:
            self.__ss('autorun-error')
            log.error(err_catch(e))
            result = {'code': 'ERROR', 'message': 'error - {}'.format(str(e)), 'data': None}
        finally:  # driver selalu di quit/close
            if self.is_login:
                self.logout()
            log.info('SELESAI')
            self.__ss('autorun-done')
            self.quit_driver()

        return result

    def start_driver(self):
        try:
            log.info('Start Driver')
            driver = app.ChromeDriver()  # Pilih driver: ChromeDriver() atau FirefoxDriver()
            headless = headless_web()
            write_log = log_driver()
            self.driver = driver.set_driver(headless=headless, write_log=write_log)
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
            Wait(self.driver, 30).until(condition.element_to_be_clickable(
                (By.XPATH, "//button[contains(.,'Bahasa')]")
            ))
            self.driver.find_element(By.XPATH, "//button[contains(.,'Bahasa')]").click()
        except Exception as e:
            log.error(err_catch(e))
            raise Exception(e)  # Stop bila gagal
        finally:
            self.__ss('ganti_bahasa')

    # noinspection DuplicatedCode,PyUnusedLocal
    def ambil_mutasi(self, rekening=None, from_date=None, to_date=None):
        result = []
        try:
            log.info('Ambil Mutasi')
            Wait(self.driver, 30).until(condition.element_to_be_clickable(
                (By.LINK_TEXT, 'Rekening')
            )).click()
            self.driver.find_element_by_xpath("//span[contains(.,'Rekening Koran')]").click()
            Wait(self.driver, 30).until(condition.presence_of_element_located(
                (By.XPATH, "//h2[contains(.,'Inkuiri Rekening Koran')]")
            ))
            Select(self.driver.find_element(By.XPATH, "//select")).select_by_visible_text('Perorangan')
            Wait(self.driver, 10).until(condition.element_to_be_clickable(
                (By.XPATH, "//span[contains(.,'Pilih Rekening')]")
            )).click()
            Wait(self.driver, 5).until(condition.element_to_be_clickable(
                (By.XPATH, "//span[contains(.,'" + rekening + "')]")
            )).click()
            el_select = Select(self.driver.find_element(By.NAME, 'postingDate'))
            el_select.select_by_visible_text('Hari ini')
            self.driver.find_element_by_xpath("//button[@type='submit']").click()
            Wait(self.driver, 10).until(condition.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'tbody')]")
            ))
            self.driver.find_element_by_xpath("//button[@type='submit']").send_keys(Keys.PAGE_DOWN)
            # sleep(3);
            # Save buat test scrap file html (lihat di main routes.py)
            save_file('ss/mandirimcm/{}-mutasi.html'.format(rekening), self.driver.page_source)
            # copy dari main routes.py /testscrap
            table_ = Pq(self.driver.page_source)('.table-div')
            body_ = Pq(table_)('.tbody .clearfix')
            div_tr = Pq(body_)('.tr')
            i = 0
            for row in div_tr:
                i += 1
                log.info('Ambil baris: ' + str(i))
                kolom = {}
                mutasi = Pq(row)('.td')
                kolom['tanggal'] = Pq(mutasi[1])('span').text()
                kolom['keterangan'] = Pq(mutasi[2])('span').text()
                kolom['code'] = Pq(mutasi[3])('span').text()
                kolom['debet'] = Pq(mutasi[4])('span').text()
                kolom['kredit'] = Pq(mutasi[5])('span').text()
                kolom['saldo'] = Pq(mutasi[6])('span').text()
                result.append(deepcopy(kolom))
        except Exception as e:
            log.error(err_catch(e))
        finally:
            self.__ss('ambil_mutasi')
        return result

    def login(self, company, username, password):
        try:
            log.info('Mencoba Login')
            Wait(self.driver, 30).until(condition.presence_of_element_located(
                (By.XPATH, "//label[contains(.,'ID Perusahaan')]//following::input[1]")
            ))
            Wait(self.driver, 5).until(condition.element_to_be_clickable(
                (By.XPATH, "//input[@type='password']")
            ))
            form = self.driver.find_element_by_xpath(".//ancestor::form")  # Batasi dari <form hingga </form>
            # Check benar-benar bahasa
            form.find_element_by_xpath("//label[contains(.,'ID Perusahaan')]//following::input[1]").send_keys(
                company)
            form.find_element_by_xpath("//label[contains(.,'ID Pengguna')]//following::input[1]").send_keys(
                username)
            form.find_element_by_xpath("//input[@type='password']").send_keys(password)
            form.find_element_by_xpath("//button[@type='submit']").click()
            Wait(self.driver, 10).until(condition.element_to_be_clickable(
                (By.CLASS_NAME, 'icon-logout')
            ))
            self.is_login = True
        except Exception as e:
            log.error(err_catch(e))
            raise Exception(e)  # Stop bila tidak bisa login
        finally:
            if self.is_login:
                self.__ss('login')
                log.info('Di dalam Login')
            else:
                log.info('Login Gagal')
                self.__ss('login-failed')

    def logout(self):
        try:
            log.info('Logout')
            Wait(self.driver, 15).until(condition.element_to_be_clickable(
                (By.CLASS_NAME, 'icon-logout')
            ))
            sleep(0.5)  # sering ada warning sebelum logout
            self.driver.find_element_by_class_name('icon-logout').click()
            # Tunggu sampai benar-benar keluar
            Wait(self.driver, 10).until(condition.presence_of_element_located(
                (By.XPATH, "//h2[contains(.,'Keluar')]")
            ))
            self.is_login = False
        except (AttributeError, Exception) as e:
            log.error(err_catch(e))
        finally:
            self.__ss('logout')

    def close_popup(self):
        try:
            log.info('Close Popup')
            self.driver.find_element_by_id('prompting-button').click()
        except Exception as e:
            log.error(err_catch(e))
        finally:
            self.__ss('close_popup')

    def close_tab(self):
        try:
            self.driver.close()
        except Exception as e:
            log.error(err_catch(e))

    def quit_driver(self):
        try:
            self.driver.quit()
        except Exception as e:
            log.error(err_catch(e))


def save_file(file_name, source):
    f = None
    try:
        f = open(file_name, 'w', encoding="utf-8")
        f.write(repr(source))
    except Exception as e:
        log.error(e.args)
    finally:
        f.close()
