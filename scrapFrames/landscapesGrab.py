from urllib.parse import unquote 
from selenium import webdriver

def search(query):
    driver = webdriver.Firefox()

    # For one word queries it will be ok, for complex ones should encode first
    driver.get(f'https://duckduckgo.com/?q={query}&t=h_&iax=images&ia=images') 

    # For now it's working with this class, not sure if it will never change
    img_tags = driver.find_elements_by_class_name('tile--img__img') 

    for tag in img_tags:
        src = tag.get_attribute('data-src')
        src = unquote(src)
        src = src.split('=', maxsplit=1)
        src = src[1]
        yield src

    driver.close()

if __name__ == '__main__':
    from pprint import pprint
    imgs_urls = list(search('sun'))
    pprint(imgs_urls)