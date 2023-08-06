from zipfile import ZipFile
from tempfile import TemporaryDirectory
import subprocess, os,re, sys, logging, glob, datetime, argparse, multiprocessing, time, shutil, json
from EventStreamDataExtractor import ParseFolder

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
ICExtractorVersion = "0.07"
#path to the compressed IC data inside the problem report
logandconfig_path = 'instrumentlogs'
#compressed IC data inside the problem report
logandconfig_name = 'logandconfig.zip'
#path to the event steam files within the problem report
eventStream_FullName = 'eventstream'
#shall the sensordata be retained?
keepICDataFolders = {'persistentdata': False, 'pipettingparametersets': False, 'sensordata': True, 'teachdata': True}

#Windows path to the 7zip executable
z7zipPath = "C:/Program Files/7-Zip/7z.exe"
#for ubuntu use sudo apt-get install p7zip-full
#z7zipPath = "7z"

#File filter for the ic log folder, by default all files will be merged into one file and the original files will be removed from the output
#If the flag is set to false, the original log will be retained in the output folder.
handleLogFiles = {'sar-avg.log': True, 'sar-bdio.log': True, 'disk.log': True,'mem.log': True,
                'sar-cpu.log': True, 'sar-cswi.log': True, 'sar-dev.log': True,
                'sar-edev.log': True, 'sar-io.log': True, 'sar-mem.log': True,
                'sar-sock.log': True, 'sar-tcp.log': True, 'sar-udp.log': True,
                'syslog': True}

