import re, os

RunSchedulerRegex = re.compile(r"""Roche.c5800.ProcessScheduler.RunScheduleChanged.*?RunState""", re.VERBOSE)
GeneralInstrumentAccessRegex = re.compile(r"""Roche.Sting.InstrumentAccess.Messages.\S+.Events.""", re.VERBOSE)
ProcessExecutionRFIDDataRegex = re.compile(r"""Roche.c5800.ProcessExecution.*?ContentChange.*?RfidData""", re.VERBOSE)
IMFlagsDataRegex = re.compile(r"""Roche.c5800.ProcessExecution.WorkOrderFlagged""", re.VERBOSE)


def ParseFile(fullFilePath):
    '''
    gets the matching regex patterns and keeps them in a list
    '''
    results = []
    with open(fullFilePath, mode='r', encoding="utf8") as f:
        for line in f:
            data = RunSchedulerRegex.search(line)
            if data:
                results.append(line)
                continue
            data = GeneralInstrumentAccessRegex.search(line)
            if data:
                results.append(line)
                continue
            data = ProcessExecutionRFIDDataRegex.search(line)
            if data:
                results.append(line)
                continue
            data = IMFlagsDataRegex.search(line)
            if data:
                results.append(line)
                continue
    if(len(results)>0):
        return list(filter(None, results)) 
    else:
        return None
    
def ParseFolder(rootdir, fileFilter = r".*.log", relativeOutputFilePath = "ICRelevantEventStream.log"):
    '''
    writes the content of the extracted event stream into a output file.
    '''
    results = []
    regex = re.compile(fileFilter)
    for path, _, files in os.walk(rootdir):
        for file in files:
            if regex.match(file):
                results_new = ParseFile(os.path.join(path,file))
                if not results_new is None :
                    results.extend(results_new)
    with open(os.path.join(rootdir, relativeOutputFilePath), 'w') as file:
        file.writelines(results)
    with open(os.path.join(rootdir, relativeOutputFilePath), 'r') as file:
            first_line = file.readline()
            for last_line in file:
                pass
    return (relativeOutputFilePath, first_line, last_line)


if __name__ == '__main__':
    #For testing purposes only!
    ParseFolder(f'C:/ProblemReportExtracts/PR-c5800-543-20210330_070015/eventstream')

