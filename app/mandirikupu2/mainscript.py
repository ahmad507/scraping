from copy import deepcopy
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
        self._url = 'https://ibank.bankmandiri.co.id/retail3/'
        self.rekening = rekening
        self.is_login = False
        self.driver = None

    def __ss(self, funct_name):
        result = False
        try:
            if self.driver is not None:
                result = self.driver.save_screenshot('ss/mandirikupu2/{}-{}.png'.format(self.rekening, funct_name))
        except Exception as e:
            log.error('Gagal capture!!!')
            log.error(str(e.args) + ', ' + str(result))

    def autorun(self, company, username, password, rekening=None, from_date=None, to_date=None):
        """autorun get mutasi"""
        result = []
        if rekening is not None:
            self.rekening = rekening
        """ from_date to_date tidak diperlukan"""
        # if from_date is None:
        #     from_date = datetime.now().strftime('%d/%m/%Y')
        # if to_date is None:
        #     to_date = from_date
        try:
            log.info('MULAI')
            self.start_driver()
            # self.close_popup()  # bila ada popup
            # self.ganti_bahasa()
            self.login(company, username, password)
            result = self.ambil_mutasi(rekening=self.rekening, from_date=from_date, to_date=to_date)
            self.logout()
        except Exception as e:
            self.__ss('autorun-error')
            log.error(err_catch(e))
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
            raise Exception('Dalam development')
        except Exception as e:
            log.error(err_catch(e))
            raise Exception(e)  # Stop bila gagal
        finally:
            self.__ss('ganti_bahasa')

    # noinspection PyUnusedLocal
    def ambil_mutasi(self, rekening=None, from_date=None, to_date=None):
        result = []
        try:
            log.info('Ambil Mutasi')
            raise Exception('Dalam development')
            # sleep(3);save_file(self.driver.page_source)  # Save buat test scrap file html (lihat di main routes.py)
            # copy dari main routes.py /testscrap
            table_ = Pq(self.driver.page_source)('.table-div')
            body_ = Pq(table_)('.tbody .clearfix')
            div_tr = Pq(body_)('.tr')
            i = 1
            for row in div_tr:
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
                i += 1
        except Exception as e:
            log.error(err_catch(e))
        finally:
            self.__ss('ambil_mutasi')
        return result

    def login(self, company, username, password):
        try:
            log.info('Mencoba Login')
            raise Exception('Dalam development')
            self.is_login = True
        except Exception as e:
            log.error(err_catch(e))
            raise Exception(e)  # Stop bila tidak bisa login
        finally:
            self.__ss('login')
            if self.is_login:
                log.info('Di dalam Login')
            else:
                log.info('Login Gagal')

    def logout(self):
        try:
            log.info('Logout')
            raise Exception('Dalam development')
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


def save_file(source):
    f = None
    try:
        f = open('mutasimanpribadi.html', 'w')
        f.write(repr(source))
    except Exception as e:
        log.error(e.args)
    finally:
        f.close()
