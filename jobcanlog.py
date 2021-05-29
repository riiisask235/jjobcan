from selenium import webdriver
from time import sleep
import datetime
import requests
from bs4 import BeautifulSoup
import re
import pandas
#ActionChainsを使う時は、下記のようにActionChainsのクラスをロードする
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import settings

LOGIN_ID = settings.ID
PASSWORD = settings.PWD

class JobCan:
    def __init__(self):
        self.driver = webdriver.Chrome('C:\work\chromedriver_win32\chromedriver')

#変数error_flgはエラーの判定に使うフラグ。最初はFalseを設定しておく
#そして途中でエラーが発生した場合はTrueを設定して、以降の処理をスキップする判定に使用
    def open_url(self,url):
        self.driver.get(url)

    def login(self,id,pwd):
        error_flg = False
        if error_flg is False:
            try:
                loginid_input = self.driver.find_element_by_xpath('//input[@id="client_manager_login_id"]')
                loginid_input.send_keys(id)
#xpathhtml,xml形式の文書から特定の部分を指定して取得するための簡易言語
                password_input = self.driver.find_element_by_xpath('//input[@id="client_login_password"]')
                password_input.send_keys(pwd)
                self.driver.find_element_by_xpath('//*[@class="btn btn-info btn-block"]').click()
            except Exception:
                print('ユーザー名、パスワード入力時にエラーが発生しました。')
                error_flg = True

    def select_shift_page(self):
        self.driver.find_element_by_xpath('//*[@class="menuCenter"]').click()
        self.driver.find_element_by_link_text('シフト予定表').click()

    def select_line_shift(self):
#ラインシフト表示
        dropdown = self.driver.find_element_by_id("type-combo")
        select_dropdown = Select(dropdown)
        select_dropdown.select_by_value("day2")

    def select_calender(self):
#表示する日程(今日)を選択
        today = datetime.date.today()
        year = today.year
        month = today.month
        day = today.day
#ドロップダウンで今日の日時を選択（send_keysを使う）
        dropdown2 = self.driver.find_element_by_name("from[day2][y]")
        dropdown2.send_keys(year)
        select_dropdown2 = Select(dropdown2)
#select_dropdown2.select_by_value("2021")
        dropdown3 = self.driver.find_element_by_name("from[day2][m]")
        dropdown3.send_keys(month)
        select_dropdown3 = Select(dropdown3)
#select_dropdown3.select_by_value("4")
        dropdown4 = self.driver.find_element_by_name("from[day2][d]")
        dropdown4.send_keys(day)
        select_dropdown4 = Select(dropdown4)
#select_dropdown4.select_by_value("22")
#表示のボタンを押す
        self.driver.find_element_by_xpath('//*[@class="btn btn-info"]').click()

    def save_screenshot(self):
# 下までスクロール
        el_html = self.driver.find_element_by_tag_name('html')
        for i in range(5):
            el_html.send_keys(Keys.PAGE_DOWN)

        w = self.driver.execute_script("return document.body.scrollWidth;")
        h = self.driver.execute_script("return document.body.scrollHeight;")
# set window size
        self.driver.set_window_size(w,h)
#スクショを取る
        self.driver.save_screenshot("FILENAME.jpg")

    def get_shift_list(self):
#driver.page_sourceで今開いてるページのソースを取得できる
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

#シフトテーブルを選択。tableタグが他にもあるので配列から特定
        shift_list = soup.find_all ("table")[5]
#find_allで<tr>タグを全部とる(リストで返ってくる)
# #<tr>～</tr>で1個の文字列
        member_list = shift_list.find_all ("tr")[2:]
# #出力内容から改善策を考えた
# #空リストをつくる
        result = []
# #member_listをfor文で回す
# #for文はリスト型データを回すのに役立つ(長さが限定的、決まっている)
# #while文は長さが不確定のモノ(無限ループ)
        for member in member_list:
# #<td>はテーブルの1マス1マスを示す
            coloms = member.find_all("td")
            for i in range(2):
                result.append(coloms[i])
# #空リストをつくる
        tame = ""
        for j in result:
            kame = j.get_text()
            tame+=kame+ "\n"
        print(tame+"本日も１日頑張りましょう(´▽｀*)")
#処理が終わったらwindowを閉じる
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    driver = JobCan()
    driver.open_url('http://jobcan.jp/login/client/?client_login_id=all-SHIRUCAFE')
    driver.login(LOGIN_ID, PASSWORD)
    driver.select_shift_page()
    driver.select_line_shift()
    driver.select_calender()
    driver.save_screenshot()
    driver.get_shift_list()