# handles all image-related components

from bs4 import BeautifulSoup
import requests

# the first 747! I wonder if planespotters has it. They must, right?
test_reg = 'AS881'

def search_url(reg: str) -> str:
    '''Gets the search url for recent photos of a plane, by registration.'''
    return f'https://www.planespotters.net/photos/reg/{reg}'

def get_last_photo_url(reg: str) -> str:
    '''Gets the URL of the last high-quality photo from planespotters, by registration.'''
    url = search_url(reg)

    # thanks, stackoverflow!
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')
    imgs = soup.find_all('img', {'class': 'photo_card__photo'})

    if not len(imgs):
        return None
    return imgs[0]['src']

if __name__ == '__main__':
    # run the test func
    print(get_last_photo_url(test_reg))
