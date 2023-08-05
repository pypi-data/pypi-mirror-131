
__module_name__ = "_poolq_downloader.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# package imports #
# --------------- #
from bs4 import BeautifulSoup
import licorice
import os
import pandas as pd
import requests
from tqdm.notebook import tqdm as tdqm_nb
import urllib.request


def _return_soup(path):

    source = urllib.request.urlopen(path).read()

    return BeautifulSoup(source, features="html.parser")


def _find_latest_version(df, verbose=True):

    latest_version = df["version"].max()
    
    if verbose:
        print(
            "Latest version of poolq: {}".format(
                licorice.font_format(latest_version, ["BOLD", "CYAN"])
            )
        )

    return latest_version


def _download_file(url, filename):
    """
    Helper method handling downloading large files from `url` to `filename`. Returns a pointer to `filename`.
    """
    chunk_size = 1024
    downloadable = requests.get(url, stream=True)
    
    with open(filename, 'wb') as file:
        progress_bar = tdqm_nb( unit="B", total=int( downloadable.headers['Content-Length'] ) )
        for chunk in downloadable.iter_content(chunk_size=chunk_size): 
            if chunk:
                progress_bar.update (len(chunk))
                file.write(chunk)
        progress_bar.close()
    
def _download_poolq(out_path, poolq_http, latest, tmp_out_path="poolq.tmp.zip"):

    """"""
    _download_file(url=poolq_http, filename=tmp_out_path)
    os.system("unzip -q {}".format(tmp_out_path))  # unzip
    os.system("rm -r {}".format(tmp_out_path))  # remove temp zip
    os.system("rm -r poolq-{}/test-data/".format(latest))
    os.system("rm -r poolq-{}/*pdf".format(latest))
    os.system("rm -r poolq-{}/*html".format(latest))
    os.system("mv poolq-{} {}".format(latest, out_path))
    
    
def _download_tests(out_path, poolq_http, latest, tmp_out_path="poolq.test_data.tmp.zip"):

    """"""
    _download_file(url=poolq_http, filename=tmp_out_path)
    os.system("unzip -q {}".format(tmp_out_path))  # unzip
    os.system("rm -r {}".format(tmp_out_path))  # remove temp zip
    os.system("rm -r poolq-{}/*.bat".format(latest))
    os.system("rm -r poolq-{}/*.jar".format(latest))
    os.system("rm -r poolq-{}/*.sh".format(latest))
    os.system("rm -r poolq-{}/*pdf".format(latest))
    os.system("rm -r poolq-{}/*html".format(latest))
    os.system("mv poolq-{}/test-data/* {}".format(latest, out_path))
    os.system("rm -r poolq-{}".format(latest))

def _find_available_poolq_versions(poolq_path, download_path):

    """"""

    soup = _return_soup(poolq_path)

    poolq_distributions = {}
    poolq_distributions["name"] = []
    poolq_distributions["version"] = []
    poolq_distributions["path"] = []

    for line in soup.findAll("a"):
        if line.text.startswith("poolq-") and "zip" in line.text:
            poolq_distributions["name"].append(line.text)
            version = line.text.replace(".zip", "").split("-")[-1]

            poolq_distributions["version"].append(version)
            poolq_distributions["path"].append(
                download_path + "&filename=poolq-{}.zip".format(version)
            )

    return pd.DataFrame.from_dict(poolq_distributions)


class _poolq_downloader:

    """"""

    def __init__(self):

        """"""

        self.poolq_path = (
            "https://portals.broadinstitute.org/gpp/public/dir?dirpath=poolq-downloads"
        )
        self.download_path = "https://portals.broadinstitute.org/gpp/public/dir/download?dirpath=poolq-downloads&filename=poolq-{}.zip"

    def fetch_available(self, verbose=True):
        """"""

        self.version_df = _find_available_poolq_versions(
            self.poolq_path, self.download_path
        )
        self.latest = _find_latest_version(self.version_df, verbose)

    def download(self, out_path="./"):

        """"""

        poolq_http = self.download_path.format(self.latest)
        _download_poolq(out_path, poolq_http, self.latest)
        
    def download_tests(self, out_path):
        
        """ """
        
        poolq_http = self.download_path.format(self.latest)
        _download_tests(out_path, poolq_http, self.latest)
        
def _look_for_poolq(path):

    """Check if poolq exists. If not, download it."""
    
    _poolq_download_path = os.path.join(os.path.dirname(path), "_distribution/")

    get_poolq = _poolq_downloader()
    get_poolq.fetch_available()
    if os.path.exists(_poolq_download_path + "poolq-{}".format(get_poolq.latest)):
        print("\nLatest installation of poolq: poolq-{} previously installed.".format(get_poolq.latest))
    else:
        print("\nDownloading...")
        get_poolq.download(_poolq_download_path)
