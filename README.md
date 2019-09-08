# ***q•riority*** is an automated queue management system that improves on itself based on feedback (from the employee and end-user). 


## Backend Prerequisites
**Disclaimer:** _The backend has been tested to work on MacOS and Ubuntu 18.04 (If the prerequisites are satisfied, it may work on other OSs too, we just haven’t tested it yet..)_

Make sure you have [Python3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py) installed first for your specific distribution.

#### Create a virtual environment

```shell
python3 -m venv .env
source .env/bin/activate
```

#### Install the required Python libraries and frameworks.

Run the Python console using
 
```shell
python3
```

And input the following

```python
import nltk; nltk.download(‘stopwords’)
python3 -m spacy download en
```

Make sure you’re in the same directory as *requirements.txt*, and run the following command on your terminal.

```shell 
pip3 install -r requirements.txt 
```

**Disclaimer:** _This may take a while._


##  Setting up and Executing the Backend

## To be added:
>1. Video demo gif / working just the gifs of screens for the backend / Manager's Panel 
>2. Flowchart (the big one)
>3. Link to Presentation in both
>4. Data for Data Analytics Model/ current implementation drawbacks