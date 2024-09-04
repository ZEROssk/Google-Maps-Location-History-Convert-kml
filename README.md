# usage
## 1. Export Google Maps location-history.json or timeline.json

## 2. pip install requirements.txt
```shell
pip3 install -r requirements.txt
```

## 3. sample
```shell
# convert 1day data
python3 main.py -t location-history.json -s 2024-01-01

# convert range data
python3 main.py -t location-history.json -s 2023-01-01 -e 2024-01-01
```

