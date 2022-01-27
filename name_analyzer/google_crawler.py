import requests
from bs4 import BeautifulSoup
import urllib
import logging

class Google_crawler(object):

  def __init__(self, dir, logger):
    self.dir = dir
    self.logger = logger


  def google_image_search(self, query, num):
    self.logger.info('google image crawling...')
    word_dict = query.split(' ')
    query = query.replace(' ', '%20')
    url = 'https://www.google.com/search?q=' + query + '&source=lnms&tbm=isch&sa=X&biw=1920&bih=982'

    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    # Relevant_Images = []  # contains the link for Large original images, type of  image
    # Best_match = []  # contains best matched image
    # for i, table in enumerate(soup.find_all('table')[3:]):
    #   if len(Best_match) == num: break
    #   tag = ''
    #   for href in table.find_all('a', href=True):
    #     tag += href['href'][7:] + ' '
    #   for span_text in table.find_all('span'):
    #     t = span_text.find('span')
    #     if t: tag += t.text + ' '
    #   tag = tag.lower()
    #   img = table.find('img')
    #   self.logger.debug(img)
    #   if img:
    #     src = img.get('src')
    #     if src is None:
    #       src = img.get_attribute('data-src')
    #       if src is None:
    #         continue
    #
    #     if src.startswith("http"):
    #       if all(word.lower() in tag for word in word_dict):
    #         Best_match.append(src)
    #       else:
    #         Relevant_Images.append(src)
    #
    # count = 0
    # for src in [*Best_match, *Relevant_Images]:
    #   if count == num: break
    #   try:
    #     urllib.request.urlretrieve(src, self.dir + str(count+1) + ".png")
    #     count += 1
    #   except Exception as e:
    #     self.logger.warning("could not load: " + url)
    #     continue

    count = 0
    for img in soup.find_all('img')[1:]:
      if count == num: break
      print(img)
      self.logger.debug(img)
      src = img.get('src')
      if src is None:
        src = img.get_attribute('data-src')
        if src is None:
          continue

      if src.startswith("http"):
        urllib.request.urlretrieve(src, self.dir + str(count+1) + ".png")
        count += 1
      else:
        self.logger.warning("image could not retrieve")
        continue