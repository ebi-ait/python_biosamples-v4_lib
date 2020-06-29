# Submit a sample with biosamples-v4 package

## Install from git
```
cd <install directory>
git clone git@github.com:ebi-ait/python_biosamples-v4_lib.git
pip install <install_directory>/python_biosamples-v4_lib
```

## Import useful modules


```python
import biosamples_v4.aap
import biosamples_v4.api
import biosamples_v4.models
import biosamples_v4.encoders
import datetime
import os
import pprint
import json
```

## AAP functions

The lib creates a client for interacting with the AAP apis, you can either set up for the prod or development i.e. "explore" instance following the steps below. 

You can either setup your environment to have variables for your usernames and passwords or replace the `os.environ["<>"]` text in the commands below.

### Prod AAI instance


```python
aap_client = biosamples_v4.aap.Client(username=os.environ["AAP_USERNAME"],
                                     password=os.environ["AAP_PASSWORD"],
                                     url="https://api.aai.ebi.ac.uk")
```


```python
aap_client.get_token()
```


```python
aap_client.get_user_details()
```




    {'userName': 'mshadbolt',
     'email': 'mshadbolt@ebi.ac.uk',
     'userReference': 'usr-c18a3b0f-ad87-4d2b-a77a-7904deec2f5f',
     '_links': {'self': {'href': 'https://api.aai.ebi.ac.uk/users/usr-c18a3b0f-ad87-4d2b-a77a-7904deec2f5f'}}}




```python
aap_client.get_user_membership_domains()
```


```python
aap_client.get_user_managed_domains()
```

### Explore AAI instance


```python
aap_explore_client = biosamples_v4.aap.Client(username=os.environ["AAP_EXPLORE_USERNAME"],
                                     password=os.environ["AAP_EXPLORE_PASSWORD"],
                                     url="https://explore.api.aai.ebi.ac.uk")
```


```python
aap_explore_client.get_token()
```


```python
aap_explore_client.get_user_details()
```




    {'userName': 'mshadbolt_dev',
     'email': 'mshadbolt@ebi.ac.uk',
     'userReference': 'usr-8791cec4-da80-41d1-b3b0-d8e96a7af318',
     '_links': {'self': {'href': 'https://explore.api.aai.ebi.ac.uk/users/usr-8791cec4-da80-41d1-b3b0-d8e96a7af318'}}}




```python
aap_explore_client.get_user_membership_domains()
```


```python
aap_explore_client.get_user_managed_domains()
```

## BioSamples API

### Prod BioSamples API

#### Fetch a sample in the Prod Biosamples instance

```python
bs_api_client = biosamples_v4.api.Client("https://www.ebi.ac.uk/biosamples")
```


```python
bs_api_client.fetch_sample(accession="SAMEA6913455",
                           jwt=aap_client.token)
```

### Dev Biosamples API

#### Submit a sample in the dev BioSamples instance

```python
bs_dev_api_client = biosamples_v4.api.Client("https://wwwdev.ebi.ac.uk/biosamples")
```


```python
test_sample = biosamples_v4.models.Sample(name="Bob",
                                          release=datetime.datetime(2020,6,28),
                                          domain="subs.test-team-65",
                                          ncbi_taxon_id=9606
                                         )
```

    Found species for taxon 9606 with species Homo sapiens



```python
test_sample._append_organism_attribute()
```


```python
test_sample.attributes.extend([biosamples_v4.models.Attribute(name="disease", 
                                                         value="diabetes mellitus",
                                                         iris="http://purl.obolibrary.org/obo/MONDO_0005015"),
                          biosamples_v4.models.Attribute(name="age", 
                                                        value="57", 
                                                        unit="year",
                                                        iris="http://www.ebi.ac.uk/uo/UO_0000036"),
                         biosamples_v4.models.Attribute(name="developmental stage", 
                                                        value="human middle aged stage", 
                                                        iris="http://purl.obolibrary.org/obo/HsapDv_0000092")])
```


```python
bs_sample_encoder = biosamples_v4.encoders.SampleEncoder()
```


```python
pprint.pprint(bs_sample_encoder.default(test_sample))
```

    {'accession': None,
     'characteristics': {'age': [{'ontologyTerms': ['http://www.ebi.ac.uk/uo/UO_0000036'],
                                  'text': '57',
                                  'unit': 'year'}],
                         'developmental stage': [{'ontologyTerms': ['http://purl.obolibrary.org/obo/HsapDv_0000092'],
                                                  'text': 'human middle aged stage',
                                                  'unit': None}],
                         'disease': [{'ontologyTerms': ['http://purl.obolibrary.org/obo/MONDO_0005015'],
                                      'text': 'diabetes mellitus',
                                      'unit': None}],
                         'organism': [{'ontologyTerms': ['http://purl.obolibrary.org/obo/NCBITaxon_9606'],
                                       'text': 'Homo sapiens',
                                       'unit': None}]},
     'contact': [],
     'domain': 'subs.test-team-65',
     'externalReferences': [],
     'name': 'Bob',
     'organization': [],
     'relationships': [],
     'release': '2020-06-28T00:00:00Z',
     'update': '2020-06-29T13:44:07Z'}



```python
response = bs_dev_api_client.persist_sample(bs_sample_encoder.default(test_sample),
                                jwt=aap_explore_client.token)

```


```python
pprint.pprint(response)
```

    {'_links': {'curationDomain': {'href': 'https://wwwdev.ebi.ac.uk/biosamples/samples{?curationdomain}',
                                   'templated': True},
                'curationLink': {'href': 'https://wwwdev.ebi.ac.uk/biosamples/samples/SAMEA7060350/curationlinks/{hash}',
                                 'templated': True},
                'curationLinks': {'href': 'https://wwwdev.ebi.ac.uk/biosamples/samples/SAMEA7060350/curationlinks'},
                'self': {'href': 'https://wwwdev.ebi.ac.uk/biosamples/samples'}},
     'accession': 'SAMEA7060350',
     'characteristics': {'age': [{'ontologyTerms': ['http://www.ebi.ac.uk/uo/UO_0000036'],
                                  'text': '57',
                                  'unit': 'year'}],
                         'developmental stage': [{'ontologyTerms': ['http://purl.obolibrary.org/obo/HsapDv_0000092'],
                                                  'text': 'human middle aged '
                                                          'stage'}],
                         'disease': [{'ontologyTerms': ['http://purl.obolibrary.org/obo/MONDO_0005015'],
                                      'text': 'diabetes mellitus'}],
                         'organism': [{'ontologyTerms': ['http://purl.obolibrary.org/obo/NCBITaxon_9606'],
                                       'text': 'Homo sapiens'}]},
     'create': '2020-06-29T13:45:22.417Z',
     'domain': 'subs.test-team-65',
     'name': 'Bob',
     'release': '2020-06-28T00:00:00Z',
     'releaseDate': '2020-06-28',
     'submittedVia': 'JSON_API',
     'taxId': 9606,
     'update': '2020-06-29T13:45:22.417Z',
     'updateDate': '2020-06-29'}


And you can view the sample at https://wwwdev.ebi.ac.uk/biosamples/samples/SAMEA7060350/

