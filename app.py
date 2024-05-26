from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def calculate_roots():
    try:
        # Попытка получения и преобразования данных
        a = float(request.form.get('a', 0))
        b = float(request.form.get('b', 0))
        c = float(request.form.get('c', 0))

        if a == 0:
            return render_template('result.html', error="Значение 'a' не может быть равно нулю.")

        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            roots = "Нет реальных корней"
        else:
            root1 = (-b + math.sqrt(discriminant)) / (2 * a)
            root2 = (-b - math.sqrt(discriminant)) / (2 * a)
            roots = f"Корень 1: {root1}, Корень 2: {root2}"

        return render_template('result.html', roots=roots)

    except ValueError:
        # Если не удалось преобразовать в число, отображаем сообщение об ошибке
        return render_template('result.html', error="Некорректный ввод. Пожалуйста, введите числа.")

@app.route('/reset', methods=['GET'])
def reset_form():
    # Функция для перезагрузки формы
    return render_template('index.html')

app.run(debug=True)

