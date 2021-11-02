from copy import deepcopy
from datetime import datetime
from time import sleep

from pyquery import PyQuery as Pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as Wait

import app
from app.remote.errorhandler import log, err_catch, log_driver, headless_web


class MainScript(object):
    def __init__(self, rekening='ss_test'):
        self._url = 'https://ibank.klikbca.com'
        self.profile = 'Chrome_bcaibank'
        self.rekening = rekening
        self.is_login = False
        self.driver = None
        self.count_login = 0
        self.start = False

    def __ss(self, funct_name):
        result = False
        try:
            if self.driver is not None:
                result = self.driver.save_screenshot('ss/ibankbca/{}-{}.png'.format(self.rekening, funct_name))
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
            if not self.start:
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
            if self.count_login > 50:
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
            self.count_login = 0
            self.start = True
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
            self.driver.switch_to.default_content()
            Wait(self.driver, 10).until(condition.presence_of_element_located(
                (By.NAME, 'menu')
            ))
            frame_menu = self.driver.find_element(By.NAME, 'menu')
            self.driver.switch_to.frame(frame_menu)
            Wait(self.driver, 2).until(condition.element_to_be_clickable(
                (By.LINK_TEXT, 'Informasi Rekening')
            )).click()
            Wait(self.driver, 1).until(condition.element_to_be_clickable(
                (By.LINK_TEXT, 'Mutasi Rekening')
            )).click()
            self.driver.switch_to.default_content()
            frame_mutasi = self.driver.find_element(By.NAME, 'atm')
            self.driver.switch_to.frame(frame_mutasi)
            el_select = Select(self.driver.find_element(By.ID, 'D1'))
            el_select.select_by_visible_text(rekening)
            self.driver.find_element(By.ID, 'r1').click()
            start_split = from_date.split('/')
            end_split = to_date.split('/')
            Select(self.driver.find_element(By.ID, 'startDt')).select_by_value('%02d' % int(start_split[0]))
            Select(self.driver.find_element(By.ID, 'startMt')).select_by_value('%01d' % int(start_split[1]))
            Select(self.driver.find_element(By.ID, 'startYr')).select_by_value(start_split[2])
            Select(self.driver.find_element(By.ID, 'endDt')).select_by_value('%02d' % int(end_split[0]))
            Select(self.driver.find_element(By.ID, 'endMt')).select_by_value('%01d' % int(end_split[1]))
            Select(self.driver.find_element(By.ID, 'endYr')).select_by_value(end_split[2])
            self.driver.find_element(By.XPATH, "//input[@name='value(submit1)']").click()
            # want_save = self.driver.find_elements_by_tag_name('table')[4].find_elements_by_tag_name('tr')
            # sleep(3);
            # Save buat test scrap file html (lihat di main routes.py)
            # save_file('ss/ibankbca/{}-mutasi.html'.format(rekening), self.driver.page_source)
            # copy dari main routes.py /testscrap
            table_ = Pq(self.driver.page_source)('table')[4]
            div_tr = Pq(table_)('tr')
            i = 0
            for row in div_tr:
                i += 1
                if i == 1:
                    continue
                log.info('Ambil baris: ' + str(i))
                kolom = {}
                mutasi = Pq(row)('td')
                kolom['tanggal'] = Pq(mutasi[0]).text()
                kolom['keterangan'] = Pq(mutasi[1]).text()
                kolom['code'] = Pq(mutasi[2]).text()
                kolom['debet'] = ''
                kolom['kredit'] = ''
                db_cr = Pq(mutasi[4]).text()
                if db_cr == 'CR':
                    kolom['kredit'] = Pq(mutasi[3]).text()
                else:
                    kolom['debet'] = Pq(mutasi[3]).text()
                kolom['saldo'] = Pq(mutasi[5]).text()
                result.append(deepcopy(kolom))
        except Exception as e:
            log.error(err_catch(e))
        finally:
            self.__ss('ambil_mutasi')
        return result

    def login(self, company, username, password):
        try:
            log.info('Mencoba Login')
            self.count_login += 1
            Wait(self.driver, 15).until(condition.element_to_be_clickable(
                (By.NAME, 'value(Submit)')
            ))
            sleep(0.8)  # ada bug bila terlalu cepat
            self.driver.find_element(By.ID, 'user_id').send_keys(username)
            self.driver.find_element(By.ID, 'pswd').send_keys(password)
            self.driver.find_element(By.NAME, 'value(Submit)').click()
            Wait(self.driver, 20).until(condition.presence_of_element_located(
                (By.NAME, 'header')
            ))
            frame_header = self.driver.find_element(By.NAME, 'header')
            self.driver.switch_to.frame(frame_header)
            Wait(self.driver, 10).until(condition.presence_of_element_located(
                (By.LINK_TEXT, '[ LOGOUT ]')
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
            self.driver.switch_to.default_content()
            Wait(self.driver, 10).until(condition.presence_of_element_located(
                (By.NAME, 'header')
            ))
            frame_header = self.driver.find_element(By.NAME, 'header')
            self.driver.switch_to.frame(frame_header)
            Wait(self.driver, 5).until(condition.element_to_be_clickable(
                (By.LINK_TEXT, '[ LOGOUT ]')
            )).click()
            # Tunggu sampai benar-benar keluar
            Wait(self.driver, 5).until(condition.element_to_be_clickable(
                (By.ID, 'user_id')
            ))
            self.is_login = False
        except (AttributeError, Exception) as e:
            log.error(err_catch(e))
        finally:
            self.__ss('logout')

    def close_popup(self):
        try:
            log.info('Close Popup')
            raise Exception('Dalam development')
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
            self.start = False
            self.count_login = 0
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


def month_to_indo(num_str):
    month = 'Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember'
    int_ = int(num_str) - 1
    return month.split('|')[int_]
