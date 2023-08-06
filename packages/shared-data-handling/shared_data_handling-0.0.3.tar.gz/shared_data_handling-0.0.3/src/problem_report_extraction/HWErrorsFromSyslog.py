import re, json
import shared_data_handling
from shared_data_handling import process_data  

dataPatterns = [r"""Hardware\semergency\sreport""",
                r"""CameraCommunicationError""",
                r"""DrawerLockFailed"""]
                #Add Retries

def ParseFile(fullFilePath):
    '''
    gets the matching regex patterns and keeps them in a list
    '''
    return process_data.ParseFileRegexPatternList(fullFilePath, dataPatterns, completeLine=True)