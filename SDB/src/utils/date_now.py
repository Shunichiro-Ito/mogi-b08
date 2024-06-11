import datetime

def date_now() -> datetime.datetime:
    # 現在のUTC時刻を取得
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    # JSTタイムゾーンを定義
    jst = datetime.timezone(datetime.timedelta(hours=9), "JST")
    # JSTに変換
    jst_now = utc_now.astimezone(jst)
    return jst_now
