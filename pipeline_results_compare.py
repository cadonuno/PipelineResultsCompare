import sys
import argparse
import json
import traceback

all_results = []
modules={}
flaws={}
totalResults = 0
filteredResults = 0

def print_help():
    print("""pipeline_results_compare.py -r1 <results1 json file> -r2 <results2 json file> [-of <output json file> -fs <fail on severity>]"
        Checks if there are any issues present in <results1 json file> that aren't present in <results 2 json file>. 
          Can filter by severity wsith the <fail on severity> parameter.
          Can save a new results file by providing output json file>
""")
    sys.exit()

def read_results(jsonFile):
	try:
		with open(jsonFile) as json_file:
			pipelinedata = json.load(json_file)
			if not 'scan_status' in pipelinedata or pipelinedata['scan_status'] == "SUCCESS":
				print(f'Reading Python file with {len(pipelinedata["findings"])} findings')
				return pipelinedata
			else:
				sys.exit("Pipeline scan status not successful")
	except Exception:
		traceback.print_exc()
		sys.exit("Error within capturing JSON data (see getJSONdata)")

def save_results(newJson, outputFile):
    print("Saving json results to file: " + outputFile)
    try:
        with open(outputFile, "w") as file:
            json.dump(newJson, file)
    except Exception:
        traceback.print_exc()
        sys.exit("Error within capturing JSON data (see getJSONdata)")

              
def handle_results():
    global totalResults
    global filteredResults
    if filteredResults > 0:
        print(f'[FAILURE] {filteredResults}/{totalResults} finding unmitigated finding exceeding severities detected.')
        sys.exit(filteredResults)
    else:
        print(f'[INFO] All {totalResults} finding are mitigated or do not exceed the severity threshold.')

def should_filter_finding(finding, filteredFindings):
    for filter in filteredFindings:
        if (filter['issue_id'] == finding['issue_id']):
            return True
    return False

def compare_results(baseResults, filterFile, failOnSeverity):
    global totalResults
    global filteredResults
    filteredFindings = filterFile['findings']
    allFindings = baseResults['findings']
    print(f'Comparing results between base file ({len(allFindings)} findings) and filter file ({len(filteredFindings)} findings)')

    toRemove = []
    count = 1
    for finding in allFindings:
        totalResults+=1
        if not finding['severity'] in failOnSeverity or should_filter_finding(finding, filteredFindings):
            toRemove.append(finding)
            count+=1
        else:
            filteredResults+=1
    for findingToRemove in toRemove:
        allFindings.remove(findingToRemove)
    return baseResults

def compare(baseResultsFileName, filterFileFileName, failOnSeverity, outputFile):
    baseResults = read_results(baseResultsFileName)
    filterFile = read_results(filterFileFileName)

    newJson = compare_results(baseResults, filterFile, failOnSeverity)

    if outputFile:
        save_results(newJson, outputFile)

    handle_results()

def parse_fail_on_severity(failOnSeverityString):
    failOnSeverity = []
    allSeverities = failOnSeverityString.split(",")
    for severity in allSeverities:
        if severity == "veryhigh":
            failOnSeverity.append(5)
        elif severity == "high":
            failOnSeverity.append(4)
        elif severity == "medium":
            failOnSeverity.append(3)
        elif severity == "low":
            failOnSeverity.append(2)
        elif severity == "verylow":
            failOnSeverity.append(1)
        elif severity == "informational":
            failOnSeverity.append(0)
    return failOnSeverity

def main():
    parser = argparse.ArgumentParser(
        description='This script checks if any findings present in results1 is not present in results2.')
    parser.add_argument('-br', '--baseResults', help='Pipeline scan results json file containing the full list of results')
    parser.add_argument('-ff', '--filterFile', help='Pipeline scan results json file containing a subset of those issues')
    parser.add_argument('-of', '--outputFile', help='Name for new json file to be generated with the filtered results')
    parser.add_argument('-fs', '--fail_on_severity', help='Severities to fail the build on (similar to the fail_on_severity parameter on the pipeline scanner)')
    

    args = parser.parse_args()

    baseResults = args.baseResults
    filterFile = args.filterFile
    outputFile = args.outputFile
    failOnSeverity = args.fail_on_severity

    if not baseResults or not filterFile:
        print_help()
    if not failOnSeverity:
        failOnSeverity = "veryhigh,high,medium,low,verylow,informational"
    else:
        failOnSeverity = failOnSeverity.replace(" ", "").lower()

    compare(baseResults, filterFile, parse_fail_on_severity(failOnSeverity), outputFile)
    
if __name__ == '__main__':
    main()