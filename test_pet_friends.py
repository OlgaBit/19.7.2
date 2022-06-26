from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
   # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
   # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

# Тест на добавление питомца без фото
def test_add_new_pet_not_photo(name='Анфиса', animal_type='кошка', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Запрашиваем ключ api и сохраняем в переменную auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)  # Добавляем питомца без фото
    assert status == 200
    assert result['name'] == name

def test_successful_update_self_pet_info(name='Мура', animal_type='Кошка', age=2):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    ''' Если список не пустой, то пробуем обновить его имя, тип и возраст'''
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        ''' Проверяем что статус ответа = 200 и имя питомца соответствует заданному'''
        assert status == 200
        assert result['name'] == name
    else:
        ''' Если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев'''
        raise Exception("There is no my pets")

# Тест на удаление питомца
def test_successful_delete_self_pet():
    '''Получаем ключ auth_key и запрашиваем список своих питомцев'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    ''' Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев'''
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Анфиса", "кошка", "3", "images/cat3.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


""" 10 дополнительных тестов"""

# Тест на передачу неверного пароля"""
def test_get_api_key_for_NOTvalid_password(email=valid_email, password="12345"):
    '''Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result'''
    status, result = pf.get_api_key(email, password)
    print(password)

    assert status == 403
    assert 'key' is not result

#  Тест на пустой пароль
def test_get_api_key_for_not_password(email= valid_email, password=''):
    '''Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result'''
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# Тест на пустой email
def test_get_api_key_for_not_email(email='', password=valid_password):
    '''Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result'''
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# Тест на ввод некорректных данных
def test_get_api_key_for_not_valid_user(email='12345', password='*/*/*'):
    '''Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print(status, result)

# Тест на добавление питомца с отрицательным возростом
def test_add_new_pet_not_photo_invalid_age(name ='Кроха', animal_type = 'кошка', age= -5):
    ''' Запрашиваем ключ api и сохраняем в переменную auth_key'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)
    assert status == 403

# Тест на добавление питомца с пустым полем 'name'
def test_add_new_pet_without_name(name="", animal_type="крот", age=1):
    ''' Запрашиваем ключ api и сохраняем в переменную auth_key'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    assert status == 400

# Тест на добавление питомца с пустым полем 'animal_type'
def test_add_new_pet_not_animal_type(name="Жучка", animal_type="", age=5):
    ''' Запрашиваем ключ api и сохраняем в переменную auth_key'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    assert status == 400

# Тест на обновление данных несуществующего питомца
def test_successful_update_self_not_pet_info(name='Боря', animal_type='поросенок', age=1):
    ''' Получаем ключ auth_key и список своих питомцев'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    ''' Если список не пустой, то пробуем обновить его имя, тип и возраст'''
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    '''Проверяем что обновление данных приводит к ошибке '''
    assert status == 403

# Тест на проверку получения списка только своих питомцев
def test_get_list_of_my_pets_corrected():
    '''Получаем ключ auth_key и запрашиваем список своих питомцев'''
    filter = "my_pets"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, results = pf.get_list_of_pets(auth_key=auth_key, filter=filter)

    assert status == 200
    count_pets = len(results['pets'])

    if count_pets != 0:
        print(f"my Pets = {len(results['pets'])}")
        print(results['pets'][0].keys())
    else:
        raise Exception("There is no my pets")

# Тест на удаление всех  своих питомцев
def test_on_delete_all_pets():
    '''Получаем ключ auth_key и запрашиваем список своих питомцев'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    ''' Проверяем - если список пустой, то добавляем нового питомца и опять запрашиваем список своих питомцев'''
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, '', "крот", "1", r'../images/Cat2.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    ''' Получаем в цикле id всех питомцев из списка и отправляем запрос на удаление'''
    for id_pet in my_pets["pets"]:
        pf.delete_pet(auth_key, id_pet["id"])
        ''' Опять запрашиваем список своих питомцев'''
        status, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    '''Проверяем что статус ответаравен 200 и в списке питомцев нет id удалённого питомца'''
    assert status == 200
    assert pet_id not in my_pets.values()
