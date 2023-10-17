# Veracode Pipeline Results Compare

Checks if there are any issues present on a pipeline results file that aren't present on another.    
Can filter by severity with the fail on severity parameter.  
Can save a new results file by providing a json output file

## Setup

Clone this repository:

    git clone https://github.com/cadonuno/PipelineResultsCompare

Install dependencies:

    cd PipelineResultsCompare
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Run

If you have saved credentials as above you can run:

    python pipeline_results_compare.py (arguments)

Otherwise you will need to set environment variables:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python vcpipemit.py (arguments)

Arguments supported include:

* `--baseResults`, `-br`  (required): Pipeline scan results json file containing the full list of results.
* `--filterFile`, `-ff` (required):Pipeline scan results json file containing a subset of those issues.
* `--outputFile`, `-of` (optional): Name for new json file to be generated with the filtered results.
* `--fail_on_severity`, `-fs` (optional, defaults to "Very High, High, Medium, Low, Very Low, Informational"): Severities to fail the build on (similar to the fail_on_severity parameter on the pipeline scanner).
