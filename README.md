![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/brendonhall/blockhead)
[![Code Coverage](https://img.shields.io/codecov/c/github/brendonhall/blockhead)](https://codecov.io/github/brendonhall/blockhead)
[![Slack](https://badgen.net/badge/icon/slack?icon=slack&label)](https://join.slack.com/invite_code)
[![Kofi](https://badgen.net/badge/icon/kofi?icon=kofi&label)](https://ko-fi.com/vapejordan)

Blockhead is a tool for aligning structure within timeseries.

We're currently supporting the scale space segmentation algorithm of A. Witkin. This algorithm 
finds edges in timeseries as a function of scale. It's useful for segmenting timeseries that
have shocks. As a an applied method, it's used in machine learning applications of well-log 
data in minerals and oil and gas exploration.

### Features
* [Scale space segmentation](https://www.ijcai.org/Proceedings/83-2/Papers/091.pdf), A. Witkin

### Install from source

Currently blockhead can be installed from source: 

```
git clone https://github.com/brendonhall/blockhead.git

cd blockhead

pip install .
```

### Install with Poetry

```
pip install poetry

git clone https://github.com/brendonhall/blockhead.git

cd blockhead

poetry install
```

```
*Coming soon, pip install -U blockhead*
```

### Testing 

```
python -m unittest discover
```

