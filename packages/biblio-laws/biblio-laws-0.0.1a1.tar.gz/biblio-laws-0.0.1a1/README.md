# Bibliometric Laws Toolkit

A toolkit to examine Laws of Bibliometrics based on bibliometric data 

## Installation
```pip
pip install biblio-laws
```

## Functions
1. Examine the laws of bibliometrics, namely, Bradford's Law, Lotka's Law, and Zipf's Law. 
2. Provide an easy tool to estimate parameters from the proposed formula of the laws.

## Examples
### Examine sample data distributions
```python
from bibliolaws.datasets import *
from bibliolaws.zipf_law import ZipfLaw
from bibliolaws.bradford_law import BradfordLaw
from bibliolaws.lotka_law import LotkaLaw

# (1) Bradford's Law for relationship between journal and publication numbers
bf=BradfordLaw(load_bradford_sample_data())
bf.zone_analysis()
x,y=bf.figure_analysis()

# (2) Lotka's Law for relationship between author and publications numbers
lotka=LotkaLaw(load_lotka_sample_data())
lotka.print_table()
lotka.plot()

# (3) Zipf's Law for relationship between term rank and term freq.
zipf=ZipfLaw(load_zipf_sample_data())
zipf.print_table()
zipf.plot()

```

## Screenshot of results

1. Bradford's Law

![Bradford's Law](https://github.com/dhchenx/dhchenx.github.io/blob/master/projects/biblio-laws/images/bradford_law.png?raw=true)

2. Lotka's Law

![Lotka's Law](https://github.com/dhchenx/dhchenx.github.io/blob/master/projects/biblio-laws/images/lotka_law.png?raw=true)

3. Zipf's Law

![Zipf's Law](https://github.com/dhchenx/dhchenx.github.io/blob/master/projects/biblio-laws/images/zipf_law.png?raw=true)

## License
The `biblio-laws` project is provided by [Donghua Chen](https://github.com/dhchenx). 

