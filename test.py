import shutil, os
def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S-{fname}'):
        import datetime
        # This creates a timestamped filename so we don't overwrite our good work
        return datetime.datetime.now().strftime(fmt).format(fname=fname)

shutil.copy("officerOnDuty.jpg", "MediaBackUp/OfficerOnDuty/" + timeStamped("DutyOff.jpg"))
shutil.copy("movie.mp4", "MediaBackUp/VideoEvidence/" + timeStamped("EmgVideo.mp4"))
