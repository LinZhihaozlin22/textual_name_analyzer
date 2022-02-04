from deepface import DeepFace
import boto3
import os
from botocore.exceptions import ClientError
import logging
from name_analyzer.google_crawler import Google_crawler
from name_analyzer.bing_crawler import Bing_crawler


class Name_analysis(object):
    def __init__(self, google_dir, bing_dir, logger_level='W'):
        self.google_dir = google_dir
        self.bing_dir = bing_dir
        self.logger = logging.getLogger()
        if logger_level == 'W':
            logging.basicConfig(level=logging.WARNING)
        elif logger_level == 'I':
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.DEBUG)

    def empty_photo_folder(self):
        self.logger.info('clean storage...')
        for file in os.scandir(self.google_dir):
            os.remove(file.path)
        for file in os.scandir(self.bing_dir):
            os.remove(file.path)

    def race_detect(self):
        self.logger.info('start race detection')
        white_confi, google_count, bing_count = 0.0, 0, 0

        def analyze_race(dir, is_google):
            nonlocal white_confi
            nonlocal google_count
            nonlocal bing_count
            for file in os.listdir(dir):
                if file.endswith(".jpg") or file.endswith(".gif") or file.endswith(".png"):
                    try:
                        obj = DeepFace.analyze(img_path=(dir + file), actions=['race'])
                    except Exception as e:
                        self.logger.debug(e)
                        continue
                    white_confi += obj['race']['white']
                    if is_google:
                        google_count += 1
                        self.logger.debug('google: ' + file)
                    else:
                        bing_count += 1
                        self.logger.debug('bing: ' + file)
                    self.logger.debug(obj)

        analyze_race(self.google_dir, True)
        analyze_race(self.bing_dir, False)
        total_image = google_count + bing_count
        if total_image == 0: return None
        white_confi /= 100 * total_image
        return ['White', white_confi, total_image, google_count, bing_count] if white_confi > 0.5 \
            else ['Non-white', 1 - white_confi, total_image, google_count, bing_count]

    def gender_detect(self):
        self.logger.info('start gender detection')
        male_confi, google_count, bing_count = 0.0, 0, 0
        client = boto3.client('rekognition')

        def analyze_gender(dir, is_google):
            nonlocal male_confi
            nonlocal google_count
            nonlocal bing_count
            for file in os.listdir(dir):
                if file.endswith(".jpg") or file.endswith(".gif") or file.endswith(".png"):
                    with open(dir + file, 'rb') as image:
                        try:
                            response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
                        except ClientError:
                            self.logger.debug("Can't detect face" + ClientError)
                            continue
                        if len(response['FaceDetails']) > 1: continue
                        for faceDetail in response['FaceDetails']:
                            self.logger.debug("Gender: " + str(faceDetail['Gender']))
                            if faceDetail['Gender']['Value'] == 'Male':
                                confidence = faceDetail['Gender']['Confidence']
                            else:
                                confidence = 100 - faceDetail['Gender']['Confidence']
                            if is_google:
                                google_count += 1
                            else:
                                bing_count += 1
                            male_confi += confidence

        analyze_gender(self.google_dir, True)
        analyze_gender(self.bing_dir, False)
        total_image = google_count + bing_count
        if total_image == 0: return None
        male_confi /= total_image * 100
        return ['Male', male_confi, total_image, google_count, bing_count] if male_confi > 0.5 \
            else ['Female', 1 - male_confi, total_image, google_count, bing_count]

    def analyze_name(self, query_dict, num=2, engine='both', search_face=False):
        if not query_dict['last_name']:
            self.logger.warning('Last name is required')
            return None
        filter, query = ['first_name', 'last_name', 'affiliation'], ''
        for f in filter:
            if query_dict[f]:
                query += query_dict[f] + ' '
        Google_crawler(self.google_dir, self.logger).google_image_search(query, num)
        Bing_crawler(self.bing_dir, self.logger).bing_image_search(query, num)
        gender = self.gender_detect()
        race = self.race_detect()
        if gender:
            self.logger.info('query: ' + query + '\ngender: ' + gender[0] + '\nconfidence: ' + str(
                gender[1]) + '\ngoogle img used: ' + str(gender[3]) + '\nbing img used: ' + str(gender[4]))
        else:
            return None
        if race:
            self.logger.info('query: ' + query + '\nrace: ' + race[0] + '\navg_confidence: ' + str(
                race[1]) + '\ngoogle img used: ' + str(race[3]) + '\nbing img used: ' + str(race[4]))
        else:
            return None
        self.empty_photo_folder()
        return {'gender': (gender[0], gender[1]), 'race': (race[0], race[1])}
