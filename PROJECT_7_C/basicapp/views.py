from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from django.urls import path
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys

# Create your views here.

def search_form(request):
    #driver_open()
    return render(request, 'basicapp/index.html')
def search(request):
    #if 'q' in request.GET:
    search_iteam=request.GET['q']
    #help_dict={"scrap_amazon":d[amazon],"srap_flipkart":d[flipkart]}
    driver = webdriver.PhantomJS(executable_path=r"phantomjs.exe")
    flipkart_data_list=list()
    url='https://www.flipkart.com/account/login?ret=%2Faccount%2Forders%3Flink%3Dhome_orders&fromMyOrdersPage=true'
    driver.get(url)
    time.sleep(4)
    #//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input
    serach_box=driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input')
    serach_box.send_keys(search_iteam)
    #Keys.ENTER
    serach_box.send_keys(Keys.ENTER)
    time.sleep(1)
    soup=BeautifulSoup(driver.page_source,'lxml')
    #print(soup)
    div_tag1=soup.find_all('div',class_='_1HmYoV _35HD7C')
    #print(div_tag1[1])
    #_3liAhj _1R0K0g
    time.sleep(1)

    div_tag2=div_tag1[1].find_all('div',class_='_3liAhj _1R0K0g')#horizontal

    #print(div_tag2)
    if div_tag2==[]:
    	div_tag2=div_tag1[1].find_all('div',class_='_1UoZlX')
    #print(div_tag2)

    #_31qSD5
    for div_tag in div_tag2[0:1]:
        a_tag=div_tag.find('a',class_="_2cLu-l")
        if a_tag==None:
        	a_tag=div_tag.find('a',class_="_31qSD5")
        a_tag_link=a_tag['href']

        #print(url1)
        driver.get(url+a_tag_link)
        soup=BeautifulSoup(driver.page_source,'lxml')
        div_tag1=soup.find('div',class_='_1HmYoV _35HD7C col-8-12')
        span_tag=div_tag1.find('span',class_='_35KyD6')
        print(span_tag.text)
        flipkart_data_list.append("PRODUCT NAME"+" "+span_tag.text)
        #_1vC4OE _3qQ9m1
        price=div_tag1.find('div',class_='_1vC4OE _3qQ9m1')
        #print('PRODUCT PRICE',price.text)
        product_price="PRODUCT PRICE "+" "+price.text
        flipkart_data_list.append(product_price)
    #_3WHvuP
        product_details=div_tag1.find('div',class_='_3WHvuP')
        p1=product_details.find_all('li',class_='_2-riNZ')
        for i in p1:
        	#print(i.text)
        	t_ext=i.text
        	flipkart_data_list.append(t_ext)
    driver.quit()
    print("------------------------------------------------------------")
    driver_AMAZON= webdriver.PhantomJS(executable_path=r"phantomjs.exe")
    url_AMAZON="https://www.amazon.in"
    driver_AMAZON.get(url_AMAZON)
    #key_pass="Mi LED TV 4C PRO 80 cm (32) HD Ready Android TV (Black)"
    search_box_AMAZON=driver_AMAZON.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
    search_box_AMAZON.send_keys(search_iteam)
    search_box_AMAZON.send_keys(Keys.ENTER)
    #search_click_AMAZON=driver_AMAZON.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input')
    #search_click_AMAZON.click()
    amazon_data_list=list()
    time.sleep(2)
    soup_AMAZON_home=BeautifulSoup(driver_AMAZON.page_source,'lxml')
    #print(soup_AMAZON_home)
    ul_tags=soup_AMAZON_home.find('ul',{"id":"s-results-list-atf"})
    div_tags=ul_tags.find_all('div',class_='s-item-container')
    #print(div_tags)
    if div_tags==[]:
    	div_tags=ul_tags.find_all('div',class_='a-fixed-left-grid-col a-col-right')#for_verticle_pages
    	#s-item-container

    #print(div_tags)
    for div_tag in div_tags[0:1]:
    	div_tag2=div_tag.find("div",class_='a-row a-spacing-small')
    	#print(div_tag2)
    	a_tag=div_tag2.find("a",class_="a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal")
    	#print(a_tag)
    	if a_tag==None:
    		#a-link-normal a-text-normal
    		a_tag=div_tag2.find("a",class_="a-link-normal a-text-normal")
    	#print(a_tag)
    	sub_link=a_tag['href']
    	#print(sub_link)
    	try:
    		#driver_AMAZON2 = webdriver.Chrome(executable_path=r"C:\chrome driver\chromedriver.exe")
    		driver_AMAZON.get(sub_link)
    	except:
    		continue
    	soup_AMAZON_subpage=BeautifulSoup(driver_AMAZON.page_source,'lxml')
    	#print(soup_AMAZON_subpage.prettify)
    	div_tag_sub=soup_AMAZON_subpage.find("div",class_='a-container')
    	#print(div_tag_sub)
    	#a-size-medium a-color-price
    	product_title_tag=div_tag_sub.find("span",class_="a-size-large")
    	#print("PRODUCT NAME",product_title_tag.text.strip())
    	amazon_data_list.append("PRODUCT NAME"+" "+product_title_tag.text.strip())
    	try:
    		product_prise_tag=div_tag_sub.find("span",class_="a-size-medium a-color-price")
    		#print("PRICE",product_prise_tag.text.strip())
    		price_amzon="PRODUCT PRICE"+" "+product_prise_tag.text.strip()
    		amazon_data_list.append(price_amzon)
    	except:
    		pass



    	try:
    		product_feature_tag=div_tag_sub.find("div",{'id':'feature-bullets'})
    		list_feature_contents=product_feature_tag.find_all("li")
    		for list_feature_content in list_feature_contents[:]:
    			#print(list_feature_content.text.strip())
    			amazon_data_list.append(list_feature_content.text.strip())
    	except:
    		pass



    	try:
    		product_content_tag=div_tag_sub.find("div",{'id':'detail_bullets_id'})
    		list_tag_contents=product_content_tag.find_all("li")
    		for list_tag_content in list_tag_contents[:5]:
    			#print(list_tag_content.text.strip())
    			amazon_data_list.append(list_tag_content.text.strip())
    	except:
    		pass


    driver_AMAZON.quit()
    return render(request,'basicapp/index2.html',{
                                    "amazon_data":amazon_data_list,
                                    "flipkart_data":flipkart_data_list})