class Extract:
    def __init__(self, zips, output_directory, archive_password, extractEventStreamData = True):
        self.zips = zips
        self.output_directory = output_directory
        self.archive_password = archive_password
        self.z7ZipPath = z7zipPath
        self.logandconfig_path = logandconfig_path
        self.logandconfig_name = logandconfig_name
        self.logandconfig_FullName = os.path.join(self.logandconfig_path, self.logandconfig_name)
        self.eventStream_FullName = eventStream_FullName
        self.extractEventStreamData = extractEventStreamData
        self.handleLogFiles = handleLogFiles

        if(not os.path.exists(self.output_directory)):
            os.mkdir(self.output_directory)

    def mergeLogFiles(self, problemReportName, fileNamePrefix, pathToLogs, deleteFilesAfterMerge=False):
        '''
        :param fileNamePrefix: e.g syslog when syslog.1 ... have to be processed
        :param pathToLogs: relative or absolute path
        :param deleteFilesAfterMerge: boolean deletes original logs after the files being combined
        :return: None
        Note: The log files are being sorted by there names.
        The merged file will have the name defined in the prefix (e.g syslog)
        the original syslog will be renamed to syslog.0
        '''
        message = f"merging all {fileNamePrefix}s into one {fileNamePrefix}"
        if deleteFilesAfterMerge:
            logging.debug(f"{message} and removing the excess files")
        else:
            logging.debug(f"{message} and keeping the excess files")

        #rename the log file to simplify the sorting algo
        try:
            fullpathToLogs = os.path.join(self.outputFullPath, pathToLogs)
            if os.path.exists(os.path.join(fullpathToLogs, fileNamePrefix)):
                os.rename(os.path.join(fullpathToLogs, fileNamePrefix), os.path.join(fullpathToLogs, f"{fileNamePrefix}.0"))
                filenames = [f for f in os.listdir(fullpathToLogs) if re.match(f'{fileNamePrefix}\.\d+', f)]
                sortedFileName = sorted(filenames, key = lambda x: int(x.split('.')[-1]), reverse=True)
                #merge the files into one log and optionally discard the old logs
                fileName = f"{problemReportName}_{fileNamePrefix}"
                fullFileName = os.path.join(fullpathToLogs, fileName)
                lines = []
                for names in sortedFileName:
                    with open(os.path.join(fullpathToLogs, names)) as infile:
                        lines.append(infile.read())
                with open(fullFileName, 'w') as outfile:
                    outfile.writelines(lines)

                if deleteFilesAfterMerge:
                    for logfile in sortedFileName:
                        os.remove(os.path.join(fullpathToLogs, logfile))
                #glimpse into syslogs to show the datetime at the beginning and ending of the file
                with open(fullFileName, "r") as file:
                    first_line = file.readline()
                    second_line = file.readline()
                    for last_line in file:
                        pass
                return (os.path.join(pathToLogs, fileName), second_line, last_line)
        except:
            logging.debug(f'Unable to handle files with \'{fileNamePrefix}\', check log folder for suspicious files...')

    def ExtractDataFromZip(self, zipfileFullName, outputDirFullName, fileInZipFileToExtract):
        '''
        method for extracting the data, has to handle password encrypted files and folders.
        for performance reason the default python lib has been replaced with 7-zip
        '''
        if self.archive_password == "":
            command = f'{self.z7ZipPath} x \"{zipfileFullName}\" -o"{outputDirFullName}" "{fileInZipFileToExtract}" -y'
        else:
            command = f'{self.z7ZipPath} x \"{zipfileFullName}\" -o"{outputDirFullName}" -p{self.archive_password} "{fileInZipFileToExtract}" -y'
        #omit traces from 7-zip
        logging.debug(command)
        returnValue = subprocess.check_call(command,stdout=open(os.devnull, 'w'))
        logging.debug(f"Extracting IC problem report contents from {zipfileFullName}, return value {returnValue}.")

    def extractICData(self, fullProblemReportName):
        '''
        Extract the logandconfig.zip file into a temp folder and extract the data to the target output directory.
        The log files will be merged and renamed except for the syslogs. Can be set in the handleLogFiles dictionary
        '''
        try:
            self.problemReportName = os.path.splitext(os.path.basename(fullProblemReportName))[0]
            logging.info(f"Processing ProblemReport \"{self.problemReportName}\"")
            #Do the heavy lifting...
            if not fullProblemReportName.endswith(".zip"):
                logging.error(f"the file \"{self.problemReportName}\" is not a zip file ")
            #Extend the output path with the datetime if the extract already exists in the output folder
            outputProblemReportName = self.problemReportName
            self.outputFullPath = os.path.join(self.output_directory, outputProblemReportName)
            if os.path.isdir(self.outputFullPath):
                logging.warning(f"PR extract for \"{outputProblemReportName} does already exist appending timestamp")
                self.outputFullPath += datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
            #write the ic problem report to the temp folder
            with TemporaryDirectory(prefix=outputProblemReportName) as tempDirName:
                #Extract the logandConfig.zip file to a temp folder
                self.ExtractDataFromZip(fullProblemReportName,tempDirName,self.logandconfig_FullName)
                #Extract the extracted logandconfig.zip file to the output folder
                with ZipFile(os.path.join(tempDirName,self.logandconfig_FullName), "r") as zf:
                    zf.extractall(self.outputFullPath)
            
            self.LogFileRanges =  {}
            #extract the event stream data?
            if self.extractEventStreamData:
                self.ExtractDataFromZip(fullProblemReportName,self.outputFullPath,self.eventStream_FullName)
                eventStreamRange = ParseFolder(rootdir=self.outputFullPath, relativeOutputFilePath=os.path.join("log",f"{self.problemReportName}_systemeventstream.log"))
                self.LogFileRanges[eventStreamRange[0]] = (eventStreamRange[1], eventStreamRange[2])
                shutil.rmtree(os.path.join(self.outputFullPath, self.eventStream_FullName))

            logging.debug(f"All files successfully extracted to {outputProblemReportName}")
            #do some clean up of the temp files
            #os.remove(tmpLogAndConfigFullFileName)
            logging.debug("Delete temporary files")
            #merge the log files, or not
            for k, v in handleLogFiles.items():
                        fileRange = self.mergeLogFiles(self.problemReportName, k, "log", deleteFilesAfterMerge=v)
                        self.LogFileRanges[fileRange[0]] = (fileRange[1], fileRange[2])
            #delete not used data
            for folder, shallKeepFolder in keepICDataFolders.items():
                if not shallKeepFolder:
                    shutil.rmtree(os.path.join(self.outputFullPath, folder))
            
            with open(os.path.join(self.outputFullPath, "metadata.json"), 'w') as metafile:
                json.dump(self.LogFileRanges, metafile) 

            logging.info(f"Processed ProblemReport \"{outputProblemReportName}\"")
        except subprocess.CalledProcessError as e:
            logging.error(f"Unable to extract \"{self.problemReportName}\" from the ProblemReport. ReturnValue from 7zip: \"{e.output}\"")
        except Exception as e:
            logging.error(f"Failed to process ProblemReport \"{self.problemReportName}\", {e}")

    def ExtractProblemReports(self):
        s = time.perf_counter()
        logging.info(f"IC PR Extractor V{ICExtractorVersion}")
        logging.info(f"Output directory \"{self.output_directory}\"")

        if len(self.zips) > 1:
            logging.info(f"Processing multiple problem reports in parallel, traces may be messy but processing is faster...")
            # #This is not a pure multiprocessing but this gives a speedbump with more then 5 PRs
            with multiprocessing.Pool(multiprocessing.cpu_count() + 1) as pool:
                for r in pool.imap_unordered(self.extractICData, self.zips):
                    pass
        else:
            logging.info(f"Processing single problem report")
            self.extractICData(self.zips[0])
        
        elapsed = time.perf_counter() - s
        logging.info(f"Execution took {elapsed:0.2f} seconds.")

if __name__ == "__main__":
    s = Extract(zips = ['C:/Users/rothf9/Desktop/watcher/transfer/PR-c5800-518-20210119_162111.zip'],
                output_directory = 'C:/Users/rothf9/Desktop/watcher/output',
                archive_password = 'TDFU@Bsting17',
                extractEventStreamData = True)

    s.ExtractProblemReports()
    
    
    #TODO: Extract counters and save in the meta data file.