from selenium import webdriver
import telegram
import commend
import background
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# start = time.time()

# 디버그 크롬에서 실행
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome("크롬 드라이버 경로")

# 크롬 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

# 속도 향상을 위한 옵션 해제
prefs = {
    'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2, 'geolocation': 2,
                                               'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                               'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                               'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                                               'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                               'push_messaging': 2, 'ssl_cert_decisions': 2,
                                               'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                               'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}

options.add_experimental_option('prefs', prefs)

# 인스타그램

"""
# 자동로그인

driver = webdriver.Chrome()
url = "https://www.instagram.com/accounts/activity/"
driver.get(url)
driver.maximize_window()
action = ActionChains(driver)

id = '********'
pw = '********'

driver.find_element_by_name('username').send_keys(id)
driver.find_element_by_name('password').send_keys(pw)
login1 = driver.find_element_by_css_selector("button.sqdOP.L3NKy.y3zKF")
login1.click()

driver.implicitly_wait(10)

login2 = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
login2.click()

"""

driver.get("https://www.instagram.com/accounts/activity/")
driver.implicitly_wait(30)
lit = driver.find_elements_by_class_name('YFq-A')
aaa = driver.find_elements_by_tag_name('.YFq-A a')
bbb = driver.find_elements_by_tag_name('.iTMfC a')

text = []  # 텍스트
prof = []  # username
link = []  # 프로필 링크
post = []  # 영상 링크

for tag in lit:
    text.append(tag.text)  # 텍스트

for tag in aaa:
    link.append(tag.get_attribute('href'))  # 프로필 링크
    prof.append(tag.get_attribute('title'))  # username

for tag in bbb:
    post.append(tag.get_attribute('href'))  # 영상 링크

# 딕셔너리 변환
dic1 = {name: value for name, value in zip(text[:10], post[:10])}
dic2 = {name: value for name, value in zip(prof[:10], link[:10])}

# 유튜브

"""
# 자동 로그인
driver = webdriver.Chrome()
url = "https://www.tensorflow.org/_d/signin?continue=https%3A%2F%2Fwww.tensorflow.org%2F%3Fhl%3Dko&prompt=select_account"
driver.get(url)
driver.maximize_window()
action = ActionChains(driver)

# id = '******'
# pw = '**********'

driver.find_element_by_id('identifierId').send_keys('아이디')
driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
time.sleep(3)
driver.find_element_by_css_selector('.whsOnd.zHQkBf').send_keys('비번')
driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
"""

driver.get("https://www.youtube.com")

driver.implicitly_wait(30)

driver.find_element_by_css_selector('.style-scope.ytd-notification-topbar-button-renderer').click()
lit = driver.find_elements_by_css_selector('.message.style-scope.ytd-notification-renderer')
aaa = driver.find_elements_by_tag_name('.style-scope.yt-multi-page-menu-section-renderer a')

text_y = []  # 텍스트
link_y = []  # 영상 링크

for tag in lit:
    text_y.append(tag.text)  # 텍스트

for tag in aaa:
    link_y.append(tag.get_attribute('href'))  # 영상 링크

driver.close()  # 창 닫기

# 딕셔너리 변환
dic3 = {name: value for name, value in zip(text_y[:5], link_y[:5])}

# 토큰, 아이디
token = '토큰'
bot = telegram.Bot(token=token)

# 텔레그램으로 전송
bot.sendMessage(chat_id='아이디', text="인스타그램")
for key, value in dic1.items():
    bot.sendMessage(chat_id='아이디', text=key)
    bot.sendMessage(chat_id='아이디', text=value)

bot.sendMessage(chat_id='아이디', text="유튜브")
for key, value in dic3.items():
    bot.sendMessage(chat_id='아이디', text=key)
    bot.sendMessage(chat_id='아이디', text=value)

# print("time :", time.time() - start)