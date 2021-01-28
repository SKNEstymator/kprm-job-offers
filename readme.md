# Repository for the papers on KPRM data

1. Webscraping

2. Using REGON API

```python
!pip install gusregon

## libraries
from gusregon import GUS
import requests
gus=GUS(api_key="xxxx")

## data
regon_file = "https://raw.githubusercontent.com/SKNEstymator/kprm-job-offers/main/data/kprm-firmy-tylko-regony.txt"
response = requests.get(regon_file)
data = response.text.split("\n")


## there are still some with missing codes or wrong
np.unique([len(i) for i in data])
# array([ 0, 12, 13, 14, 15])

## get PKD codes based solely on regon code
k = 0
kody_pkd = []
for kod in data:
  print(k)
  mm = gus.get_pkd(regon=kod)
  if len(mm)==0:
    kody_pkd.append("")
  else:
    kody_pkd.append(mm[0]["code"])
  k +=1

```

