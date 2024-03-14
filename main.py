import time
import pandas as pd
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

time_control = 1

# Первая часть задания: извлечение .csv файла

options = webdriver.ChromeOptions()
options.add_argument('start-maximized')

options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

# Запускаем веб-драйвер
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=['en-US', 'en'],
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor='Intel Inc.',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True,
        )

# Открываем веб-страницу
driver.get('https://www.nseindia.com')

time.sleep(time_control)

# Находим элемент, на который нужно навести
element_to_hover_over = driver.find_element(By.ID, 'link_2')

time.sleep(time_control)

# Находим элемент, который нужно нажать
element_to_click = driver.find_element(By.XPATH, "//*[text()='Pre-Open Market']")

# Создаем объект ActionChains
action = ActionChains(driver)

# Наводим курсор на элемент
action.move_to_element(element_to_hover_over).perform()

# Ждем некоторое время, чтобы увидеть эффект наведения
driver.implicitly_wait(time_control)

# Нажимаем на другой элемент
element_to_click.click()

# Ждем некоторое время
driver.implicitly_wait(time_control)

# Найдите таблицу на странице
table = driver.find_element(By.XPATH, "//table[@id='livePreTable']")

# Извлекаем заголовки таблицы
headers = [header.text for header in table.find_elements(By.XPATH,".//th")]

# Извлекаем строки таблицы
rows = []
for row in table.find_elements(By.XPATH,".//tr"):
    row_data = [cell.text for cell in row.find_elements(By.XPATH,".//td")]
    if row_data:  # Исключаем пустые строки
        rows.append(row_data)

# Создаем DataFrame из данных
df = pd.DataFrame(rows, columns=headers)

# Сохраняем DataFrame в CSV файл
df[['SYMBOL', 'FINAL']].to_csv('./output.csv', index=False)

# Вторая часть: имитация последующих действий

time.sleep(time_control)

# Создаем элемент для нажатия кнопки "Домой" 
home = driver.find_element(By.ID, 'link_0')
home.click()

time.sleep(time_control)

# Создаем элемент, до которого будем пролистывать страницу
element_to_scroll = driver.find_element(By.ID, 'home-top5stock' )
# Пролистываем страницу до этого элемента
driver.execute_script("arguments[0].scrollIntoView();", element_to_scroll)

time.sleep(time_control)

# Создаем элемент, для перехода на страницу таблицы
view_all_to_click = driver.find_element(By.XPATH, "//*[@id='gainers_loosers']/div[3]/a")
view_all_to_click.click()

time.sleep(time_control)

# Создаем элемент для оперирования селектором
selector = driver.find_element(By.ID, 'equitieStockSelect')
selector.click()

time.sleep(time_control)

# Создаем элемент для перевыбора элемента в селекторе
nifty_next_50_to_click = driver.find_element(By.XPATH, '//*[@id="equitieStockSelect"]/optgroup[1]/option[2]')
nifty_next_50_to_click.click()

time.sleep(time_control)

# Прокручиваем на 1000 пикселей вниз
driver.execute_script("window.scrollBy(0, 1000)")

time.sleep(time_control)

# Закрываем браузер
driver.quit()