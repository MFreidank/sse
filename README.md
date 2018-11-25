# Hippocrates &emsp;  <img src="https://raw.githubusercontent.com/escodebar/sse/fix/extend_README/data/images/hippo_small.png" alt="alt text" width="5%"> &emsp; <img src="https://www.baselhack.ch/frontend/images/logo/baselhack_black.png" alt="alt text" width="7%">

![alt text](https://travis-ci.org/escodebar/sse.svg?branch_master)

**Problem:** Researchers in medicine and biology often need access to 
combined information about the interaction of different topics such 
as drugs, genes and biological pathways. 
While paper repositories such as PubMed provide easy access to publications, 
linking information from publications is a tedious and manual process. 

**Solution:**
* Provide intelligent semantic search engine for publication data.
* Extract and match combinations of topics in user input in 
bio-medical publication repositories.
* Integrate publicly available scientific vocabularies from Athena.
* Use *Machine Learning* to identify new trending topics that our database does not 
yet contain. 

**Additional Resources:**
* Publication repositories:
[PubMed](https://www.ncbi.nlm.nih.gov/pubmed), [Medline](https://www.medline.eu/de/)
* Standardized OMOP vocabularies:
[Athena](https://www.ohdsi.org/analytic-tools/athena-standardized-vocabularies/)
* Cognitive services for text extraction with Machine Learning:
[Azure](https://azure.microsoft.com/en-us/services/cognitive-services/?v=18.44a)
* Blazing-fast multi-string matching:
[pyahocorasick](https://github.com/WojciechMula/pyahocorasick)
* Automated software tests after each commit:
[Travis](https://travis-ci.org/escodebar/sse)

Pitched and implemented as part of [BaselHack 2018](https://www.baselhack.ch).
Our presentation slides are available [here](https://github.com/escodebar/sse/raw/master/presentation/Hippocrates_Presentation_20181125_FINAL.pdf).

### Setup

To setup the API, create a Python virtual environment and install the `Django` 
backend and `Vue.js` frontend.

```shell
$ git clone git@github.com/escodebar/sse.git && cd sse
$ python3 -m venv . && source bin/activate
$ (sse) python3 -m pip install -e . -r requirements.txt -c constraints.txt
$ (sse) python3 manage.py migrate
$ (sse) python3 manage.py runserver

# install frontend
$ npm install

# build for production with minification
$ npm run build
```

### Built with:
<img src="https://vuejsexamples.com/content/images/2017/10/vuejsexamples.png" alt="alt text" width="10%"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/2000px-Python.svg.png" alt="alt text" width="10%"> <img src="https://www.djangoproject.com/m/img/logos/django-logo-positive.png" alt="alt text" width="15%"> <img src="https://overview.azureedge.net/cdn/Azure%20Cognitive%20Services.png" alt="alt text" width="15%"> <img src="http://kutaslab.ucsd.edu/people/urbach/images/pubmed_icon.png" alt="alt text" width="15%"> <img src="https://pbs.twimg.com/profile_images/893569174269603840/EtH4vbqO.jpg" alt="alt text" width="15%"> <img src="https://travis-ci.com/images/logos/Tessa-1.png" alt="alt text" width="15%">



