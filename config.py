import datetime

# the individual graph plts are stored in this folder
graphFolder = "graphs"

# at what time did the recording of the video file start?
videoCreationDatetime = datetime.datetime(year=2021, month=11, day=4, hour=14, minute=1, second=42)

# evaluate a video frame every <samplingIntervalInSeconds>
samplingIntervalInSeconds = 1

#  graph title
graphTitle = "Evolution of Twitter Space listeners"

# where does the time range start on the graphs?
graphStartTime = "14:00:00"

# where does the time range stop on the graphs?
graphEndTime = "14:40:00"

# what is the minimum number of listeners displayed in the graphs?
graphMinimumNumberOfListeners = 0

# what is the maximum number of listeners displayed in the graphs?
graphMaximumNumberOfListeners = 1000
