# pool-sharq
Python wrapper for the Broad Institute GPP's [poolq software](https://portals.broadinstitute.org/gpp/public/software/poolq)

Uses the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) webscraping library to check for the latest distribution of poolq from the Broad Institute's GPP. Downloads the latest distribution if it is not already downloaded.

### Install

```BASH
pip install pool_sharq
```


### Usage

```python
import pool_sharq

poolq = pool_sharq.poolq(dir="/path/to/data/") # contains rows.txt and columns.txt along with fastq files. 
poolq.run()
```

### You can also download / use test data provided by the GPP
```python
pool_sharq.download_test_data()
```

```python
poolq = pool_sharq.poolq() # point to test data
poolq.run()
```

