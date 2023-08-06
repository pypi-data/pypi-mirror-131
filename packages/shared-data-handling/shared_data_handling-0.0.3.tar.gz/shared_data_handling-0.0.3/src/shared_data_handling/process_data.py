from tqdm import tqdm
import re, os, errno

def FindFiles(
    rootdir,
    fileNameMask = '(syslog.*)'):
    pattern = re.compile(fileNameMask)
    matches = []
    for root, dirnames, filenames in os.walk(rootdir):
       for filename in filter(lambda name:pattern.match(name),filenames):
           matches.append(os.path.join(root, filename))
    return matches


def ParseFolderRegexPatternList(
    rootdir,
    regexPatternAsVerboseStringList = [r""" """, r""" """],
    fileNameMask = '(syslog.*)',
    firstMatchOnly = False):

    results = []

    files_pbar = tqdm(FindFiles(rootdir, fileNameMask))
    for file in files_pbar:
        files_pbar.set_description(f"Processing {file}")
        data = ParseFileRegexPatternList(
            file, 
            regexPatternAsVerboseStringList,
            firstMatchOnly=firstMatchOnly)
        if not data is None :
            results.extend(data)
    return results

def ParseFolder(rootdir, 
    regexPatternAsVerboseString = r""" """,
    fileNameMask = '(syslog.*)',
    firstMatchOnly = False):
    '''
    Path to the syslogs, sub dirs will also be scanned
    '''
    if(not os.path.isdir(rootdir)):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), rootdir)

    results = []
    files_pbar = tqdm(FindFiles(rootdir, fileNameMask))
    for file in files_pbar:
        files_pbar.set_description(f"Processing {file}")
        data = ParseFileSingleRegexPattern(
            file, 
            regexPatternAsVerboseString,
            firstMatchOnly=firstMatchOnly)
        if not data is None :
            results.extend(data)
    return results
    #return sorted(results, key=lambda x: datetime.datetime.strptime(x['DateTime'], '%Y-%m-%dT%H:%M:%S'))

def ParseFolderBeginMidEndRegexPattern(
    rootdir = ".",
    regexPatternAsVerboseStringBegin = r"""""",
    regexPatternAsVerboseListMiddle = [r"""""",r""""""],
    regexPatternAsVerboseStringEnd = r"""""",
    fileNameMask = '(syslog.*)',
    firstMatchOnly = False):

    results = []
    files_pbar = tqdm(FindFiles(rootdir, fileNameMask))
    for file in files_pbar:
        files_pbar.set_description(f"Processing {file}")
        data = ParseFileBeginMidEndRegexPattern(
            file,
            regexPatternAsVerboseStringBegin,
            regexPatternAsVerboseListMiddle,
            regexPatternAsVerboseStringEnd,
            firstMatchOnly=firstMatchOnly)
        if not data is None :
            results.extend(data)
    return results



def ParseFileRegexPatternList(
    fullFilePath, 
    regexPatternAsVerboseStringList,
    firstMatchOnly = False, 
    completeLine = False):
    '''
    fullFilePath path to a syslog containing the STVolumeCheck data to be analyzed
    clearData: clears the before collecting the data
    '''
    results = []
    result = {}
    with open(fullFilePath, 'r') as f:
        for line in f:
            for regexPatternAsString in regexPatternAsVerboseStringList:
                regexPattern = re.compile(regexPatternAsString, re.VERBOSE)
                data = regexPattern.search(line)
                if not data is None:
                    result['file'] = fullFilePath
                    result['pattern'] = regexPattern
                    result['data'] = data.groupdict()
                    if completeLine:
                        result['line'] = data.groups(0)
                    results.append(result)
                    result = {}
                    break
            if firstMatchOnly and len(results) == len(regexPatternAsVerboseStringList):
                break
    # if(len(results)>0):
    #     print(f"Source: {fullFilePath} result length {len(results)}")
    #     return results
    # else:
    #     print(f"Source: {fullFilePath}, no data found")  

def ParseFileSingleRegexPattern(
    fullFilePath, 
    regexPatternAsVerboseString,
    firstMatchOnly = False):
    '''
    fullFilePath path to a syslog containing the STVolumeCheck data to be analyzed
    clearData: clears the before collecting the data
    '''
    results = []
    result = {}
    regexPattern = re.compile(regexPatternAsVerboseString, re.VERBOSE)
    with open(fullFilePath, 'r') as f:
        for line in f:
            begin = regexPattern.search(line)
            if not begin is None:
                result['file'] = fullFilePath
#                result['pattern'] = regexPatternAsVerboseString
                result.update(begin.groupdict())
                results.append(result)
                result = {}
                if firstMatchOnly:
                    break
    # if(len(results)>0):
    #     print(f"Source: {fullFilePath} result length {len(results)}")
    #     return results
    # else:
    #     print(f"Source: {fullFilePath}, no data found")  

def ParseFileBeginMidEndRegexPattern(
    fullFilePath,
    regexPatternAsVerboseStringBegin,
    regexPatternAsVerboseListMiddle,
    regexPatternAsVerboseStringEnd,
    firstMatchOnly = False):
     '''
     fullFilePath path to a syslog containing the STVolumeCheck data to be analyzed
     clearData: clears the before collecting the data
     '''
     beginRegex = re.compile(regexPatternAsVerboseStringBegin, re.VERBOSE)
     midRegexes = [re.compile(midRegex, re.VERBOSE) for midRegex in regexPatternAsVerboseListMiddle]
     endRegex = re.compile(regexPatternAsVerboseStringEnd, re.VERBOSE)

     beginFound = False
     results = []
     result = {}
   
     with open(fullFilePath, 'r') as f:
         for line in f:
             begin = beginRegex.search(line)
             if not begin is None:
                 beginFound = True
                 result['file'] = fullFilePath
                 result.update(begin.groupdict())
                 midRegexIndex = 0
                 continue
             if beginFound:
                 for midRegex in midRegexes:
                    tempvalue = midRegex.search(line)
                    if not tempvalue is None:
                        for t in tempvalue.groupdict():
                            result[f"{t}_{midRegexIndex}"] = tempvalue.groupdict()[t]
                        midRegexIndex += 1
                        break
                 end = endRegex.search(line)
                 if not end is None:
                     beginFound = False
                     result.update(end.groupdict())
                     results.append(result)
                     result = {}
                     midRegexIndex = 0
                     if firstMatchOnly:
                         break
    #  if(len(results)>0):
    #      print(f"Source: {fullFilePath} result length {len(results)}")
    #      return results
    #  else:
    #      print(f"Source: {fullFilePath}, no data found")