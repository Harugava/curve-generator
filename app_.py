from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import base64
import os

app = Flask(__name__)

# Функция для генерации трохоиды
def generate_trochoid(R, h, num_points=200):
    t = np.linspace(0, 8 * np.pi, num_points)
    x = R * t - h * np.sin(t)
    y = R - h * np.cos(t)
    return x, y

# Функция для генерации эпициклоиды
def generate_epicycloid(r, k, num_points=200):
    t = np.linspace(0, 2 * np.pi, num_points)
    x = r * (k + 1) * (np.cos(t) - np.cos((k + 1) * t) / (k + 1))
    y = r * (k + 1) * (np.sin(t) - np.sin((k + 1) * t) / (k + 1))
    return x, y

@app.route("/", methods=["GET", "POST"])
def index():
    graph_html = None
    selected_curve = "trochoid"  # Значение по умолчанию
    if request.method == "POST":
        selected_curve = request.form.get("shape", "trochoid")
        try:
            if selected_curve == "trochoid":
                R = float(request.form.get("R", 1))
                h = float(request.form.get("h", 1))
                x, y = generate_trochoid(R, h)
                title = "Trochoid"
                # Создание графика
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.set_xlim(min(x) - 2 * R, max(x) + 2 * R)
                ax.set_ylim(min(y) - 8 * R, max(y) + 8 * R)
                ax.set_xlabel("x", fontsize=14)
                ax.set_ylabel("y", fontsize=14)
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
                ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
                ax.tick_params(axis='both', which='major', labelsize=12)
                ax.set_aspect('equal')
            elif selected_curve == "epicycloid":
                r = float(request.form.get("r", 1))
                k = float(request.form.get("k", 1))
                x, y = generate_epicycloid(r, k)
                title = "Epicycloid"
                # Создание графика
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.set_xlim(min(x) - 8 * r, max(x) + 8 * r)
                ax.set_ylim(min(y) - 8 * r, max(y) + 8 * r)
                ax.set_xlabel("x", fontsize=14)
                ax.set_ylabel("y", fontsize=14)
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
                ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
                ax.tick_params(axis='both', which='major', labelsize=12)
                ax.set_aspect('equal')
            else:
                raise ValueError("Invalid curve type")


            # Линия для анимации
            line, = ax.plot([], [], lw=3, color='blue')
            ax.grid(True)

            # Сохранение графика как GIF
            gif_path = "curve_animation.gif"
            ani = FuncAnimation(fig, lambda frame: ax.plot(x[:frame], y[:frame], color='blue'), frames=len(x), interval=30)
            ani.save(gif_path, writer=PillowWriter(fps=120))

            # Чтение GIF и конвертация в base64
            with open(gif_path, "rb") as f:
                gif_data = f.read()
            graph_html = base64.b64encode(gif_data).decode("utf-8")

            # Удаление временного файла
            os.remove(gif_path)
        except Exception as e:
            graph_html = f"<p style='color: red;'>Ошибка: {e}</p>"

    return render_template("index.html", graph_html=graph_html, selected_curve=selected_curve)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
