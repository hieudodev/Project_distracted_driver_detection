from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

# mở trình duyệt với Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

s = Service('D:\Code\Python\CrawlData\drivernew\chromedriver.exe')
wd = webdriver.Chrome(service=s)
def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)
    
	#Link đến trang web cần lấy dữ liệu
	url = "https://www.google.com/search?q=ng%C6%B0%E1%BB%9Di+l%C3%A1i+xe+%C3%B4+t%C3%B4&tbm=isch&ved=2ahUKEwjKtoC7s4P7AhVadt4KHcGRC84Q2-cCegQIABAA&oq=ng%C6%B0%E1%BB%9Di+l%C3%A1i+xe+%C3%B4+t%C3%B4&gs_lcp=CgNpbWcQAzIECCMQJzIGCAAQBRAeMgYIABAIEB4yBwgAEIAEEBgyBwgAEIAEEBgyBwgAEIAEEBg6BAgAEEM6BwgAELEDEEM6CAgAEIAEELEDOgUIABCABDoHCCMQ6gIQJzoICAAQsQMQgwE6CwgAEIAEELEDEIMBOgQIABAeUIQKWPztE2DR8BNoFnAAeAqAAcsBiAHaJJIBBzE0LjI2LjGYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=CAtcY8qSNdrs-QbBo67wDA&bih=589&biw=614&rlz=1C1UEAD_enVN983VN983"
	wd.get(url)

	image_urls = set()
	skips = 0
    # b1 click qua tất cả các ảnh
	# b2 duyệt qua tất cả ảnh click và trả vê link
	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break
				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print('image :',image)

	return image_urls

# hàm lưu ảnh
def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 100)

for i, url in enumerate(urls):
    print('i',i)
    print('url', url)

	#lưu ảnh về máy 
    download_image("D:\Code\Project\DistractedDriverDetection_Final\CrawImages\Images/", url, str(i) + ".jpg")

wd.quit()