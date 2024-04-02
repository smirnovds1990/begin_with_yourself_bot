from datetime import datetime as dt


async def compile_registration_data(data: dict) -> dict:
    data['height'] = int(data['height'])
    data['current_weight'] = float(data['current_weight'])
    data['birth_date'] = dt.strptime(data['birth_date'], '%d.%m.%Y')
    return data
