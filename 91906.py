import tkinter as tk
from tkinter import ttk, messagebox
import json
import heapq
import os
from datetime import datetime


class LoginPopup:
    def __init__(self, parent, main_menu_ref):
        self.popup = tk.Toplevel(parent)
        self.popup.title("Login / Register")
        self.popup.geometry("380x300")
        self.popup.configure(bg="#e6e6e6")
        self.main_menu = main_menu_ref
        
        self.popup.grab_set()

        tk.Label(self.popup, text="Smart Kitchen Account", font=("Arial", 16, "bold"), bg="#e6e6e6", fg="black").pack(pady=15)

        input_frame = tk.Frame(self.popup, bg="#e6e6e6")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="ID:", bg="#e6e6e6", fg="black", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.id_entry = tk.Entry(input_frame, width=20, font=("Arial", 11))
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="PW:", bg="#e6e6e6", fg="black", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.pw_entry = tk.Entry(input_frame, width=20, font=("Arial", 11), show="*")
        self.pw_entry.grid(row=1, column=1, padx=5, pady=5)

        self.msg_label = tk.Label(self.popup, text="Enter the information and press button", bg="#e6e6e6", fg="black", font=("Arial", 9))
        self.msg_label.pack(pady=5)

        btn_frame = tk.Frame(self.popup, bg="#e6e6e6")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Login", width=10, bg="#5DADE2", fg="black", font=("Arial", 10, "bold"), command=self.action_login).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Join", width=10, bg="#58D68D", fg="black", font=("Arial", 10, "bold"), command=self.action_register).pack(side="left", padx=10)

    def action_login(self):
        username = self.id_entry.get().strip()
        password = self.pw_entry.get().strip()

        if not username or not password:
            self.msg_label.config(text="⚠️ Enter both ID and PW")
            return

        db = self.main_menu.users_db
        if username in db and db[username]["password"] == password:
            self.popup.grab_release()
            self.popup.destroy()
            self.main_menu.login_success(username, is_new_user=False)
        else:
            self.msg_label.config(text="❌ Incorrect ID or PW")

    def action_register(self):
        username = self.id_entry.get().strip()
        password = self.pw_entry.get().strip()

        if not username or not password:
            self.msg_label.config(text="⚠️ Enter joining ID or PW")
            return

        if username in self.main_menu.users_db:
            self.msg_label.config(text="❌ This ID already on.")
        else:
            self.main_menu.users_db[username] = {
                "password": password,
                "fridge_option": 1,
                "is_new": True 
            }
            self.main_menu.save_users()
            self.popup.grab_release()
            self.popup.destroy()
            self.main_menu.login_success(username, is_new_user=True)



