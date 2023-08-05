
__module_name__ = "_poolq_module.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# local imports #
# ------------- #
from ._supporting_functions._run_poolq import _run_poolq
from ._supporting_functions._get_downloaded_poolq_version import _get_downloaded_poolq_version


class _poolq:

    def __init__(self):
        
        self.poolq_version, self.poolq_path = _get_downloaded_poolq_version()
  
    def run(
        self,
        barcode_file,
        condition_file,
        barcode_reads,
        condition_reads,
        verbose=True,
        ):
        
        _run_poolq(self.poolq_path,
                   barcode_file,
                   condition_file,
                   barcode_reads,
                   condition_reads,
                   verbose)

