import logging
import sys
import os
from typing import Tuple, List

# ==================== НАСТРОЙКА ЛОГГЕРА ====================
os.makedirs("logs", exist_ok=True)

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")

# ==================== ОСНОВНАЯ ФУНКЦИЯ ====================
def calculate_triangle(side_a: str, side_b: str, side_c: str) -> Tuple[str, List[Tuple[int, int]]]:
    logging.info(f"Получены входные данные: A='{side_a}', B='{side_b}', C='{side_c}'")

    try:
        a = float(side_a)
        b = float(side_b)
        c = float(side_c)
    except ValueError:
        logging.error("Ошибка: входные данные не являются числами")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        logging.warning("Ошибка: стороны должны быть положительными числами")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a + b <= c or a + c <= b or b + c <= a:
        logging.warning("Ошибка: из данных сторон нельзя составить треугольник")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a == b == c:
        triangle_type = "равносторонний"
    elif a == b or a == c or b == c:
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    logging.info(f"Тип треугольника определён: {triangle_type}")

    max_side = max(a, b, c)
    scale = 80 / max_side

    x1, y1 = 10, 10
    x2 = int(10 + a * scale)
    y2 = 10

    cos_angle = (a**2 + b**2 - c**2) / (2 * a * b)
    cos_angle = max(min(cos_angle, 1.0), -1.0)
    height = b * (1 - cos_angle**2)**0.5

    x3 = int(10 + (b * cos_angle) * scale)
    y3 = int(10 + height * scale)

    x3 = max(0, min(x3, 100))
    y3 = max(0, min(y3, 100))
    x2 = max(0, min(x2, 100))

    coordinates = [(x1, y1), (x2, y2), (x3, y3)]
    logging.info(f"Координаты вершин: {coordinates}")

    return triangle_type, coordinates

# ==================== ТОЧКА ВХОДА ====================
def main():
    print("=== Программа определения типа треугольника ===")
    print("Введите длины трёх сторон (можно с точкой, например 3.5)")
    print("Для выхода введите 'exit'\n")

    while True:
        try:
            side_a = input("Сторона A: ").strip()
            if side_a.lower() == "exit":
                logging.info("Пользователь завершил программу")
                print("До свидания!")
                break

            side_b = input("Сторона B: ").strip()
            side_c = input("Сторона C: ").strip()

            result_type, coords = calculate_triangle(side_a, side_b, side_c)

            print("\n----- РЕЗУЛЬТАТ -----")
            print(f"Тип треугольника: '{result_type}'")
            print(f"Координаты вершин: {coords}")
            print("---------------------\n")

            if result_type:
                logging.info(f"Успешный запрос. Результат: {result_type}, координаты: {coords}")
            else:
                logging.error("Неуспешный запрос. Данные нечисловые.")

        except Exception as e:
            logging.exception("Произошла непредвиденная ошибка:")
            print("Произошла ошибка. Смотри логи.")

if __name__ == "__main__":
    main()