class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Kitchen Management System")
        self.root.geometry("600x670")
        self.root.configure(bg="#e6e6e6")

        self.user_file = "users.json"
        self.food_file = "foods.json"
        self.current_user = None
        self.users_db = {}
        self.load_users()

        self.title_label = tk.Label(
            self.root, text="My Smart Kitchen", font=("Arial", 24, "bold"), bg="#e6e6e6", fg="black"
        )
        self.title_label.pack(pady=20)
        self.account_frame = tk.Frame(self.root, bg="#e6e6e6")
        self.account_frame.pack(fill="x", padx=40, pady=10)

        self.status_label = tk.Label(
            self.account_frame, text="🔒 Log Out Now. Login first to use service.", 
            fg="black", bg="#e6e6e6", font=("Arial", 10, "bold"), wraplength=500
        )
        self.status_label.pack(pady=5)

        self.acc_btn_frame = tk.Frame(self.account_frame, bg="#e6e6e6")
        self.acc_btn_frame.pack(pady=5)

        self.auth_btn = tk.Button(
            self.acc_btn_frame, text="Log in / Join", font=("Arial", 11, "bold"), 
            width=23, bg="#5DADE2", fg="black", command=self.open_auth_popup
        )
        self.auth_btn.pack(side="left", padx=5)

        self.delete_acc_btn = tk.Button(
            self.acc_btn_frame, text="Delete Account", font=("Arial", 11, "bold"),
            width=10, bg="#A6ACAF", fg="black", command=self.try_delete_account
        )

        self.option_frame = tk.LabelFrame(
            self.root, text=" Choose Fridge Shape ", font=("Arial", 11, "bold"),
            bg="#e6e6e6", fg="black", padx=20, pady=15
        )
        self.option_frame.pack(fill="x", padx=40, pady=10)

        self.fridge_option = tk.IntVar(value=1)
        self.backup_option = 1 

        self.r1 = tk.Radiobutton(self.option_frame, text="OPTION 1: 1 Big Frozen Storage and 1 small Refrigerated storage", variable=self.fridge_option, value=1, font=("Arial", 11), bg="#e6e6e6", fg="black", anchor="w", command=self.on_option_changed)
        self.r1.pack(fill="x", pady=2)
        self.r2 = tk.Radiobutton(self.option_frame, text="OPTION 2: Frozen / Refrigerated Half/Half (5:5)", variable=self.fridge_option, value=2, font=("Arial", 11), bg="#e6e6e6", fg="black", anchor="w", command=self.on_option_changed)
        self.r2.pack(fill="x", pady=2)
        self.r3 = tk.Radiobutton(self.option_frame, text="OPTION 3:  1 Small Frozen Storage and 2 Small Refrigerated storage", variable=self.fridge_option, value=3, font=("Arial", 11), bg="#e6e6e6", fg="black", anchor="w", command=self.on_option_changed)
        self.r3.pack(fill="x", pady=2)

        self.cancel_opt_btn = tk.Button(
            self.option_frame, text="✖ Cancel", font=("Arial", 10, "bold"),
            bg="#CD6155", fg="black", command=self.cancel_option_ui
        )

        self.fridge_btn_frame = tk.Frame(self.root, bg="#e6e6e6")
        self.fridge_btn_frame.pack(pady=20)

        self.change_opt_btn = tk.Button(
            self.root, text="🔧 Change the shape of Fridge?", font=("Arial", 11, "bold"), width=30, height=1,
            bg="#95A5A6", fg="black", relief="raised", command=self.show_option_ui_manually
        )

        self.fridge_btn = tk.Button(
            self.fridge_btn_frame, text="OPEN: Smart Fridge", font=("Arial", 14, "bold"), width=35, height=2,
            bg="#A9DFBF", fg="black", relief="raised", command=self.open_fridge
        )
        self.fridge_btn.pack()

    def load_users(self):
        if os.path.exists(self.user_file):
            try:
                with open(self.user_file, "r") as f:
                    self.users_db = json.load(f)
            except:
                self.users_db = {}
        else:
            self.users_db = {}

    def save_users(self):
        with open(self.user_file, "w") as f:
            json.dump(self.users_db, f, indent=4)

    def open_auth_popup(self):
        LoginPopup(self.root, self)

    def login_success(self, username, is_new_user=False):
        self.current_user = username
        user_data = self.users_db[username]
        
        saved_opt = user_data.get("fridge_option", 1)
        self.fridge_option.set(saved_opt)
        self.backup_option = saved_opt 
        
        is_truly_new = user_data.get("is_new", False) or is_new_user

        self.status_label.config(text=f"✔ {username} Welcome! You can use smart fridge.", fg="black")
        self.auth_btn.config(text="Logout", bg="#EC7063", command=self.try_logout)
        self.delete_acc_btn.pack(side="left", padx=5)
        
        if is_truly_new:
            self.change_opt_btn.pack_forget()
            self.cancel_opt_btn.pack_forget() 
            self.option_frame.pack(fill="x", padx=40, pady=10, before=self.fridge_btn_frame)
        else:
            self.option_frame.pack_forget()
            self.change_opt_btn.pack(pady=10, before=self.fridge_btn_frame)

    def try_logout(self):
        self.current_user = None
        self.status_label.config(text="🔒 Logout Now. Need login to use service.", fg="black")
        self.auth_btn.config(text="Login/New", bg="#5DADE2", command=self.open_auth_popup)
        
        self.delete_acc_btn.pack_forget()
        self.change_opt_btn.pack_forget()
        self.cancel_opt_btn.pack_forget()
        self.fridge_option.set(1)
        self.option_frame.pack(fill="x", padx=40, pady=10, before=self.fridge_btn_frame)

    def try_delete_account(self):
        if not self.current_user: return
        confirm = messagebox.askyesno("Delete_acc", f"Are you sure you want to delete the [{self.current_user}] account? \nDeleting the account will permanently erase all saved refrigerator data.")
        if confirm:
            user_to_delete = self.current_user
            if user_to_delete in self.users_db:
                del self.users_db[user_to_delete]
                self.save_users()
            if os.path.exists(self.food_file):
                try:
                    with open(self.food_file, "r") as file:
                        food_data = json.load(file)
                    if isinstance(food_data, dict) and user_to_delete in food_data:
                        del food_data[user_to_delete]
                        with open(self.food_file, "w") as file:
                            json.dump(food_data, file, indent=4)
                except:
                    pass
            messagebox.showinfo("Complete", "Your membership deleting has been safely processed.")
            self.try_logout()

    def show_option_ui_manually(self):
        if self.current_user:
            self.backup_option = self.fridge_option.get() 
        self.change_opt_btn.pack_forget()
        self.option_frame.pack(fill="x", padx=40, pady=10, before=self.fridge_btn_frame)
        self.cancel_opt_btn.pack(anchor="e", pady=(10, 0)) 

    def cancel_option_ui(self):
        self.fridge_option.set(self.backup_option) 
        self.option_frame.pack_forget()
        self.change_opt_btn.pack(pady=10, before=self.fridge_btn_frame)

    def on_option_changed(self):
        if self.current_user:
            selected_opt = self.fridge_option.get()
            self.users_db[self.current_user]["fridge_option"] = selected_opt
            self.save_users()

    def open_fridge(self):
        if not self.current_user:
            self.status_label.config(text="⚠️ Login first to create and open a refrigerator!", fg="black")
            return

        if self.users_db[self.current_user].get("is_new", False):
            self.users_db[self.current_user]["is_new"] = False
            self.save_users()

        selected_opt = self.fridge_option.get()
        self.root.withdraw()
        
        fridge_window = tk.Toplevel(self.root)
        app = FridgeApp(fridge_window, selected_opt, self.current_user, self)
        fridge_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close_fridge(fridge_window))

    def on_close_fridge(self, fridge_window):
        fridge_window.destroy()
        if self.current_user:
            self.option_frame.pack_forget()
            self.change_opt_btn.pack(pady=10, before=self.fridge_btn_frame)
        self.root.deiconify()



