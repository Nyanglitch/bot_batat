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
	local_prefix = prefix + "DDL_"
	select = Select(driver.find_element_by_id(local_prefix + ident))
	select.select_by_index(value - 1)

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
lookup("txtFam", info[0]) # last name
lookup("txtIm", info[1]) # first name
lookup("txtTel", info[2]) # phone
lookup("txtEmail", info[3]) # email

selectup("Day", int(info[4]))
selectup("Month", int(info[5]))
lookup("TextBox_Year", int(info[6]))

time.sleep(10) # pause to fill in the captcha

clickity("ButtonA")

# next page: clicking the link
driver.find_element_by_link_text("Загранпаспорт").click()

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