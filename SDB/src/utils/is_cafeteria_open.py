import datetime
import jpholiday

def is_cafeteria_open(now: datetime.datetime = datetime.datetime.now()) -> bool:
    is_open = True
    day = now.weekday()
    hour = now.hour
    minute = now.minute
    if day == 5 or day == 6:
        is_open = False
    #祝日の場合も休み
    if jpholiday.is_holiday(now):
        is_open = False

    #平日の場合
    if hour < 8 or hour >= 20:
        is_open = False
    return is_open

# Unit Test
if __name__ == "__main__":
    assert is_cafeteria_open(datetime.datetime(2024, 5, 8, 12, 45)) == True
    assert is_cafeteria_open(datetime.datetime(2024, 5, 8, 7, 59)) == False
    assert is_cafeteria_open(datetime.datetime(2024, 5, 8, 20, 1)) == False
    assert is_cafeteria_open(datetime.datetime(2024, 5, 8, 12, 45)) == True
    assert is_cafeteria_open(datetime.datetime(2024, 7, 15, 15, 45)) == False

    print("All tests passed.")


    

    