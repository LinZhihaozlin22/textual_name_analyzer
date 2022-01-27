# textual_name_analyzer
A framework to analyze textual name.

## Setup
* In order to access the gender dectection service provided by AWS Rekognition, you will need to first setup AWS CLI. Please follow the steps provided by the link: https://docs.aws.amazon.com/rekognition/latest/dg/setting-up.html

## How to run
**1. First import the package**
```
from name_analyzer import name_analysis

```

**2. Create two directories that you want to store Google and Bing images. (All images will be deleted after each call complete)**

**3. Initialize object**
```
obj = name_analysis(google_dir= 'your_google_image_storage', bing_dir= 'your_bing_image_storage')

```

**4. Call method and get result. It will return a dictionary as {gender: confidence, race: confidence}** 
```
result = obj.analyze_name(query)

```
