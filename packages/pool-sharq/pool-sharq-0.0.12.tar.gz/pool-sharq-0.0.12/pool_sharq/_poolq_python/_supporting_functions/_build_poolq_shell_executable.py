
__module_name__ = "_build_poolq_shell_executable.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


def _build_poolq_shell_executable(
    poolq_shell_path,
    barcode_file,
    condition_file,
    barcode_reads,
    reads,
    row_barcode_policy="PREFIX:CACCG@12",
    col_barcode_policy="FIXED:0",
    verbose=False,
):

    """
    Parameters:
    ------------
    poolq_shell_path
        path to poolq3.sh

    barcode_file
        path to barcode/rows/reference.csv file.

    condition_file
        path to columns/conditions.csv file.

    barcode_reads

    condition_reads

    row_barcode_policy

    col_barcode_policy

    verbose
        type: bool
        default: False

    Returns:
    --------
    poolq_shell_executable

    Notes:
    ------

    """

    poolq_shell = "bash {} ".format(poolq_shell_path)
    rows = "--row-reference {} ".format(barcode_file)
    cols = "--col-reference {} ".format(condition_file)
    row_reads = "--row-reads {} ".format(reads)
    col_reads = "--col-reads {} ".format(barcode_reads)
    row_bc_policy = "--row-barcode-policy {} ".format(row_barcode_policy)
    col_bc_policy = "--col-barcode-policy {}".format(col_barcode_policy)

    poolq_shell_executable = (
        poolq_shell
        + rows
        + cols
        + row_reads
        + col_reads
        + row_bc_policy
        + col_bc_policy
    )

    return poolq_shell_executable
