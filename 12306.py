from time import sleep
import time
from  datetime import  datetime as dt
from selenium import webdriver
import requests
import re
import zmail

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

class MyMail(object):
    def mail_success(self,price,path):
        self.username = "WyuuServer@163.com"
        self.authorization_code = 'UDFD******NAM'
        self.server = zmail.server(self.username, self.authorization_code)
        mail_body = {
            'subject': '抢票结果',
            'content_text': f'您好，抢票成功，价格为{price},请在十分钟内完成支付，否则系统将自动释放车票,以下是最终截图',  # 纯文本或者HTML内容
            'attachments': [path]
        }
        mail_to = "2644489337@qq.com"
        self.server.send_mail(mail_to, mail_body)
        print(f"请在十分钟内支付，价格为{price}，详细信息已发送邮件至",mail_to)

    def mail_fail(self,path):
        self.username = "WyuuServer@163.com"
        self.authorization_code = 'UDFD******NAM'
        self.server = zmail.server(self.username, self.authorization_code)
        mail_body = {
            'subject': '抢票异常',
            'content_text': f'您好，抢票出现异常，请及时查看，以下是最后的截图',
            # 纯文本或者HTML内容
            'attachments': [path]
        }
        mail_to = "2644489337@qq.com"
        self.server.send_mail(mail_to, mail_body)
        print("已将异常结果发送到", mail_to)

def url_isok(url):
    status_code=requests.get(url).status_code
    if status_code==200:
        print('12306官网访问成功!')
    else:
        exit('访问12306时出错，请检查网络')

def get_location():
    dep=input('请输入出发城市')
    des=input('请输入目的城市')
    is_stu=input('是否购买学生票?')
    dic={'dep':dep,'des':des,'is_stu':is_stu}
    return dic

def date_chose():
    current_date = datetime.now()
    date_list = []
    for i in range(15):
        date = current_date + timedelta(days=i)
        formatted_date = date.strftime('%m月%d日')
        date_list.append(f"{i + 1}、{formatted_date}")
        print('请选择您要购票的日期:')
    for date_entry in date_list:
        print(date_entry)
    day_go=int(input('请输入日期前的序号:'))
    if day_go>15|day_go<1 :
        exit('输入的序号不正确！')
    else:
        return day_go


