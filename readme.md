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

## save to file
with open("kprm-firmy-tylko-regony-pkd.txt", "w") as outfile:
    outfile.write("\n".join(kody_pkd))

```

Distribution of PKD codes

```python
np.array(np.unique(kody_pkd, return_counts=True)).T
```

```
array([['', '39'],
       ['5030Z', '2'], # B
       ['5222B', '6'], # B
       ['5911Z', '1'], # B
       ['7500Z', '1'], # M
       ['8411Z', '148'], # O
       ['8412Z', '54'], # O
       ['8413Z', '755'], # O
       ['8422Z', '86'], # O
       ['8424Z', '249'], # O
       ['8425Z', '243'], # O
       ['8430Z', '1'], # O 
       ['8559B', '2'], # O 
       ['8610Z', '1'], # O
       ['9101B', '34'], # R
       ['9420Z', '9'], # S
       ['9499Z', '1']],  # S
       dtype='<U21')
```
