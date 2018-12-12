
def IntradayBarNumber(bars):
    result = []
    if len(bars.timestamp) == 0:
        return result
    ibn = 0
    current_date = None
    for ts in bars.timestamp:
        if current_date != ts.date():
            ibn = 0
            current_date = ts.date()
        else:
            ibn += 1
        result.append(ibn)

    return result


