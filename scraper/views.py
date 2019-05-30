from django.shortcuts import render

from selenium import webdriver
from time import sleep
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.firefox.options import Options


def selenium_scrap(search_term):
	s_results = []
	options = Options()
	options.set_headless(True)

	#search_term = input('Enter search term you need\n')


	driver = webdriver.Firefox(options=options)

	url = 'https://www.google.com/maps/'

	driver.get(url)
	sleep(2)


	inp_field = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
	inp_field.send_keys(search_term)
	sleep(2)
	search_butt = driver.find_element_by_xpath('//*[@id="searchbox-searchbutton"]')
	search_butt.click()
	sleep(2)

	num = 0
	info = 'No Info'

	while True:
		search_results = driver.find_elements_by_class_name('section-result-text-content')
		print(f"Found {len(search_results)}")
		try:
			search_results[num].click()
			num += 1
			sleep(2)
			# nadji informacije
			try:
				name = driver.find_element_by_tag_name('h1').text
			except NoSuchElementException:
				sleep(2)
				name = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[7]/div[9]/div/div[1]/div/div/div[2]/div[3]/div[1]/h1').text
			print(name)
			try:
				rating = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[7]/div[9]/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div[1]/span[1]/span/span').text
			except NoSuchElementException:
				rating = 'Nema rejting'
			try:
				num_rating = driver.find_element_by_xpath('/html/body/jsl/div[3]/div[7]/div[9]/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div[1]/span[3]/ul/li/span[2]/span[1]/button').text
			except NoSuchElementException:
				num_rating = 0
			print(f"Rating: {rating}, number of rates: {num_rating}")
			try:
				address, plus_code, website, tel, *args = driver.find_elements_by_xpath('/html/body/jsl/div[3]/div[7]/div[9]/div/div[1]/div/div/div[*]/div/div[1]/span[3]/span[3]')
				print(f"Adresa: {address.text}")
				print(f"Website: {website.text}")
				print(f"Telefon: {tel.text}")
				s_results.append([name, rating, num_rating, address.text, plus_code.text, website.text, tel.text])
			except ValueError:
				info = driver.find_elements_by_xpath('/html/body/jsl/div[3]/div[7]/div[9]/div/div[1]/div/div/div[*]/div/div[1]/span[3]/span[3]')
				print([i for i in info])
			sleep(5)
			# NAZAD NA REZULTATE
			back_butt = driver.find_element_by_class_name('section-back-to-list-button.blue-link.noprint').click()
			sleep(4)
			# UVEK POSLE POVRATKA PONOVO SKENIRAJ REZULTATE
			search_results = driver.find_elements_by_class_name('section-result-text-content')
			sleep(2)

			
		except IndexError:
			print("Going to next page ===>")
			try:
				next_page = driver.find_element_by_xpath('//*[@id="n7lv7yjyC35__section-pagination-button-next"]').click()
				num = 0
				sleep(5)
			except ElementClickInterceptedException as e:
				print(e)
				break

	# go to next page for results
	#next_page = driver.find_element_by_xpath('//*[@id="n7lv7yjyC35__section-pagination-button-next"]').click()

	sleep(2)
	driver.close()
	return s_results

# Create your views here.
def scraper(request):
	return render(request, 'scraper.html')

def scraping_results(request):
	fulltext = request.GET['fulltext']
	RESULTS = selenium_scrap(fulltext)
	return render(request, 'scraping_results.html', {"fulltext": fulltext, 'rezultat': RESULTS})