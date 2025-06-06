from contextlib import contextmanager
import requests
from requests.exceptions import HTTPError

@contextmanager
def check_status_code_http(
    expected_status_code: int = requests.codes.ok,
    expected_message: str = ''
):
    try:
        yield
        # Если ожидаем ошибку, но она не произошла
        if expected_status_code != requests.codes.ok:
            raise AssertionError(
                f'Ожидалась ошибка с кодом {expected_status_code}, но запрос завершился успешно'
            )
    except HTTPError as e:
        # Если произошла ошибка, но мы ожидали успех
        if expected_status_code == requests.codes.ok:
            raise AssertionError(
                f'Ожидался успешный ответ, но получена ошибка: {e.response.status_code} - {e.response.text}'
            )
        # Проверка кода ошибки
        assert e.response.status_code == expected_status_code, \
            f'Ожидался статус {expected_status_code}, получен {e.response.status_code}'
        # Проверка сообщения
        if expected_message:
            actual_message = e.response.json().get('title', '')
            assert actual_message == expected_message, \
                f'Ожидалось сообщение "{expected_message}", получено "{actual_message}"'
# @contextmanager
# def check_status_code_http(
#         expected_status_code: requests.codes = requests.codes.OK,
#         expected_message: str = ''
#         ):
#     try:
#         yield
#         if expected_status_code != requests.codes.OK:
#             raise AssertionError(f'Ожидаемый статус код должен быть равен {expected_status_code}')
#         if expected_status_code != requests.codes.OK:
#             raise AssertionError(f'Должно быть получено сообщение "{expected_message}", но запрос прошел успешно')
#     except HTTPError as e:
#         assert e.response.status_code == expected_status_code
#         assert e.response.json()['title'] == expected_message
