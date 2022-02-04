# textual_name_analyzer
A framework to analyze textual name.

## Setup
* In order to access the gender dectection service provided by AWS Rekognition, you will need to first setup AWS CLI. Please follow the first two steps provided by the link (only need the part about setting up AWS CLI): https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html

## How to run 
check test file as an example

**1. First import the package**
```
from name_analyzer.name_analysis import Name_analysis
```

**2. Create two directories that you want to store Google and Bing images. (All images will be deleted after each call complete)**

**3. Initialize object**
```
obj = Name_analysis(google_dir= 'your_google_image_storage', bing_dir= 'your_bing_image_storage')
```

**4. Call method and get result. It will return a dictionary as {gender: confidence, race: confidence}** 
```
query = {
    'first_name':'first name',
    'last_name': 'last name', #required
    'affiliation': 'affiliation',
    'title': 'title'
}
result = obj.analyze_name(query)
```

**5. Result format**
```
{gender: (label, score), race: (label, score)}
```

**Optional:**
The default number of images to crawl is 2 for each search engine. You can specify a number by passing an integer in second argument.
```
query, num = 'textual_name', 4
result = obj.analyze_name(query, num)
```