if __name__ =='__main__':

    bro=webdriver.Edge()
    bro.get('https://www.12306.cn/')
    url_isok(bro.current_url)
    login_bt=bro.find_element('xpath','//*[@id="J-btn-login"]').click()
    login_QR_bt=bro.find_element('xpath','//*[@id="toolbar_Div"]/div[2]/div[2]/ul/li[2]/a').click()
    print('请在30秒内扫码登录')
    wait = WebDriverWait(bro, 30)
    try:
        # 使用显式等待等待个人信息页面出现
        personal_center = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="gerenzhongxin"]/h2')))
        #sleep(3)
        user_name=bro.find_element('xpath','//*[@id="js-minHeight"]/div[1]/div[1]/strong').text
        print(f'登录成功，欢迎您,{user_name}!')
        Ac=ActionChains(bro)
        train_ticket=bro.find_element('xpath','//*[@id="J-chepiao"]/a')
        Ac.move_to_element(train_ticket).perform()
        train_single_ticket=wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="megamenu-3"]/div[1]/ul/li[1]/a')))#bro.find_element('xpath','//*[@id="megamenu-3"]/div[1]/ul/li[1]/a')
        Ac.move_to_element(train_single_ticket).click().perform()
        print('已进入抢票页面,请设置相关信息')
        wait = WebDriverWait(bro, 120)
        key = input('设置好站点后输入任意值开始抢票')
        start_time = dt.now()
        #print(start_time)

        table_row=bro.find_elements('xpath','//*[@id="queryLeftTable"]/tr[contains(@id, "ticket_")]')
        len=len(table_row)
        print (f"获取到火车票{len}张！")
        loop_key=1
        start_time_2 = dt.now()
        bro.find_element('xpath', '//*[@id="date_range"]/ul/li[14]').click()
        print('抢票中...')
        while(loop_key):
            #wait.until( EC.element_to_be_clickable((By.XPATH, f'/html/body/div[3]/div[7]/div[9]/table/tbody/tr[{2*len-1}]/td[13]/a')))
            wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/div[7]/div[9]/table/tbody/tr[{2*len-1}]/td[13]')))
            bro.find_element('xpath','//*[@id="date_range"]/ul/li[14]').click()
            for count in range(0,len):
                try:
                    key=2*count+1
                    bro.find_element('xpath',f'/html/body/div[3]/div[7]/div[9]/table/tbody/tr[{key}]/td[13]/a')
                    # print('ok')
                    start_time=int(re.split(":",bro.find_element('xpath',f'/html/body/div[3]/div[7]/div[9]/table/tbody/tr[{key}]/td[1]/div/div[3]/strong[@class="start-t"]').text)[0])
                    # print(start_time)
                    if start_time>=9 and start_time<=11:
                        print(bro.find_element('xpath',f'/html/body/div[3]/div[7]/div[9]/table/tbody/tr[{key}]/td[4]').text,type(bro.find_element('xpath',f'/html/body/div[3]/div[7]/div[9]/table/tbody/tr[{key}]/td[4]').text))
                        if bro.find_element('xpath',f'/html/body/div[3]/div[7]/div[9]/table/tbody/tr[{key}]/td[4]').text!='候补':
                            bro.find_element('xpath',f'/html/body/div[3]/div[7]/div[9]/table/tbody/tr[{key}]/td[@class="no-br"]/a').click()
                            loop_key=0
                            break
                        else:
                            #print('车座无')
                            continue

                    else:
                        #print('时间不符')
                        continue
                except NoSuchElementException:
                    #print('卖完了')
                    continue
        print('抢票成功')
        wait = WebDriverWait(bro, 20)
        end_time=dt.now()
        #print(end_time)
        diff=(end_time-start_time_2).total_seconds()
        print('阶段一耗时',diff)
        #input('sb')
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="normalPassenger_0"]')))
        bro.find_element('xpath','//*[@id="normalPassenger_0"]').click()
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '  // *[ @ id = "dialog_xsertcj_cancel"]')))
        bro.find_element('xpath','  // *[ @ id = "dialog_xsertcj_cancel"]').click()
        bro.find_element('xpath','//*[@id="submitOrder_id"]').click()
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '  //*[@id="qr_submit_id"]')))
        print('已找到提交按钮')
        # sleep(3)
        # qr = bro.find_element(By.XPATH, '//*[@id="qr_submit_id"]')
        qr = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a#qr_submit_id.btn92s')))
        #qr=wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[6]/div/div[5]/div[1]/div/div[2]/div[2]/div[8]/a[3]')))
        bro.execute_script("arguments[0].click();", qr)
        end_time_2=dt.now()
        diff_2=(end_time_2-start_time_2).total_seconds()
        print('全阶段耗时',diff_2)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '  //*[@id="total_ticket_price"]')))
        price=bro.find_element('xpath',' //*[@id="total_ticket_price"]').text
        bro.get_screenshot_as_file('抢票成功.png')
        path = 'F:/work/Pycharm/PyCharm 2023.2/Porjects/venv/12306测试/抢票成功.png'
        Mail = MyMail()
        Mail.mail_success(price,path)
        input('输入任意数值退出（请确保已经完成支付！)')

    except TimeoutException:
        bro.get_screenshot_as_file('异常.png')
        path_e = 'F:/work/Pycharm/PyCharm 2023.2/Porjects/venv/12306测试/异常.png'
        Mail = MyMail()
        Mail.mail_fail(path_e)
        exit('程序超时')

    finally:
        bro.close()
        print('程序结束，感谢使用！')

