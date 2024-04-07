async def compile_registration_data(data: dict) -> dict:
    '''
    Функция, обрабатывающая `data` из формы регистрации.
    '''
    data['height'] = int(data['height'])
    data['birth_year'] = int(data['birth_year'])
    return data
