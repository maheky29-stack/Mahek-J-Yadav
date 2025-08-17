import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Movie"]
collection = db["Marvel"]

# CREATE
def create_record():
    movie_id = entry_id.get()
    title = entry_title.get()
    director = entry_director.get()
    year = entry_year.get()
    genre = entry_genre.get()

    if not (movie_id and title and director and year and genre):
        messagebox.showerror("Error", "All fields are required!")
        return

    if collection.find_one({"_id": movie_id}):
        messagebox.showerror("Error", "Record with this ID already exists!")
        return

    collection.insert_one({
        "_id": movie_id,
        "Title": title,
        "Director": director,
        "Year": year,
        "Genre": genre
    })
    messagebox.showinfo("Success", "Record created successfully!")
    clear_entries()
    read_records()

# READ
def read_records():
    listbox.delete(0, tk.END)
    for movie in collection.find():
        listbox.insert(tk.END, f"{movie['_id']} | {movie['Title']} | {movie['Director']} | {movie['Year']} | {movie['Genre']}")

# UPDATE
def update_record():
    movie_id = entry_id.get()
    if not movie_id:
        messagebox.showerror("Error", "ID is required to update!")
        return

    update_data = {}
    if entry_title.get():
        update_data["Title"] = entry_title.get()
    if entry_director.get():
        update_data["Director"] = entry_director.get()
    if entry_year.get():
        update_data["Year"] = entry_year.get()
    if entry_genre.get():
        update_data["Genre"] = entry_genre.get()

    if update_data:
        result = collection.update_one({"_id": movie_id}, {"$set": update_data})
        if result.matched_count:
            messagebox.showinfo("Success", "Record updated successfully!")
        else:
            messagebox.showerror("Error", "Record not found!")
    else:
        messagebox.showerror("Error", "No fields to update!")
    clear_entries()
    read_records()

# DELETE
def delete_record():
    movie_id = entry_id.get()
    if not movie_id:
        messagebox.showerror("Error", "ID is required to delete!")
        return

    result = collection.delete_one({"_id": movie_id})
    if result.deleted_count:
        messagebox.showinfo("Success", "Record deleted successfully!")
    else:
        messagebox.showerror("Error", "Record not found!")
    clear_entries()
    read_records()

# CLEAR FIELDS
def clear_entries():
    entry_id.delete(0, tk.END)
    entry_title.delete(0, tk.END)
    entry_director.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_genre.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("MongoDB CRUD - Marvel Movies")

# Labels and Entries
tk.Label(root, text="ID:").grid(row=0, column=0, sticky="e")
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Title:").grid(row=1, column=0, sticky="e")
entry_title = tk.Entry(root)
entry_title.grid(row=1, column=1)

tk.Label(root, text="Director:").grid(row=2, column=0, sticky="e")
entry_director = tk.Entry(root)
entry_director.grid(row=2, column=1)

tk.Label(root, text="Year:").grid(row=3, column=0, sticky="e")
entry_year = tk.Entry(root)
entry_year.grid(row=3, column=1)

tk.Label(root, text="Genre:").grid(row=4, column=0, sticky="e")
entry_genre = tk.Entry(root)
entry_genre.grid(row=4, column=1)

# Buttons
tk.Button(root, text="Create", command=create_record).grid(row=5, column=0, pady=5)
tk.Button(root, text="Read", command=read_records).grid(row=5, column=1)
tk.Button(root, text="Update", command=update_record).grid(row=6, column=0, pady=5)
tk.Button(root, text="Delete", command=delete_record).grid(row=6, column=1)
tk.Button(root, text="Clear", command=clear_entries).grid(row=7, column=0, columnspan=2)

# Listbox to display data
listbox = tk.Listbox(root, width=80)
listbox.grid(row=8, column=0, columnspan=2, pady=10)

read_records()  # Load existing records at startup

root.mainloop()
