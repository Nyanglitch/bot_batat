"""
Bot Batat
Automates most of the pain of filling out the forms
for the Washington consulate queue website for a very specific question.
Unfortunately full potential of automated sign-up
is impossible at the moment due to captcha restriction.
Unless there's a way to bypass the captcha, of course.

HOW IT WORKS:
1. Reads the "batat-input.txt" file for info to put in the form.
2. Fills it out and leaves 10 seconds for you to fill in the captcha.
3. Voila?
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

# initializing the driver
driver = webdriver.Firefox()

# getting the page
driver.get("http://washington.kdmid.ru/queue/visitor.aspx")

# prefix for common tag names
prefix = "ctl00_MainContent_"
prefix_sel = prefix + "DDL_"

# looking for elements
def lookup(ident, content):
	"""
	Looks up elements of the form by id and
	sends specified content to it.
	"""
	elem = driver.find_element_by_id(prefix + ident)
	elem.clear()
	elem.send_keys(content)

def selectup(ident, value):
	"""
	Looks up select elements by id and
	selects a specified value.
	"""
	select = Select(driver.find_element_by_id(prefix_sel + ident))
	select.select_by_index(int(value) - 1)

def clickity(ident):
	"""
	Clicks and ticks the stuff.
	"""
	driver.find_element_by_id(prefix + ident).click()
 
# reading and cleaning the input file
info = []
with open("batat-input.txt", 'r') as f:
	info = f.readlines()
	info = [i.strip() for i in info]

# filling out the form
site_selectors = ["txtFam", "txtIm", "txtTel", 
	"txtEmail", "Day", "Month", "TextBox_Year"] 

for index, selector in enumerate(site_selectors):
	if index not in [4, 5]:
		lookup(selector, info[index])
	else:
		selectup(selector, info[index])

time.sleep(10) # pause to fill in the captcha

clickity("ButtonA")

# next page: clicking the link
def zagran_click():
	driver.find_element_by_link_text("Загранпаспорт").click()

try:
	zagran_click()
except NoSuchElementException:
	time.sleep(5)
	zagran_click()

# next page: tick checkbox, follow link
clickity("CheckBoxList1_0")
clickity("ButtonQueue")

# next page: extracting info
# time.sleep(20)

# closest_date = driver.find_element_by_xpath(
# 	"//table[@id='ctl00_MainContent_RadioButtonList1']/tbody/tr/td[1]/label"
# 	).text
# print(closest_date)

# driver.close()

"""
After the script finished it's work,
you just look at what's available.
Yeah, not very exciting.
But hey, it automates at least something!
"""