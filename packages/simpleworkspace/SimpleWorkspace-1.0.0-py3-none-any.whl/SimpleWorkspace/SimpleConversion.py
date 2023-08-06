class ByteConversion:
    KB = 1000
    MB = 1000000
    GB = 1000000000

    def __init__(self):
        return

    @staticmethod
    # ForcePrefix=
    def GetStringRepresentation(totBytes, prefix, precisionDecimals=2):
        """
        :param ForcePrefix: b, kb, mb, gb
        """
        if(prefix == "b"):
            return str(totBytes) + " B"
        elif(prefix == "kb"):
            return str(round(totBytes/ByteConversion.KB, precisionDecimals)) + " KB"
        elif(prefix == "mb"):
            return str(round(totBytes/ByteConversion.MB, precisionDecimals)) + " MB"
        elif(prefix == "gb"):
            return str(round(totBytes/ByteConversion.GB, precisionDecimals)) + " GB"
        else:
            raise Exception("Incorrect prefix!")

class TimeConversion:
    def __init__(self):
        return
        
    @staticmethod
    def DaysToSec(days):
        return TimeConversion.HoursToSec(24*days)

    @staticmethod
    def HoursToSec(hours):
        return TimeConversion.MinutesToSec(60*hours)
        
    @staticmethod
    def MinutesToSec(minutes):
        return minutes*60