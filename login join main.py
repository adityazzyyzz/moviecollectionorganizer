import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import mysql.connector
import csv
import os

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1350x700')
        self.root.title("Login - Movie Collection Organizer")
        self.root.resizable(False, False)

        self.setup_login_ui()

    def setup_login_ui(self):
        # Path to background image
        bg_image_path = 'C:/Users/krris/Downloads/images/login_3.jpg'

        # Check if the image exists
        if not os.path.isfile(bg_image_path):
            messagebox.showerror('Error', 'Background image file not found!')
            self.root.destroy()
            return

        # Set background image and resize it to fit the window
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((1350, 700), Image.LANCZOS)
        self.bgimg = ImageTk.PhotoImage(bg_image)
        bg = tk.Label(self.root, image=self.bgimg)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame for login with transparency
        logframe = tk.Frame(self.root, bg='white', padx=20, pady=20, bd=7, relief=tk.RIDGE)
        logframe.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Add title with bold font
        title = tk.Label(logframe, text='Movie Collection Organizer', font=('Helvetica', 20, 'bold'), bg='white', fg='#333')
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Add username label and entry
        uname_label = tk.Label(logframe, text='Username:', font=('Helvetica', 14), bg='white', fg='#333')
        uname_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.unameE = tk.Entry(logframe, font=('Helvetica', 14), bd=2, relief=tk.SOLID)
        self.unameE.grid(row=1, column=1, padx=5, pady=5)

        # Add password label and entry
        pass_label = tk.Label(logframe, text='Password:', font=('Helvetica', 14), bg='white', fg='#333')
        pass_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.upassE = tk.Entry(logframe, show='*', font=('Helvetica', 14), bd=2, relief=tk.SOLID)
        self.upassE.grid(row=2, column=1, padx=5, pady=5)

        # Add login button with hover effect
        login_btn = tk.Button(logframe, text='Login', font=('Helvetica', 14, 'bold'), bg='white', fg='#333', bd=3, relief=tk.RIDGE, command=self.logfun)
        login_btn.grid(row=3, column=0, columnspan=2, pady=10)

        login_btn.bind("<Enter>", self.on_enter)
        login_btn.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        e.widget['background'] = '#333'
        e.widget['foreground'] = 'white'

    def on_leave(self, e):
        e.widget['background'] = 'white'
        e.widget['foreground'] = '#333'

    def logfun(self):
        username = self.unameE.get()
        password = self.upassE.get()
        
        if username == '' or password == '':
            messagebox.showerror('Error', 'Please Enter User Name and Password!')
        elif username == 'mahesh' and password == 'mahesh123':
            messagebox.showinfo('Success', f'Welcome {username} to the Movie Collection Organizer!')
            self.root.withdraw()  # Hide the login window
            main_window = tk.Toplevel(self.root)
            MovieCollectionOrganizer(main_window, username)
        else:
            messagebox.showerror('Failure', 'Invalid User Name or Password!')

