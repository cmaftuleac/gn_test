Note! Storage contains only actual data, therefore storage cleans after getting data from it. In order to avoid errors, run fetchData script before running script for getting data from the storage!


chmod +x fetchData.py getCommodityPrice.py

apt install python-pip 

pip install virtualenv

virtualenv -p python3 .venv

source .venv/bin/activate

pip install -r requirements.txt

apt install mongodb-clients

apt install mongodb-server

./fetchData.py 

./getCommodityPrice.py 2018-10-29 2018-11-18 gold



