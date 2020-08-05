## Install from git
```
cd <install directory>
git clone git@github.com:ebi-ait/python_biosamples-v4_lib.git
pip install <install_directory>/python_biosamples-v4_lib
```

## Import useful modules


```python
import biosamples_v4.aap as aap
import biosamples_v4.api as api
import biosamples_v4.models as models
import biosamples_v4.encoders as encoders
import datetime
import os
import pprint
import json
```

## Accession a sample

This process reserves a biosamples accession before you have the full information you want to submit to it. We will got through the process in dev but it works the same in prod, you just need to make sure you use the production aap and bsd api urls.

```python
# create aap client
aap_explore = aap.Client(username=os.environ["AAP_EXPLORE_USERNAME"],
                         password=os.environ["AAP_EXPLORE_PASSWORD"],
                         url="https://explore.api.aai.ebi.ac.uk")
# create bsd api client
bs_dev_api_client = api.Client("https://wwwdev.ebi.ac.uk/biosamples")
```

The following gets you a single accession.

```python
pre_accession = bs_dev_api_client.preaccession("self.team-34", aap_explore.get_token())
```

The following gets 100 accessions and stores them in a list.

```python
accession_list = []
for number in range(1, 100):
    accession_list.append(bs_dev_api_client.preaccession("self.team-34", aap_explore.get_token()))
```

You can then print the list to a file with one accession on each line as follows:

```python
with open('accession_list.txt', 'w') as f:
    for item in accession_list:
        f.write("%s\n" % item)
```