class MovieCollectionOrganizer:
    def __init__(self, root, username):
        self.root = root
        self.root.geometry('1280x720+0+0')
        self.root.title('Movie Collection Organizer')
        self.root.resizable(False, False)
        self.username = username

        self.connect_db()
        self.setup_ui()

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='krrish13@KAU',
                database='movie_collection_organiser'
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            messagebox.showerror('Database Error', f'Error connecting to the database: {e}')

    def setup_ui(self):
        # Background Image
        background_image_path = 'C:/Users/krris/Downloads/images/mainpage_bg.jpg'
        background_image = Image.open(background_image_path)
        background_image = background_image.resize((1280, 720), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(background_image)
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome Label
        tk.Label(self.root, text=f'Welcome, {self.username}!', font=('Arial', 20, 'bold'), fg='white', bg='#E22529').pack(pady=4)

        # Menu Frame
        menu_frame = tk.Frame(self.root, bg='lightblue')
        menu_frame.pack(fill=tk.X, padx=10, pady=20)

        button_width = 20
        button_height = 2
        
        tk.Button(menu_frame, text='Add Movie', command=self.add_movie, width=button_width, height=button_height).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Update Movie', command=self.update_movie, width=button_width, height=button_height).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Delete Movie', command=self.delete_movie, width=button_width, height=button_height).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Export Movies', command=self.export_movies, width=button_width, height=button_height).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Logout', command=self.logout, width=button_width, height=button_height).pack(side=tk.RIGHT, padx=10)

        # Search Frame
        search_frame = tk.Frame(self.root, bg='lightblue')
        search_frame.pack(fill=tk.X, padx=10, pady=1)

        tk.Label(search_frame, text='Search:', bg='lightblue').pack(side=tk.LEFT, padx=10)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=10)
        tk.Button(search_frame, text='Search', command=self.search_movies, width=button_width, height=button_height).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text='Show All Movies', command=self.show_movies, width=button_width, height=button_height).pack(side=tk.LEFT, padx=5)

        # Movie List Frame
        list_frame = tk.Frame(self.root)
        list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(list_frame, columns=('movie_id', 'title', 'genre', 'director', 'release_year', 'duration', 'rating'), show='headings')
        self.tree.heading('movie_id', text='ID')
        self.tree.heading('title', text='Title')
        self.tree.heading('genre', text='Genre')
        self.tree.heading('director', text='Director')
        self.tree.heading('release_year', text='Year')
        self.tree.heading('duration', text='Duration')
        self.tree.heading('rating', text='Rating')

        self.tree.column('movie_id', width=50)
        self.tree.column('title', width=200)
        self.tree.column('genre', width=100)
        self.tree.column('director', width=150)
        self.tree.column('release_year', width=70)
        self.tree.column('duration', width=70)
        self.tree.column('rating', width=70)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.show_movies()

    def show_movies(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("SELECT * FROM movies")
        for row in self.cur.fetchall():
            self.tree.insert('', tk.END, values=row)

    def add_movie(self):
        add_window = tk.Toplevel(self.root)
        add_window.title('Add Movie')
        
        fields = ['Title', 'Genre', 'Director', 'Release Year', 'Duration', 'Rating']
        entries = {}
        
        for field in fields:
            tk.Label(add_window, text=field).pack()
            entries[field] = tk.Entry(add_window)
            entries[field].pack()
        
        def save():
            values = [entries[field].get() for field in fields]
            try:
                self.cur.execute("INSERT INTO movies (title, genre, director, release_year, duration, rating) VALUES (%s, %s, %s, %s, %s, %s)", values)
                self.conn.commit()
                messagebox.showinfo('Success', 'Movie added successfully!')
                add_window.destroy()
                self.show_movies()
            except Exception as e:
                messagebox.showerror('Error', f'Failed to add movie: {e}')
        
        tk.Button(add_window, text='Save', command=save).pack()

    def update_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Please select a movie to update')
            return
        
        movie = self.tree.item(selected[0])['values']
        update_window = tk.Toplevel(self.root)
        update_window.title('Update Movie')
        
        fields = ['Title', 'Genre', 'Director', 'Release Year', 'Duration', 'Rating']
        entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(update_window, text=field).pack()
            entries[field] = tk.Entry(update_window)
            entries[field].insert(0, movie[i+1])
            entries[field].pack()
        
        def save():
            values = [entries[field].get() for field in fields]
            values.append(movie[0])  # Append movie_id
            try:
                self.cur.execute("UPDATE movies SET title=%s, genre=%s, director=%s, release_year=%s, duration=%s, rating=%s WHERE movie_id=%s", values)
                self.conn.commit()
                messagebox.showinfo('Success', 'Movie updated successfully!')
                update_window.destroy()
                self.show_movies()
            except Exception as e:
                messagebox.showerror('Error', f'Failed to update movie: {e}')
        
        tk.Button(update_window, text='Save', command=save).pack()

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Please select a movie to delete')
            return
        
        if messagebox.askyesno('Confirm', 'Are you sure you want to delete this movie?'):
            movie_id = self.tree.item(selected[0])['values'][0]
            try:
                self.cur.execute("DELETE FROM movies WHERE movie_id=%s", (movie_id,))
                self.conn.commit()
                messagebox.showinfo('Success', 'Movie deleted successfully!')
                self.show_movies()
            except Exception as e:
                messagebox.showerror('Error', f'Failed to delete movie: {e}')

    def search_movies(self):
        search_term = self.search_var.get()

        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return

        self.tree.delete(*self.tree.get_children())

        try:
            query = """
                SELECT * FROM movies 
                WHERE 
                    movie_id LIKE %s OR
                    title LIKE %s OR
                    genre LIKE %s OR
                    director LIKE %s OR
                    release_year LIKE %s OR
                    rating LIKE %s
            """
            search_pattern = f"%{search_term}%"
            self.cur.execute(query, (search_pattern,) * 6)
            rows = self.cur.fetchall()

            for row in rows:
                self.tree.insert('', tk.END, values=row)

        except Exception as e:
            messagebox.showerror('Error', f'Failed to search movies: {e}')

    def export_movies(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not filename:
                return

            self.cur.execute("SELECT * FROM movies")
            rows = self.cur.fetchall()

            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Title', 'Genre', 'Director', 'Release Year', 'Duration', 'Rating'])
                writer.writerows(rows)
            messagebox.showinfo('Success', 'Movies exported successfully!')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to export movies: {e}')

    def logout(self):
        self.cur.close()
        self.conn.close()
        self.root.destroy()
        login_window.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    login_window = root
    root.mainloop()