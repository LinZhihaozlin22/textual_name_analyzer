from bs4 import BeautifulSoup
import urllib
import json
import requests
import logging

class Bing_crawler(object):

  def __init__(self, dir, logger):
    self.dir = dir
    self.logger = logger


  def bing_image_search(self, query, num):
    self.logger.info('bing iamge crawling...')
    word_dict = query.split(' ')
    query = query.replace(' ', '+')
    url = 'https://www.bing.com/images/search?q=' + query + '&FORM=IRFLTR'
    header = {
      'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')

    Relevant_Images = []  # contains the link for Large original images, type of  image
    Best_match = []    # contains best matched image
    for a in soup.find_all('a', class_='iusc'):
      if len(Best_match) == num: break
      m = json.loads(a["m"])
      murl = m["murl"]
      turl = m["turl"]
      image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
      tag = (image_name+' '+turl+' '+ murl).lower()
      if all(word.lower() in tag for word in word_dict):
        Best_match.append((image_name, turl))
      else: Relevant_Images.append((image_name, turl))

    self.logger.debug('best matching image', Best_match)
    self.logger.debug('related image', Relevant_Images)
    count = 0
    for image_name, turl in [*Best_match, *Relevant_Images]:
      if count == num: break
      try:
        img_data = urllib.request.urlopen(turl).read()
        with open(self.dir + str(count + 1) + '.png', 'wb') as handler:
          handler.write(img_data)
        count += 1
      except Exception as e:
        self.logger.warning("could not load : " + image_name)
        self.logger.warning(e)
        continue