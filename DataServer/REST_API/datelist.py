import datetime
import calendar


def datelist(fromdate, todate):
    returnlist = []

    # check if dates are provided
    if fromdate and todate:
        # convert dates to datetime objects
        fromdate = datetime.datetime.strptime(fromdate, '%Y-%m-%d')
        todate = datetime.datetime.strptime(todate, '%Y-%m-%d')
        fromedate_monthID = fromdate.month + fromdate.year * 12
        todate_monthID = todate.month + todate.year * 12

        # invalid dates
        if todate < fromdate:
            return returnlist

        # same month case
        if todate_monthID == fromedate_monthID:
            returnlist.append(
                {'month-year': fromdate.strftime('%Y-%m'), 'datefrom': fromdate.strftime('%Y-%m-%d'), 'dateto': todate.strftime('%Y-%m-%d')})
            return returnlist

        # different month case
        cycles = 0
        for monthID in range(fromedate_monthID, todate_monthID):
            year = (monthID - 1) // 12
            month = (monthID - 1) % 12 + 1
            _, last_day = calendar.monthrange(year, month)

            if cycles == 0:
                returnlist.append(
                    {'month-year': fromdate.strftime('%Y-%m'), 'datefrom': fromdate.strftime('%Y-%m-%d'), 'dateto': datetime.datetime(year, month, last_day).strftime('%Y-%m-%d')})

            else:
                returnlist.append({'month-year': datetime.datetime(year, month, 1).strftime('%Y-%m'), 'datefrom': datetime.datetime(year, month, 1).strftime(
                    '%Y-%m-%d'), 'dateto': datetime.datetime(year, month, last_day).strftime('%Y-%m-%d')})

            cycles += 1

        # add last month
        returnlist.append({'month-year': todate.strftime('%Y-%m'), 'datefrom': datetime.datetime(todate.year, todate.month, 1).strftime(
            '%Y-%m-%d'), 'dateto': todate.strftime('%Y-%m-%d')})

    return returnlist
