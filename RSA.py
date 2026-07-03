import math
import tkinter as tk
from tkinter import ttk, messagebox
import time


# ====================== RSA ЛОГИКА ======================
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def encrypt_message(text, e, n):
    return [pow(ord(char), e, n) for char in text]


def decrypt_message(encrypted, d, n):
    return "".join([chr(pow(char, d, n)) for char in encrypted])


# ====================== GUI ======================
def run_rsa():
    try:
        p = int(entry_p.get())
        q = int(entry_q.get())
        e = int(entry_e.get())
        msg = entry_msg.get().strip()

        if not msg:
            messagebox.showwarning("Внимание", "Введите сообщение!")
            return

        if not (is_prime(p) and is_prime(q)):
            messagebox.showerror("Ошибка", "P и Q должны быть простыми числами!")
            return

        n = p * q
        phi = (p - 1) * (q - 1)

        if math.gcd(e, phi) != 1:
            messagebox.showerror("Ошибка", f"e должно быть взаимно простым с φ = {phi}")
            return

        d = pow(e, -1, phi)

        # Анимация процесса
        status.config(text="🔄 Вычисление ключей...", fg="orange")
        root.update()
        time.sleep(0.5)

        encrypted = encrypt_message(msg, e, n)

        status.config(text="🔐 Шифрование...", fg="blue")
        root.update()
        time.sleep(0.4)

        # Анимация шифротекста
        entry_enc.delete(0, tk.END)
        enc_str = str(encrypted)
        for i in range(len(enc_str) + 1):
            entry_enc.delete(0, tk.END)
            entry_enc.insert(0, enc_str[:i])
            root.update()
            time.sleep(0.015)

        decrypted = decrypt_message(encrypted, d, n)

        # Анимация расшифровки
        status.config(text="🔓 Расшифровка...", fg="green")
        entry_dec.delete(0, tk.END)
        for i in range(len(decrypted) + 1):
            entry_dec.delete(0, tk.END)
            entry_dec.insert(0, decrypted[:i])
            root.update()
            time.sleep(0.025)

        # Результаты
        label_n.config(text=f"n = {n}")
        label_d.config(text=f"d = {d}")
        status.config(text="✅ Готово! Всё работает", fg="green")

    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте, что все поля заполнены числами!")
    except Exception as ex:
        messagebox.showerror("Ошибка", f"Что-то пошло не так:\n{ex}")


# ====================== ИНТЕРФЕЙС ======================
root = tk.Tk()
root.title("RSA Шифрование")
root.geometry("560x680")
root.configure(bg="#2c3e50")

# Стиль
style = ttk.Style()
style.theme_use('clam')

# Заголовок
title = tk.Label(root, text="🔒 RSA Учебный Шифратор",
                 font=("Arial", 18, "bold"), fg="#ecf0f1", bg="#2c3e50")
title.pack(pady=20)

# Основной фрейм
frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

# Поля ввода
ttk.Label(frame, text="P (простое число):").pack(anchor="w", pady=4)
entry_p = ttk.Entry(frame, font=("Arial", 11))
entry_p.pack(fill="x", pady=4)
entry_p.insert(0, "61")

ttk.Label(frame, text="Q (простое число):").pack(anchor="w", pady=4)
entry_q = ttk.Entry(frame, font=("Arial", 11))
entry_q.pack(fill="x", pady=4)
entry_q.insert(0, "53")

ttk.Label(frame, text="E (открытый экспонент):").pack(anchor="w", pady=4)
entry_e = ttk.Entry(frame, font=("Arial", 11))
entry_e.pack(fill="x", pady=4)
entry_e.insert(0, "17")

ttk.Label(frame, text="Сообщение:").pack(anchor="w", pady=(15, 4))
entry_msg = ttk.Entry(frame, font=("Arial", 11))
entry_msg.pack(fill="x", pady=4)
entry_msg.insert(0, "Привет от RSA!")

# Кнопка
btn = ttk.Button(frame, text="🔐 Зашифровать и Расшифровать", command=run_rsa)
btn.pack(pady=20)

# Статус
status = tk.Label(frame, text="Готов к работе", font=("Arial", 11), fg="#2ecc71", bg="#2c3e50")
status.pack(pady=8)

# Результаты
result_frame = ttk.LabelFrame(frame, text="Результат", padding=15)
result_frame.pack(fill="x", pady=10)

label_n = tk.Label(result_frame, text="n = ", font=("Courier", 12), bg="#34495e", fg="white")
label_n.pack(pady=5, fill="x")

label_d = tk.Label(result_frame, text="d = ", font=("Courier", 12), bg="#34495e", fg="white")
label_d.pack(pady=5, fill="x")

tk.Label(result_frame, text="Шифротекст:", bg="#2c3e50", fg="white").pack(anchor="w")
entry_enc = tk.Entry(result_frame, font=("Courier", 10), width=70, bg="#ecf0f1")
entry_enc.pack(pady=5)

tk.Label(result_frame, text="Расшифрованное сообщение:", bg="#2c3e50", fg="white").pack(anchor="w")
entry_dec = tk.Entry(result_frame, font=("Courier", 10), width=70, bg="#ecf0f1")
entry_dec.pack(pady=5)

root.mainloop()