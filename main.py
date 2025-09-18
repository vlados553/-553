import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import hashlib
import re
from datetime import datetime

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Усовершенствованная система авторизации")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Стилизация
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        # Подключение к БД
        self.db_connection = sqlite3.connect('users.db', check_same_thread=False)
        self.create_tables()
        
        # Текущий пользователь
        self.current_user = None
        
        self.show_login_frame()
    
    def create_tables(self):
        cursor = self.db_connection.cursor()
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        # Таблица записей пользователя
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.db_connection.commit()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_email(self, email):
        if not email:  # Пустой email допустим
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_frame(self):
        self.clear_window()
        self.current_user = None
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=50, padx=50, fill=tk.BOTH, expand=True)
        
        header = ttk.Label(main_frame, text="Вход в систему", style='Header.TLabel')
        header.pack(pady=20)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Логин или email:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.login_username = ttk.Entry(form_frame, width=30)
        self.login_username.grid(row=0, column=1, padx=5, pady=5)
        self.login_username.bind('<Return>', lambda e: self.login())
        
        ttk.Label(form_frame, text="Пароль:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.login_password = ttk.Entry(form_frame, width=30, show="*")
        self.login_password.grid(row=1, column=1, padx=5, pady=5)
        self.login_password.bind('<Return>', lambda e: self.login())
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Войти", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Регистрация", command=self.show_register_frame).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Забыли пароль?", command=self.show_password_recovery).pack(side=tk.LEFT, padx=5)
    
    def show_register_frame(self):
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=30, padx=50, fill=tk.BOTH, expand=True)
        
        header = ttk.Label(main_frame, text="Регистрация", style='Header.TLabel')
        header.pack(pady=10)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Логин*:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.register_username = ttk.Entry(form_frame, width=30)
        self.register_username.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.register_email = ttk.Entry(form_frame, width=30)
        self.register_email.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Пароль*:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.register_password = ttk.Entry(form_frame, width=30, show="*")
        self.register_password.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Повторите пароль*:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.register_confirm = ttk.Entry(form_frame, width=30, show="*")
        self.register_confirm.grid(row=3, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Зарегистрироваться", command=self.register).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Назад", command=self.show_login_frame).pack(side=tk.LEFT, padx=5)
    
    def show_password_recovery(self):
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=50, padx=50, fill=tk.BOTH, expand=True)
        
        header = ttk.Label(main_frame, text="Восстановление пароля", style='Header.TLabel')
        header.pack(pady=20)
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.recovery_email = ttk.Entry(form_frame, width=30)
        self.recovery_email.grid(row=0, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Восстановить", command=self.recover_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Назад", command=self.show_login_frame).pack(side=tk.LEFT, padx=5)
    
    def show_main_app(self):
        self.clear_window()
        
        # Создаем меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        user_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Пользователь", menu=user_menu)
        user_menu.add_command(label="Профиль", command=self.show_profile)
        user_menu.add_separator()
        user_menu.add_command(label="Выйти", command=self.show_login_frame)
        
        notes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Заметки", menu=notes_menu)
        notes_menu.add_command(label="Мои заметки", command=self.show_notes)
        notes_menu.add_command(label="Добавить заметку", command=self.show_add_note)
        
        # Основной интерфейс
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        welcome_text = f"Добро пожаловать, {self.current_user[1]}!"
        header = ttk.Label(main_frame, text=welcome_text, style='Header.TLabel')
        header.pack(pady=10)
        
        # Статистика
        stats_frame = ttk.LabelFrame(main_frame, text="Статистика")
        stats_frame.pack(pady=10, fill=tk.X, padx=10)
        
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_notes WHERE user_id = ?", (self.current_user[0],))
        notes_count = cursor.fetchone()[0]
        
        ttk.Label(stats_frame, text=f"Количество заметок: {notes_count}").pack(pady=5)
        ttk.Label(stats_frame, text=f"Дата регистрации: {self.current_user[4]}").pack(pady=5)
        if self.current_user[5]:
            ttk.Label(stats_frame, text=f"Последний вход: {self.current_user[5]}").pack(pady=5)
        
        # Последние заметки
        notes_frame = ttk.LabelFrame(main_frame, text="Последние заметки")
        notes_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)
        
        cursor.execute("SELECT title, created_at FROM user_notes WHERE user_id = ? ORDER BY created_at DESC LIMIT 5", (self.current_user[0],))
        recent_notes = cursor.fetchall()
        
        if recent_notes:
            for note in recent_notes:
                note_text = f"{note[0]} - {note[1]}"
                ttk.Label(notes_frame, text=note_text).pack(pady=2, anchor=tk.W)
        else:
            ttk.Label(notes_frame, text="У вас пока нет заметок").pack(pady=10)
        
        ttk.Button(main_frame, text="Управление заметками", command=self.show_notes).pack(pady=10)
    
    def show_profile(self):
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=30, padx=50, fill=tk.BOTH, expand=True)
        
        header = ttk.Label(main_frame, text="Профиль пользователя", style='Header.TLabel')
        header.pack(pady=10)
        
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(pady=10)
        
        ttk.Label(info_frame, text="Логин:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(info_frame, text=self.current_user[1]).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(info_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(info_frame, text=self.current_user[3] or "Не указан").grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(info_frame, text="Дата регистрации:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(info_frame, text=self.current_user[4]).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        if self.current_user[5]:
            ttk.Label(info_frame, text="Последний вход:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
            ttk.Label(info_frame, text=self.current_user[5]).grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Назад", command=self.show_main_app).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Сменить пароль", command=self.show_change_password).pack(side=tk.LEFT, padx=5)
    
    def show_change_password(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Смена пароля")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Текущий пароль:").pack(pady=5)
        current_password = ttk.Entry(dialog, show="*", width=30)
        current_password.pack(pady=5)
        
        ttk.Label(dialog, text="Новый пароль:").pack(pady=5)
        new_password = ttk.Entry(dialog, show="*", width=30)
        new_password.pack(pady=5)
        
        ttk.Label(dialog, text="Повторите новый пароль:").pack(pady=5)
        confirm_password = ttk.Entry(dialog, show="*", width=30)
        confirm_password.pack(pady=5)
        
        def change_pass():
            current = current_password.get()
            new = new_password.get()
            confirm = confirm_password.get()
            
            if not current or not new or not confirm:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            if new != confirm:
                messagebox.showerror("Ошибка", "Новые пароли не совпадают")
                return
            
            hashed_current = self.hash_password(current)
            if hashed_current != self.current_user[2]:
                messagebox.showerror("Ошибка", "Текущий пароль неверен")
                return
            
            hashed_new = self.hash_password(new)
            cursor = self.db_connection.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_new, self.current_user[0]))
            self.db_connection.commit()
            
            messagebox.showinfo("Успех", "Пароль успешно изменен")
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Сменить пароль", command=change_pass).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_notes(self):
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        header = ttk.Label(main_frame, text="Мои заметки", style='Header.TLabel')
        header.pack(pady=10)
        
        # Панель управления
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=5, fill=tk.X)
        
        ttk.Button(control_frame, text="Добавить заметку", command=self.show_add_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Назад", command=self.show_main_app).pack(side=tk.LEFT, padx=5)
        
        # Список заметок
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Создаем Treeview для отображения заметок
        columns = ("id", "title", "created", "updated")
        self.notes_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        self.notes_tree.heading("id", text="ID")
        self.notes_tree.heading("title", text="Заголовок")
        self.notes_tree.heading("created", text="Создана")
        self.notes_tree.heading("updated", text="Обновлена")
        
        self.notes_tree.column("id", width=50)
        self.notes_tree.column("title", width=200)
        self.notes_tree.column("created", width=120)
        self.notes_tree.column("updated", width=120)
        
        # Scrollbar для Treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.notes_tree.yview)
        self.notes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.notes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопки управления заметками
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=10)
        
        ttk.Button(action_frame, text="Просмотреть", command=self.view_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Редактировать", command=self.edit_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Удалить", command=self.delete_note).pack(side=tk.LEFT, padx=5)
        
        # Загружаем заметки
        self.load_notes()
    
    def load_notes(self):
        # Очищаем текущий список
        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)
        
        # Загружаем заметки из БД
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, title, created_at, updated_at FROM user_notes WHERE user_id = ? ORDER BY updated_at DESC", (self.current_user[0],))
        notes = cursor.fetchall()
        
        for note in notes:
            self.notes_tree.insert("", tk.END, values=note)
    
    def show_add_note(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить заметку")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Заголовок:").pack(pady=5, padx=10, anchor=tk.W)
        title_entry = ttk.Entry(dialog, width=50)
        title_entry.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Label(dialog, text="Содержание:").pack(pady=5, padx=10, anchor=tk.W)
        content_text = scrolledtext.ScrolledText(dialog, width=60, height=15)
        content_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        def save_note():
            title = title_entry.get()
            content = content_text.get("1.0", tk.END).strip()
            
            if not title:
                messagebox.showerror("Ошибка", "Заголовок не может быть пустым")
                return
            
            cursor = self.db_connection.cursor()
            cursor.execute("INSERT INTO user_notes (user_id, title, content) VALUES (?, ?, ?)", 
                          (self.current_user[0], title, content))
            self.db_connection.commit()
            
            messagebox.showinfo("Успех", "Заметка успешно добавлена")
            dialog.destroy()
            self.load_notes()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Сохранить", command=save_note).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def view_note(self):
        selected = self.notes_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заметку для просмотра")
            return
        
        item = self.notes_tree.item(selected[0])
        note_id = item['values'][0]
        
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT title, content, created_at, updated_at FROM user_notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Просмотр заметки")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=note[0], style='Header.TLabel').pack(pady=10)
        
        info_frame = ttk.Frame(dialog)
        info_frame.pack(pady=5, fill=tk.X, padx=10)
        
        ttk.Label(info_frame, text=f"Создана: {note[2]}").pack(side=tk.LEFT)
        ttk.Label(info_frame, text=f"Обновлена: {note[3]}").pack(side=tk.RIGHT)
        
        content_frame = ttk.Frame(dialog)
        content_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        content_text = scrolledtext.ScrolledText(content_frame, width=60, height=15)
        content_text.insert("1.0", note[1])
        content_text.config(state=tk.DISABLED)
        content_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(dialog, text="Закрыть", command=dialog.destroy).pack(pady=10)
    
    def edit_note(self):
        selected = self.notes_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заметку для редактирования")
            return
        
        item = self.notes_tree.item(selected[0])
        note_id = item['values'][0]
        
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT title, content FROM user_notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать заметку")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Заголовок:").pack(pady=5, padx=10, anchor=tk.W)
        title_entry = ttk.Entry(dialog, width=50)
        title_entry.insert(0, note[0])
        title_entry.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Label(dialog, text="Содержание:").pack(pady=5, padx=10, anchor=tk.W)
        content_text = scrolledtext.ScrolledText(dialog, width=60, height=15)
        content_text.insert("1.0", note[1])
        content_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        def save_changes():
            title = title_entry.get()
            content = content_text.get("1.0", tk.END).strip()
            
            if not title:
                messagebox.showerror("Ошибка", "Заголовок не может быть пустым")
                return
            
            cursor.execute("UPDATE user_notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", 
                          (title, content, note_id))
            self.db_connection.commit()
            
            messagebox.showinfo("Успех", "Заметка успешно обновлена")
            dialog.destroy()
            self.load_notes()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Сохранить", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def delete_note(self):
        selected = self.notes_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заметку для удаления")
            return
        
        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранную заметку?"):
            return
        
        item = self.notes_tree.item(selected[0])
        note_id = item['values'][0]
        
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM user_notes WHERE id = ?", (note_id,))
        self.db_connection.commit()
        
        messagebox.showinfo("Успех", "Заметка успешно удалена")
        self.load_notes()
    
    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        hashed_password = self.hash_password(password)
        
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE (username = ? OR email = ?) AND password = ?", 
                      (username, username, hashed_password))
        user = cursor.fetchone()
        
        if user:
            # Обновляем время последнего входа
            cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user[0],))
            self.db_connection.commit()
            
            self.current_user = user
            messagebox.showinfo("Успех", "Авторизация прошла успешно!")
            self.show_main_app()
        else:
            messagebox.showerror("Ошибка", "Неверный логин/email или пароль")
    
    def register(self):
        username = self.register_username.get().strip()
        email = self.register_email.get().strip()
        password = self.register_password.get()
        confirm = self.register_confirm.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Поля с * обязательны для заполнения")
            return
        
        if len(username) < 3:
            messagebox.showerror("Ошибка", "Логин должен содержать至少 3 символа")
            return
        
        if len(password) < 4:
            messagebox.showerror("Ошибка", "Пароль должен содержать至少 4 символа")
            return
        
        if password != confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return
        
        if email and not self.validate_email(email):
            messagebox.showerror("Ошибка", "Некорректный email")
            return
        
        hashed_password = self.hash_password(password)
        
        try:
            cursor = self.db_connection.cursor()
            if email:
                cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                              (username, hashed_password, email))
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                              (username, hashed_password))
            self.db_connection.commit()
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            self.show_login_frame()
        except sqlite3.IntegrityError as e:
            error_msg = str(e)
            if "UNIQUE constraint failed: users.username" in error_msg:
                messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует")
            elif "UNIQUE constraint failed: users.email" in error_msg:
                messagebox.showerror("Ошибка", "Пользователь с таким email уже существует")
            else:
                messagebox.showerror("Ошибка", f"Ошибка при регистрации: {error_msg}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка: {str(e)}")
    
    def recover_password(self):
        email = self.recovery_email.get().strip()
        
        if not email:
            messagebox.showerror("Ошибка", "Введите email")
            return
        
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT username FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            messagebox.showinfo("Успех", f"Инструкции по восстановлению пароля отправлены на {email}\n\n(В реальном приложении здесь была бы отправка email)")
        else:
            messagebox.showerror("Ошибка", "Пользователь с таким email не найден")
    
    def __del__(self):
        if hasattr(self, 'db_connection'):
            self.db_connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthApp(root)
    root.mainloop()