from datetime import timedelta, datetime


def date_list(day: int = 30, start: str = 'today', fmt: str = '%Y-%m-%d', rev=False):
    """n日前までの日付文字列をlist化
    Args:
        day (int): 日数
        start: (str): 開始の日、例えば`2021-12-01`とすればこの日からn日前までのlistを返す
        fmt (str): strftimeで使われるformat
        rev (bool): 結果をriverseする(defalt=Falseでは正順)
    Returns:
        list: n日分の日付文字列

    Example:
        >>> date_list(3, '2020-12-1')
        ['2020-11-29', '2020-11-30', '2020-12-01']
        >>> date_list(3, '20201201', '%Y%m%d')
        ['20201129', '20201130', '20201201']
        >>> date_list(3, '2020-12-01', rev=True)
        ['2020-12-01', '2020-11-30', '2020-11-29']

    Note:
        https://docs.python.org/ja/3/library/datetime.html#strftime-strptime-behavior
    """
    d = datetime.now()
    if start != 'today':
        d = datetime.strptime(start, fmt)
    li = [d.strftime(fmt)]
    for _ in range(day - 1):
        d -= timedelta(days=1)
        li.append(d.strftime(fmt))
    if not rev:
        li.reverse()
    return li
