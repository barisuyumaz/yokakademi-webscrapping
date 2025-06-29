import requests
from bs4 import  BeautifulSoup, NavigableString
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import csv
from selenium.webdriver.common.by import By


path = "level_1_yokakademi2.txt" #you should change with your path

#Urls of all Turkish universities
uniurl= "https://akademik.yok.gov.tr/AkademikArama/view/universityListview.jsp"

link_pt1 = "https://akademik.yok.gov.tr"

r = requests.get(uniurl,verify=False)
soup = BeautifulSoup(r.content,"html.parser")
data_unis = soup.find("tbody",{"class":"searchable"}).find_all("tr")#list of all universities

data = []
for i in data_unis:
    data.append(link_pt1+i.find_all("a")[0]['href'])
#-------------


#Arranging chromdriver
width = 1024
height = 768

chrome_options = Options()
chrome_options.page_load_strategy = 'normal'
chrome_options.add_argument('--enable-automation')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--lang=en')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-browser-side-navigation')
chrome_options.add_argument('--mute-audio')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--force-device-scale-factor=1')
chrome_options.add_argument(f'window-size={width}x{height}')

chrome_options.add_experimental_option(
    'prefs', {
        'intl.accept_languages': 'en,en_US',
        'download.prompt_for_download': False,
        'download.default_directory': '/dev/null',
        'automatic_downloads': 2,
        'download_restrictions': 3,
        'notifications': 2,
        'media_stream': 2,
        'media_stream_mic': 2,
        'media_stream_camera': 2,
        'durable_storage': 2,
    }
)

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.set_page_load_timeout(1000)  # Timeout 10 seconds
#-------------


#FUNCTIONS
def get_info(soup):
    data = soup.find_all("div",{"class":"col-md-6"}) #3data var ilki profili, ikincisi akademik görevler, 3. öğrenim bilgisi

    #---------------------BÖLÜM 1 KİŞİSEL BİLGİLER
    try:
        profil_data = data[0].find("td")
        #---LVL 3'e dahil değil
        with open(path,'a',newline='') as dosya:
            thewriter = csv.writer(dosya, delimiter="$")
            liste = []
            try:
                #print("AKADEMİKSEN ADI:",profil_data.find('h4').text) #akademisyen adı
                liste.append(profil_data.find('h4').text)
            except:
                #print(',')
                liste.append("")
            #----
            try:
                #print("AKADEMİKSYEN MAİL:",profil_data.find_all('a')[1]['href'].replace('[at]','@')[7:]) # akademisyen maili hrefi ve texti mailto:cengizyilmaz@iyte.edu.tr cengizyilmaz[at]iyte.edu.tr
                liste.append(profil_data.find_all('a')[1]['href'].replace('[at]','@')[7:])
            except:
                #print(",")
                liste.append("")
            try:
                #print("ALANI:",profil_data.find("span",{"class":"label label-success"}).text) #bölüm
                liste.append(profil_data.find("span",{"class":"label label-success"}).text)
            except:
                #print(",")
                liste.append("")
            try:
                #print("BÖLÜMÜ:",profil_data.find("span",{"class":"label label-primary"}).text) #alan
                liste.append(profil_data.find("span",{"class":"label label-primary"}).text)
            except:
                #print(",")
                liste.append("")

            nav_str = []
            for i in profil_data.extract():
                if(type(i)==NavigableString):
                    nav_str.append(i)

            try:
                #print("BULUNDUĞU FAKÜLTE:",nav_str[0]) # anlık akademik durumu
                liste.append(nav_str[0])
            except:
                #print(",")
                liste.append("")
            try:
                #print("İLGİ ALANLARI HOBİ VS.:",nav_str[1]) # hobileri vs.
                liste.append(nav_str[1])

            except:
                #print(",")
                liste.append("")

            try:
                #print(soup.find("span",{"class":"pull-right greenOrcid"}).text)
                liste.append(soup.find("span",{"class":"pull-right greenOrcid"}).text)
            except:
                #print(",")
                liste.append("")





            #----------------------BÖLÜM 2 AKADEMİK GÖREVLER
            #print("#######AKADEMİK GÖREVLER#######")
            ogr_bilgisi = data[1].find_all("li")
            ogr_bilgisi_data = ogr_bilgisi[1:-1]
            akademik_grv_sayi = 0
            for i in ogr_bilgisi_data:
                if(ogr_bilgisi_data.index(i)%2==0):
                    try:
                        #print("YIL : ",i.find("span",{"class":"bg-light-blue"}).text)
                        liste.append(i.find("span",{"class":"bg-light-blue"}).text)
                    except:
                        #print(",")
                        liste.append("")
                    akademik_grv_sayi +=1
                else:
                    try:
                        #print("MEVKİ : ",i.find("a",{"class":"btn btn-success btn-xs"}).text)
                        liste.append(i.find("a",{"class":"btn btn-success btn-xs"}).text)
                    except:
                        #print(",")
                        liste.append("")
                    try:
                        #print("ÜNİVERSİTE : ",i.find("h4").text)
                        liste.append(i.find("h4").text)
                    except:
                        #print(",")
                        liste.append("")
                    try:
                        #print("BÖLÜM : ",i.find("h5").text)
                        liste.append(i.find("h5").text)
                    except:
                        #print(",")
                        liste.append("")
                    sayi = 6
                    while(sayi!=0):
                        if(i.find("h"+str(sayi)) == None):
                            #print((8-sayi)*",")#2 hücrelik ÇALIŞMA sütunları için
                            for i in range(8-sayi):
                                liste.append("")
                            sayi=0
                        else:
                            #print("ÇALIŞMA :",i.find("h"+str(sayi)).text)
                            liste.append(i.find("h"+str(sayi)).text)
                            sayi+=1

            #print(((15-akademik_grv_sayi)*5)*",")
            for i in range((15-akademik_grv_sayi)*6):
                liste.append("")


            #----------------------BÖLÜM 3 ÖĞRENİM BİLGİSİ
            #print("#######ÖĞRENİM BİLGİSİ#######")
            ogr_bilgisi = data[2].find_all("li")
            ogr_bilgisi_data = ogr_bilgisi[1:-1]
            ogrenim_blg_sayi=0
            for i in ogr_bilgisi_data:
                if(ogr_bilgisi_data.index(i)%2==0):
                    try:
                        #print("YIL : ",i.find("span",{"class":"bg-light-blue"}).text)
                        liste.append(i.find("span",{"class":"bg-light-blue"}).text)
                    except:
                        #print(",")
                        liste.append("")
                    ogrenim_blg_sayi +=1
                else:
                    try:
                        #print("MEVKİ : ",i.find("a",{"class":"btn btn-info btn-xs"}).text)
                        liste.append(i.find("a",{"class":"btn btn-info btn-xs"}).text)
                    except:
                        #print(",")
                        liste.append("")
                    try:
                        #print("ÜNİVERSİTE : ",i.find("h4").text)
                        liste.append(i.find("h4").text)
                    except:
                        #print(",")
                        liste.append("")
                    try:
                        #print("BÖLÜM : ",i.find("h5").text)
                        liste.append(i.find("h5").text)
                    except:
                        #print(",")
                        liste.append("")
                    sayi = 6
                    while(sayi!=0):
                        if(i.find("h"+str(sayi)) == None):
                            #print((8-sayi)*",")
                            for i in range(8-sayi):
                                liste.append("")
                            sayi=0
                        else:
                            #print("ÇALIŞMA",i.find("h"+str(sayi)).text)
                            liste.append(i.find("h"+str(sayi)).text)
                            sayi+=1
                    
            #print(((15-ogrenim_blg_sayi)*5)*",")
            for i in range((15-ogrenim_blg_sayi)*6):
                liste.append("")

            thewriter.writerow(liste)
            dosya.close()
    except:
        with open(path,'a',newline='') as dosya:
            thewriter = csv.writer(dosya, delimiter="$")
            thewriter.writerow([])
            dosya.close()

