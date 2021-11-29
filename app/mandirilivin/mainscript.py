from copy import deepcopy
from datetime import datetime
from time import sleep

from pyquery import PyQuery as Pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.webdriver.support.wait import WebDriverWait as Wait

import app
from app.remote.errorhandler import log, err_catch, log_driver, headless_web


class MainScript(object):
    def __init__(self, rekening='ss_test'):
        self._url = 'https://ibank.bankmandiri.co.id/retail3/'
        self.profile = 'Chrome_mandirilivin'
        self.rekening = rekening
        self.is_login = False
        self.driver = None

    def __ss(self, funct_name):
        result = False
        try:
            if self.driver is not None:
                result = self.driver.save_screenshot('ss/mandirilivin/{}-{}.png'.format(self.rekening, funct_name))
        except Exception as e:
            log.error('Gagal capture!!!')
            log.error(str(e.args) + ', ' + str(result))

    def autorun(self, company, username, password, rekening=None, from_date=None, to_date=None):
        """autorun get mutasi"""
        if rekening is not None:
            self.rekening = rekening
        if from_date is None:
            from_date = datetime.now().strftime('%d/%m/%Y')
        if to_date is None:
            to_date = from_date
        try:
            log.info('MULAI')
            self.start_driver()
            # self.close_popup()  # bila ada popup
            # self.ganti_bahasa()
            self.login(company, username, password)
            response = self.ambil_mutasi(rekening=self.rekening, from_date=from_date, to_date=to_date)
            result = {'code': 'OK', 'message': '', 'data': {'mutasi': response}}
            self.logout()
        except Exception as e:
            self.__ss('autorun-error')
            log.error(err_catch(e))
            result = {'code': 'ERROR', 'message': 'error - {}'.format(str(e)), 'data': None}
        finally:  # driver selalu di logout
            if self.is_login:
                self.logout()
            log.info('SELESAI')
            self.__ss('autorun-done')
            self.quit_driver()

        return result

    def start_driver(self):
        try:
            log.info('Start Driver')
            headless = headless_web()
            write_log = log_driver()
            driver = app.ChromeDriver(profile=self.profile)  # Pilih driver: ChromeDriver() atau FirefoxDriver()
            self.driver = driver.set_driver(headless=headless, write_log=write_log)
            self.driver.get(self._url)
        except Exception as e:
            log.error(err_catch(e))
            raise Exception(e)  # Stop bila gagal
        finally:
            # self.__ss('start_driver')
            pass

    def ganti_bahasa(self):
        try:
            log.info('Ganti Bahasa')
            raise Exception('Dalam development')
        except Exception as e:
            log.error(err_catch(e))
            raise Exception(e)  # Stop bila gagal
        finally:
            # self.__ss('ganti_bahasa')
            pass

    # noinspection PyUnusedLocal
    def ambil_mutasi(self, rekening=None, from_date=None, to_date=None):
        result = []
        if from_date is None:
            from_date = datetime.now().strftime('%d/%m/%Y')
        if to_date is None:
            to_date = from_date
        try:
            log.info('Ambil Mutasi')
            Wait(self.driver, 20).until(condition.element_to_be_clickable(
                (By.XPATH, "//a[@id='currentId-" + rekening + "']/div")
            )).click()
            Wait(self.driver, 15).until(condition.presence_of_element_located(
                (By.ID, 'panelSearch')
            ))
            self.driver.execute_script("$('#fromDate').val('{}')".format(from_date))
            self.driver.execute_script("$('#toDate').val('{}')".format(to_date))
            sleep(2)
            Wait(self.driver, 5).until(condition.element_to_be_clickable(
                (By.ID, 'btnSearch')
            )).click()
            Wait(self.driver, 20).until(condition.invisibility_of_element(
                (By.XPATH, "//td[contains(.,'Loading...')]")
            ))
            Wait(self.driver, 5).until(condition.presence_of_element_located(
                (By.ID, 'globalTable')
            ))
            # sleep(3);
            # Save buat test scrap file html (lihat di main routes.py)
            # save_file('ss/mandirilivin/{}-mutasi.html'.format(rekening), self.driver.page_source)
            # copy dari main routes.py /testscrap
            table_ = Pq(self.driver.page_source)('#globalTable')
            body_ = Pq(table_)('table tbody')
            div_tr = Pq(body_)('tr')
            i = 0
            for row in div_tr:
                i += 1
                log.info('Ambil baris: ' + str(i))
                kolom = {}
                mutasi = Pq(row)('td')
                check_data = Pq(mutasi[0]).text()
                if check_data[0:14] == 'Tidak ada data':
                    continue
                kolom['tanggal'] = Pq(mutasi[0]).text()
                kolom['keterangan'] = Pq(mutasi[1]).text()
                kolom['code'] = ''
                kolom['debet'] = Pq(mutasi[2]).text()
                kolom['kredit'] = Pq(mutasi[3]).text()
                kolom['saldo'] = ''
                result.append(deepcopy(kolom))
        except Exception as e:
            log.error(err_catch(e))
            log.error('Rekening error: ' + rekening)
        finally:
            self.__ss('ambil_mutasi')
        return result

    def login(self, company, username, password):
        try:
            log.info('Mencoba Login')
            Wait(self.driver, 70).until(condition.frame_to_be_available_and_switch_to_it(
                (By.NAME, 'mainFrame')
            ))
            Wait(self.driver, 5).until(condition.presence_of_element_located(
                (By.XPATH, "//html[@id='login-page']")
            ))
            self.driver.find_element_by_id('userid_sebenarnya').send_keys(username)
            self.driver.find_element_by_id('pwd_sebenarnya').send_keys(password)
            self.driver.find_element_by_id('btnSubmit').click()
            Wait(self.driver, 40).until(condition.presence_of_element_located(
                (By.CLASS_NAME, 'mdr-logout')
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
            Wait(self.driver, 10).until(condition.element_to_be_clickable(
                (By.CLASS_NAME, 'mdr-logout')
            )).click()
            Wait(self.driver, 5).until(condition.element_to_be_clickable(
                (By.ID, 'btnCancelReg')
            )).click()
            Wait(self.driver, 5).until(condition.presence_of_element_located(
                (By.XPATH, "//html[@id='login-page']")
            ))
            self.driver.switch_to.default_content()
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