class Food:
    def __init__(self, name, expiry, food_type, storage, region, page=1):
        self.name = name
        self.expiry = expiry
        self.food_type = food_type
        self.storage = storage
        self.region = region
        self.page = page


    def to_dict(self):
        return {
            "name": self.name,
            "expiry": self.expiry,
            "food_type": self.food_type,
            "storage": self.storage,
            "region": self.region,
            "page": self.page
        }


class FridgeApp:
    def __init__(self, root, fridge_option=1, current_user="default", main_menu_ref=None):
        self.root = root
        self.main_menu = main_menu_ref
        self.root.title(f"Smart Fridge - ({current_user}'s Kitchen)")
        self.root.geometry("1420x850")
        self.root.configure(bg="#d9d9d9")

        self.fridge_option = fridge_option
        self.current_user = current_user

        self.food_objects = {}
        self.all_foods = []
        self.current_page = 1
        self.max_page = 1


        self.master_scrollbar = tk.Scrollbar(self.root, orient="vertical")
        self.master_scrollbar.pack(side="right", fill="y")

        self.master_canvas = tk.Canvas(self.root, bg="#d9d9d9", highlightthickness=0, yscrollcommand=self.master_scrollbar.set)
        self.master_canvas.pack(side="left", fill="both", expand=True)
        self.master_scrollbar.config(command=self.master_canvas.yview)

        self.scrollable_frame = tk.Frame(self.master_canvas, bg="#d9d9d9")
        self.canvas_window = self.master_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.master_canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.root.bind_all("<MouseWheel>", self.on_mouse_wheel) 
        self.root.bind_all("<Button-4>", self.on_mouse_wheel)
        self.root.bind_all("<Button-5>", self.on_mouse_wheel)

        self.create_gui()
        self.load_foods()

    def on_frame_configure(self, event):
        self.master_canvas.configure(scrollregion=self.master_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.master_canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mouse_wheel(self, event):
        if event.num == 4:
            self.master_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.master_canvas.yview_scroll(1, "units")
        else:
            self.master_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_info_box(self, parent):
        frame = tk.Frame(
            parent,
            width=250,
            height=180,
            bg="#d9d9d9",
            relief="flat",
            bd=0
        )
        frame.pack(pady=20)
        frame.pack_propagate(False)


        name = tk.Label(frame, text="", bg="#d9d9d9", anchor="w")
        name.pack(fill="x", padx=10, pady=5)


        expiry = tk.Label(frame, text="", bg="#d9d9d9", anchor="w")
        expiry.pack(fill="x", padx=10)


        food_type = tk.Label(frame, text="", bg="#d9d9d9", anchor="w")
        food_type.pack(fill="x", padx=10)


        storage = tk.Label(frame, text="", bg="#d9d9d9", anchor="w")
        storage.pack(fill="x", padx=10)
        
        delete_button = tk.Button(frame, text="Delete")
        return {
            "frame": frame,
            "name": name,
            "expiry": expiry,
            "type": food_type,
            "storage": storage,
            "delete_button": delete_button
        }

    def create_gui(self):
        utility_frame = tk.Frame(self.scrollable_frame, bg="#d9d9d9")
        utility_frame.pack(fill="x", padx=20, pady=5)
        
        back_btn = tk.Button(
            utility_frame, text="◀ Back to Main", font=("Arial", 11, "bold"),
            bg="#BDC3C7", fg="black", padx=10, pady=5, command=self.back_to_main
        )
        back_btn.pack(side="left")


        top_frame = tk.Frame(self.root,bg="#d9d9d9")
        top_frame.pack(pady=20)

        tk.Label(top_frame,text="Food Name:",bg="#d9d9d9").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(top_frame,width=40)
        self.name_entry.grid(row=0, column=1)

        tk.Label(top_frame,text="Type:",bg="#d9d9d9").grid(row=1,column=0)
        self.type_box = ttk.Combobox(
            top_frame,
            values=[
                "Dairy",
                "Meat",
                "Vegetable",
                "Fruits",
                "Frozen Food"
            ],
            state="readonly",
            width=37
        )
        self.type_box.grid(row=1,column=1)
        self.expiry_label = tk.Label(top_frame,text="Expiry Date:",bg="#d9d9d9")
        self.expiry_label.grid(row=2,column=0)


        self.expiry_frame = tk.Frame(top_frame,bg="#d9d9d9")
        self.expiry_frame.grid(row=2,column=1)

        # Day
        self.day_box = ttk.Combobox(
            self.expiry_frame,
            values=[str(i).zfill(2) for i in range(1, 32)],
            width=9,
            state="readonly"
        )
        self.day_box.pack(side="left", padx=2)


        # Month
        self.month_box = ttk.Combobox(
            self.expiry_frame,
            values=[str(i).zfill(2) for i in range(1, 13)],
            width=9,
            state="readonly"
        )
        self.month_box.pack(side="left", padx=2)


        self.days_frame = tk.Frame(top_frame,bg="#d9d9d9")
        self.days_entry = tk.Entry(self.days_frame,width=40)
        self.days_entry.pack(side="left")


        # Year
        from datetime import datetime
        current_year = datetime.now().year
        self.year_box = ttk.Combobox(
            self.expiry_frame,
            values=[
                str(year)
                for year in range(current_year, current_year + 6)
            ],
            width=10,
            state="readonly"
        )
        self.year_box.pack(side="left", padx=2)
        self.type_box.bind("<<ComboboxSelected>>",self.change_expiry_input)


        tk.Label(top_frame,text="Storage:",bg="#d9d9d9").grid(row=3, column=0)
        self.storage_box = ttk.Combobox(
            top_frame,
            values=[
                "Frozen",
                "Refrigerated"
            ],
            state="readonly",
            width=37
        )
        self.storage_box.grid(row=3, column=1)



        self.sort_button = tk.Menubutton(
            top_frame,
            text="Sort ▼",
            relief="raised",
            width=8
        )
        self.sort_menu = tk.Menu(self.sort_button,tearoff=0)
        self.sort_menu.add_command(label="Added Order",command=lambda: self.sort_foods("Added Order"))
        self.sort_menu.add_command(label="Expiry (Soonest)",command=lambda: self.sort_foods("Expiry (Soonest)"))
        self.sort_menu.add_command(label="Expiry (Latest)",command=lambda: self.sort_foods("Expiry (Latest)"))
        self.sort_button["menu"] = self.sort_menu
        self.sort_button.grid(row=4,column=2,pady=(5, 0))


        tk.Button(top_frame,text="Add Food",command=self.add_food).grid(row=3, column=2, padx=20)
        self.error_label = tk.Label(
            self.root,
            text="",
            fg="red",
            bg="#d9d9d9",
            font=("Arial", 11, "bold")
        )
        self.error_label.pack(pady=(5,10))
        main_frame = tk.Frame(self.root,bg="#d9d9d9")
        main_frame.pack(expand=True)


        left_frame = tk.Frame(main_frame,bg="#d9d9d9")
        left_frame.grid(row=0,column=0,padx=20)
 

        self.box1 = self.create_info_box(left_frame)
        self.box1["frame"].pack_configure(pady=(0, 40))
        self.box3 = self.create_info_box(left_frame)


        center_frame = tk.Frame(main_frame,bg="#d9d9d9")
        center_frame.grid(row=0,column=1)


        self.canvas = tk.Canvas(
            center_frame,
            width=520,
            height=650,
            bg="#bfbfbf",
            highlightthickness=0
        )
        self.canvas.pack()

        self.canvas.create_rectangle(
            50, 30,
            470, 610,
            fill="#e6e6e6",
            width=3
        )
        self.canvas.create_rectangle(
            80, 60,
            440, 200,
            fill="white"
        )
        self.canvas.create_rectangle(
            80, 240,
            440, 380,
            fill="white"
        )
        self.canvas.create_rectangle(
            80, 420,
            440, 560,
            fill="white"
        )
        nav_frame = tk.Frame(center_frame, bg="#d9d9d9")
        nav_frame.pack(pady=10)
        
        self.prev_btn = tk.Button(nav_frame, text="◀", font=("Arial", 14), command=self.prev_page)
        self.prev_btn.pack(side="left", padx=10)


        self.page_label = tk.Label(nav_frame, text="Page 1 / 1", font=("Arial", 12, "bold"), bg="#d9d9d9", width=10)
        self.page_label.pack(side="left", padx=10)


        self.next_btn = tk.Button(nav_frame, text="▶", font=("Arial", 14), command=self.next_page)
        self.next_btn.pack(side="left", padx=10)



        right_frame = tk.Frame(main_frame,bg="#d9d9d9")
        right_frame.grid(row=0,column=2,padx=20)


        self.box2 = self.create_info_box(right_frame)
        self.box2["frame"].pack_configure(pady=(0, 40))
        self.box4 = self.create_info_box(right_frame)

        self.region_boxes = {
            1: self.box1,
            2: self.box2,
            3: self.box3,
            4: self.box4
        }

    def back_to_main(self):
        self.root.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")
        if self.main_menu:
            self.main_menu.on_close_fridge(self.root)

    def change_expiry_input(self, event=None):
        selected_type = self.type_box.get()
        if selected_type in ["Fruits", "Vegetable"]:
            self.expiry_label.config(text="Days Until Expiry:")
            self.expiry_frame.grid_remove()
            self.days_frame.grid(row=2, column=1, sticky="w")
        else:
            self.expiry_label.config(text="Expiry Date:")
            self.days_frame.grid_remove()
            self.expiry_frame.grid(row=2, column=1, sticky="w")

    def add_food(self):
        name = self.name_entry.get().strip()
        food_type = self.type_box.get()
        storage = self.storage_box.get()

        if not name or not food_type:
            self.error_label.config(text="Please fill in all food information.")
            return

        from datetime import datetime, timedelta


        if food_type in ["Fruits", "Vegetable"]:
            days = self.days_entry.get().strip()
            
            if days == "" or not days.isdigit():
                self.error_label.config(text="Invalid days input.")
                return
            
            expiry_date = datetime.now() + timedelta(days=int(days))
            expiry = expiry_date.strftime("%d-%m-%Y")


        else:
            day, month, year = self.day_box.get(), self.month_box.get(), self.year_box.get()
            if not day or not month or not year:
                self.error_label.config(text="Please select an expiry date.")
               
                return
            
            expiry = f"{day}-{month}-{year}"


        if not storage:
            self.error_label.config(text="Please select a storage type.")
            return

        self.error_label.config(text="")
        self.clear_inputs()


        food = Food(name, expiry, food_type, storage, region=1, page=1)
        self.all_foods.append(food)
        
        self.reorganize_foods()

        self.current_page = food.page
        self.reorganize_foods()
        self.save_foods()



    def show_info(self, rect):
        food = self.food_objects[rect]
        box = self.region_boxes[food.region]
        if box["name"].cget("text") == f"Name: {food.name}" and box["frame"].cget("relief") == "solid":
            box["frame"].config(bg="#d9d9d9", relief="flat", bd=0)
            box["name"].config(text="", bg="#d9d9d9")
            box["expiry"].config(text="", bg="#d9d9d9")
            box["type"].config(text="", bg="#d9d9d9")
            box["storage"].config(text="", bg="#d9d9d9")
            box["delete_button"].pack_forget()
            return

        box["frame"].config(bg="white", relief="solid", bd=1)
        box["name"].config(text=f"Name: {food.name}", bg="white")
        box["expiry"].config(text=f"Expiry: {food.expiry}", bg="white")
        box["type"].config(text=f"Type: {food.food_type}", bg="white")
        box["storage"].config(text=f"Storage: {food.storage}", bg="white")
        box["delete_button"].config(command=lambda r=rect: self.delete_food(r))
        box["delete_button"].pack(pady=10)

    


    def delete_food(self, rect):
        if rect not in self.food_objects: 
            return

        food = self.food_objects[rect]
        box = self.region_boxes[food.region]
        box["frame"].config(bg="#d9d9d9", relief="flat", bd=0)
        box["name"].config(text="", bg="#d9d9d9")
        box["expiry"].config(text="", bg="#d9d9d9")
        box["type"].config(text="", bg="#d9d9d9")
        box["storage"].config(text="", bg="#d9d9d9")
        box["delete_button"].pack_forget()

        if food in self.all_foods:
            self.all_foods.remove(food)

        self.clear_info_boxes()
        self.reorganize_foods()
        self.save_foods()



    def save_foods(self):
        food_list = [food.to_dict() for food in self.all_foods]
        try:
            with open(
                "foods.json", 
                "r"
            ) as file:
                data_to_save = json.load(file)
                if not isinstance(data_to_save, dict): data_to_save = {}
        except:
            data_to_save = {}

        data_to_save[self.current_user] = food_list
        with open(
            "foods.json", 
            "w"
        ) as file:
            json.dump(data_to_save, file, indent=4)

    def reorganize_foods(self):
        for item in list(self.food_objects.keys()):
            self.canvas.delete(item)
        self.food_objects.clear()

        frozen_count = 0
        refrig_count = 0

        for food in self.all_foods:
            if food.storage == "Frozen":
                if self.fridge_option == 1:
                    food.page = (frozen_count // 24) + 1
                    p_idx = frozen_count % 24
                    x = 110 + (p_idx % 6) * 55
                    y = 90 + (p_idx // 6) * 55
                elif self.fridge_option == 2:
                    food.page = (frozen_count // 18) + 1
                    p_idx = frozen_count % 18
                    x = 110 + (p_idx % 6) * 55
                    y = 90 + (p_idx // 6) * 55
                else:
                    food.page = (frozen_count // 12) + 1
                    p_idx = frozen_count % 12
                    x = 110 + (p_idx % 6) * 55
                    y = 90 + (p_idx // 6) * 55
                frozen_count += 1
            else:
                if self.fridge_option == 1:
                    food.page = (refrig_count // 12) + 1
                    p_idx = refrig_count % 12
                    x = 110 + (p_idx % 6) * 55
                    y = 450 + (p_idx // 6) * 55
                elif self.fridge_option == 2:
                    food.page = (refrig_count // 18) + 1
                    p_idx = refrig_count % 18
                    x = 110 + (p_idx % 6) * 55
                    y = 360 + (p_idx // 6) * 55
                else:
                    food.page = (refrig_count // 24) + 1
                    p_idx = refrig_count % 24
                    if p_idx < 12:
                        x = 110 + (p_idx % 6) * 55
                        y = 270 + (p_idx // 6) * 55
                    else:
                        tmp = p_idx - 12
                        x = 110 + (tmp % 6) * 55
                        y = 450 + (tmp // 6) * 55
                refrig_count += 1
                
            fridge_center_x = 260
            fridge_center_y = 320
            if x < fridge_center_x:
                food.region = 1 if y < fridge_center_y else 3
            else:
                food.region = 2 if y < fridge_center_y else 4

        self.max_page = max([f.page for f in self.all_foods] + [1])
        if self.current_page > self.max_page:
            self.current_page = self.max_page

        f_render = 0
        r_render = 0
        for food in self.all_foods:
            if food.storage == "Frozen":
                if self.fridge_option == 1:
                    f_p = (f_render // 24) + 1
                    p_idx = f_render % 24
                    x = 110 + (p_idx % 6) * 55
                    y = 90 + (p_idx // 6) * 55
                elif self.fridge_option == 2:
                    f_p = (f_render // 18) + 1
                    p_idx = f_render % 18
                    x = 110 + (p_idx % 6) * 55
                    y = 90 + (p_idx // 6) * 55
                else:
                    f_p = (f_render // 12) + 1
                    p_idx = f_render % 12
                    x = 110 + (p_idx % 6) * 55
                    y = 90 + (p_idx // 6) * 55
                f_render += 1
                if f_p != self.current_page: continue
            else:
                if self.fridge_option == 1:
                    r_p = (r_render // 12) + 1
                    p_idx = r_render % 12
                    x = 110 + (p_idx % 6) * 55
                    y = 450 + (p_idx // 6) * 55
                elif self.fridge_option == 2:
                    r_p = (r_render // 18) + 1
                    p_idx = r_render % 18
                    x = 110 + (p_idx % 6) * 55
                    y = 360 + (p_idx // 6) * 55
                else:
                    r_p = (r_render // 24) + 1
                    p_idx = r_render % 24
                    if p_idx < 12:
                        x = 110 + (p_idx % 6) * 55
                        y = 270 + (p_idx // 6) * 55
                    else:
                        tmp = p_idx - 12
                        x = 110 + (tmp % 6) * 55
                        y = 450 + (tmp // 6) * 55
                r_render += 1
                if r_p != self.current_page: continue

            rect = self.canvas.create_rectangle(
                x,
                y,
                x + 30,
                y + 30,
                fill=self.get_food_color(food.food_type),
                outline="black"
            )
            self.food_objects[rect] = food
            self.canvas.tag_bind(
                rect,
                "<Button-1>",
                lambda e, r=rect: self.show_info(r)
            )

        self.page_label.config(text=f"Page {self.current_page} / {self.max_page}")


    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.clear_info_boxes()
            self.reorganize_foods()


    def next_page(self):
        if self.current_page < self.max_page:
            self.current_page += 1
            self.clear_info_boxes()
            self.reorganize_foods()


    def clear_info_boxes(self):
        for box in self.region_boxes.values():
            box["frame"].config(bg="#d9d9d9", relief="flat", bd=0)
            box["name"].config(text="", bg="#d9d9d9")
            box["expiry"].config(text="", bg="#d9d9d9")
            box["type"].config(text="", bg="#d9d9d9")
            box["storage"].config(text="", bg="#d9d9d9")
            box["delete_button"].pack_forget()
        self.selected_rect = None



    def get_food_color(self, food_type):
        colors = {
            "Dairy": "#5DADE2",
            "Meat": "#EC7063",
            "Vegetable": "#58D68D",
            "Fruits": "#F4D03F",
            "Frozen Food": "#2A98E2"
        }
        return colors[food_type]
    
    def clear_inputs(self):

        # Food name
        self.name_entry.delete(0, tk.END)

        # Combobox
        self.type_box.set("")
        self.storage_box.set("")

        # Date Combobox
        self.day_box.set("")
        self.month_box.set("")
        self.year_box.set("")

        # Days until expiry
        self.days_entry.delete(0, tk.END)
        self.expiry_label.config(text="Expiry Date:")
        self.days_frame.grid_remove()
        self.expiry_frame.grid(row=2, column=1, sticky="w")
        

    def load_foods(self):
        try:
            with open(
                "foods.json",
                "r"
            ) as file:
                data = json.load(file)
        except:
            self.all_foods = []
            return
        self.all_foods = [Food(item["name"], item["expiry"], item["food_type"], item["storage"], item["region"], item.get("page", 1)) for item in data]
        self.reorganize_foods()


    def sort_foods(self, option):
        if option == "Added Order":
            self.load_foods()
            return

        elif option in ["Expiry (Soonest)", "Expiry (Latest)"]:
            pq = []
            for food in self.all_foods:
                expiry = datetime.strptime(food.expiry, "%d-%m-%Y")
                heapq.heappush(pq, (expiry, id(food), food))

            self.all_foods = []
            while pq:
                _, _, food = heapq.heappop(pq)
                self.all_foods.append(food)
            if option == "Expiry (Latest)":
                self.all_foods.reverse()

        self.reorganize_foods()
        self.save_foods()




root = tk.Tk()
app = MainMenu(root)
root.mainloop()
