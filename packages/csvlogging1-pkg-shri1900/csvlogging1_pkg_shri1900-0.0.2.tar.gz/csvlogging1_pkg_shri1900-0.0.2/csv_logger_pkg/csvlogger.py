import os
from datetime import datetime

class csvlogger:
    
        def write_log(self, infotype, debug="", info="", error="", warning="", is_debug_mode_on=False):
            if is_debug_mode_on:
                # calculate file name based on date
                now = datetime.now()  # current date and time
                year = now.strftime("%Y")
                month = now.strftime("%m")
                day = now.strftime("%d")
                filename = year + month + day + ".csv"
    
                # open file
                if os.path.isfile(filename):
                    f = open(filename, "a")
                else:
                    # upload old file on S3
                    # oldfilename = year + month + (day -1) + ".csv"
                    # if os.path.isfile(oldfilename):
                    # try uploading it on S3
    
                    f = open(filename, "w+")
    
                logs = infotype + "," + debug + "," + info + "," + error + "," + warning
    
                # write logs
                f.write(logs + "\n")
    
                # close the file
                f.close()


# Test the file
#csv = csvlogger()
#csv.write_log("1", is_debug_mode_on=True)
#csv.write_log("2", is_debug_mode_on=False)
#csv.write_log("3")
