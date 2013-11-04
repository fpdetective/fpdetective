
from multiprocessing import Pool

def run_in_parallel(inputs, worker, no_of_processes=4):
    """Run given worker function in parallel with nunmber of processes given."""
    # TODO multiprocessing does not work in PlanetLab nodes. OS Error 38! 
    # Fall back to another parallelization method if there's an error.
    p = Pool(no_of_processes)
    p.map(worker, inputs)