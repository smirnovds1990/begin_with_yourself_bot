NAMES_PATTERN = r'[А-Яа-я]'
WIGHT_PATTERN = r'^[0-9]{2,3}?\.?[0-9]{0,2}$'
HEIGHT_PATTERN = r'^[0-9]{3,3}$'
DATE_PATTERN = r'^[0-9]{2}\.[0-9]{2}\.[1-2][0-9]{3}$'

MIN_LENGTH = 2
MAX_NAME_LENGTH = 25
MAX_HEIGHT_LENGTH = 3
MAX_WEIGHT_LENGTH = 5
DATE_LENGTH = 10

NOTIFICATIONS = (
    'ОЧЕНЬ ВАЖНО ЗАНИМАТЬСЯ!',
    'НУ ПРАВДА, ПОЗАНИМАЙСЯ УЖЕ!',
    'НЕ ЗАБЫВАЙ СПАТЬ!'
)
