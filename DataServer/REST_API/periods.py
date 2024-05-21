import logging
import calendar
import datetime
from .models import Period


def createPeriods(user, fromYear, toYear):
    log = logging.getLogger('utils')
    try:
        # check if period already exists
        firstPeriod = Period.objects.filter(year=fromYear, month=1, user=user)
        lastPeriod = Period.objects.filter(year=toYear, month=12, user=user)
        if firstPeriod and lastPeriod:
            return

        # create periods
        for year in range(fromYear, toYear + 1):
            for month in range(1, 13):
                quarter = ((month - 1) // 3) + 1
                fromDate = datetime.date(year, month, 1)
                _, lastDay = calendar.monthrange(year, month)
                toDate = datetime.date(year, month, lastDay)

                Period.objects.create(
                    user=user,
                    year=year,
                    month=month,
                    quarter=quarter,
                    fromDate=fromDate,
                    toDate=toDate)

    except Exception as e:
        self.log.error("UTILS ERROR [createPeriods]:", e)