def get_teachers():
    authinfo = driver.find_element(By.XPATH, "//table[@id = 'authorlistTb']/tbody")
    authinfos = authinfo.find_elements(By.TAG_NAME,"tr")

    auth_ids = []
    auth_titles = []
    auth_names = []
    auth_links = []
    auth_affils = []
    auth_temels = []
    auth_yans = []

    for a in authinfos:
        soup = BeautifulSoup(a.get_attribute('outerHTML')).tr
        try:
            auth_ids.append(soup.find('span', {'id':'spid'}).text)
        except:
            auth_ids.append('')
        auth_title = soup.find('td', {'width':'110px'})
        try:
            auth_titles.append(auth_title.next_sibling.h6.text)
        except:
            auth_titles.append('')
        try:
            auth_names.append(auth_title.next_sibling.h6.nextSibling.text)
        except:
            auth_names.append('')
        try:
            auth_links.append(auth_title.next_sibling.h6.nextSibling.a.get('href'))
        except:
            auth_links.append('')
        try:
            auth_affils.append(auth_title.next_sibling.h6.nextSibling.nextSibling.text)
        except:
            auth_affils.append('')
        try:
            auth_temels.append(soup.find('span', {'class':'label label-success'}).text)
        except:
            auth_temels.append('')
        try:
            auth_yans.append(soup.find('span', {'class':'label label-primary'}).a.text)
        except:
            auth_yans.append('')

    for j in auth_links:
        driver.get(link_pt1+j)
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource,"html.parser")
        get_info(soup)
        driver.back()

def get_pages():
    global alar
    pages = driver.find_element(By.XPATH,"//ul[@class = 'pagination']")
    pages = BeautifulSoup(pages.get_attribute('outerHTML')).ul
    alar = pages.find_all('a')
    return alar

sayfa_sayi = 1
def search_pages(start,pages):
    global sayfa_sayi
    for i in range(start,len(pages)):
        driver.get(link_pt1+pages[i]['href'])
        get_teachers()
        sayfa_sayi += 1
        #print(sayfa_sayi)


#MAIN
start = 0 #if you don't wanna finish the getting datas at once, you can continue from your last point with this variable
for index, i in enumerate(data[start:]):
    print("%"+str(int((start+index)*(100/len(data))))) #what percentage has been obtained

    driver.get(i)

    if(11 != len(get_pages())):
        get_teachers()
        sayfa_sayi += 1
        #print(sayfa_sayi)
        search_pages(1,get_pages())

    else:
        get_pages()
        get_teachers()
        sayfa_sayi += 1

        search_pages(1,get_pages())

        get_pages()

        while(len(alar) == 12):
            search_pages(2,get_pages())

            get_pages()
     
        search_pages(2,get_pages())

