# BlastWrapper

`BlastWrapper` is a Python package designed to interact with the **BLAST (Basic Local Alignment Search Tool)** API provided by NCBI. It allows users to submit, check the status of, and retrieve results from BLAST queries using simple functions.


## Features
- Submit a BLAST query with specific parameters (e.g., program, database).
- Check the status of the BLAST query (whether it is still running or completed).
- Retrieve results from completed BLAST queries in various formats.

## Installation

You can install `blastwrapper` via **Poetry** or **pip** (if published to PyPI in the future).

### Using Poetry
1. Install Poetry if you haven't already:  
   [Poetry installation guide](https://python-poetry.org/docs/#installation)
   
2. Clone the repository and install the dependencies:
   ```sh
   git clone https://github.com/yourusername/BLASTWrapper.git
   cd BLASTWrapper
   poetry install
   ```

### Using pip
```sh
pip install blastwrapper
```

## Usage

### Functions Overview

    put_query: Submits a BLAST query to the server and returns a RID (Request ID).
    check_status: Checks if the BLAST query has completed by monitoring the status with the provided RID.
    get_results: Retrieves the results of the BLAST query after it has completed.


### Step 1: Submit a BLAST query
```python
from blastwrapper import put_query, check_status, get_results
sequence = "ATCGATCGATCG"
rid = put_query(sequence)  # Returns the RID of the submitted query
```
### Step 2: Check the status of the BLAST query
```python
import time
status = "NOT READY"
while status != "READY":
    time.sleep(60)  # Wait for 1 minute before checking again. Do not lower this, as BLAST requires this as a minimum wait time
    status = check_status(rid, time_elapsed=60)
```
### Step 3: Get the results after the job completes
```python
results = get_results(rid)
print(results.text)  # Print the results in the selected format
```
#### Parameters for put_query:

- *sequence*: The query sequence to search for (required).
- *program*: The BLAST program to use (default: "blastn").
- *database*: The BLAST database to search (default: "core_nt").
- *short_query, filter, expect, nuc_rew, nuc_pen, word_size, gap_cost, matrix, cbs, ht_list, fmt_type, description, alignment, report*: Various other parameters that have same default values as BLAST documentation you can customize (refer to [NCBI BLAST documentation](https://blast.ncbi.nlm.nih.gov/doc/blast-help/urlapi.html#urlapi)).

#### Parameters for check_status:

- *rid* (required): The request ID (RID) obtained from the put_query function. 
- *time_elapsed* (required): Time in seconds since the query was submitted. This can be used to track how long the query has been running.
- *fmt_type, fmt_object, align_view, descr, align, report*: Additional customization parameters for status checking that have same default values as BLAST documentation (refer to [NCBI BLAST documentation](https://blast.ncbi.nlm.nih.gov/doc/blast-help/urlapi.html#urlapi)).

#### Parameters for get_results:

- *rid*: The request ID (RID) obtained from the put_query function.
- *view_res*: The format of the result view (default: "FromRes").
- *fmt_type*: The format type for the results (default: "Text").
- *descr, align, report*: Other parameters to customize the result display that have same default values as BLAST documentation (refer to [NCBI BLAST documentation](https://blast.ncbi.nlm.nih.gov/doc/blast-help/urlapi.html#urlapi)).

## Testing

For testing see the tests/ directory. It is highly recommended to run tests via poetry. 

```bash
 poetry run pytest -v
 ```

## License 
This project is licensed under the MIT License – see the LICENSE file for details.
