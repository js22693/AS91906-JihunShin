import tkinter as tk
from tkinter import ttk
import datetime as dt



class Food:
    def __init__(self, name, expiry, food_type, storage, region):
        self.name = name
        self.expiry = expiry
        self.food_type = food_type
        self.storage = storage
        self.region = region


class FridgeApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Smart Fridge")
        self.root.geometry("1400x900")
        self.root.configure(bg="#d9d9d9")

        self.food_objects = {}

        self.frozen_count = 0
        self.refrigerated_count = 0

        self.create_gui()

    def create_info_box(self, parent):

        frame = tk.Frame(
            parent,
            width=250,
            height=180,
            bg="white",
            relief="solid",
            bd=1
        )

        frame.pack(pady=20)
        frame.pack_propagate(False)

        name = tk.Label(
            frame,
            text="Name:",
            bg="white",
            anchor="w"
        )
        name.pack(fill="x", padx=10, pady=5)

        expiry = tk.Label(
            frame,
            text="Expiry:",
            bg="white",
            anchor="w"
        )
        expiry.pack(fill="x", padx=10)

        food_type = tk.Label(
            frame,
            text="Type:",
            bg="white",
            anchor="w"
        )
        food_type.pack(fill="x", padx=10)

        storage = tk.Label(
            frame,
            text="Storage:",
            bg="white",
            anchor="w"
        )
        storage.pack(fill="x", padx=10)

        return {
            "name": name,
            "expiry": expiry,
            "type": food_type,
            "storage": storage
        }


    def create_gui(self):

        top_frame = tk.Frame(self.root,bg="#d9d9d9")
        top_frame.pack(pady=20)

        

        tk.Label(top_frame,text="Food Name:",bg="#d9d9d9").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(top_frame,width=40)
        self.name_entry.grid(row=0, column=1)



        tk.Label(top_frame,text="Type:",bg="#d9d9d9").grid(row=2, column=0)
        self.type_box = ttk.Combobox(
            top_frame,
            values=[
                "Dairy",
                "Meat",
                "Vegetable",
                "Fruits",
                "frozen food"
            ],
            state="readonly",
            width=37
        )

        tk.Label(top_frame,text="Expiry Date:",bg="#d9d9d9").grid(row=1, column=0)
        self.expiry_box = ttk.Combobox(
            top_frame,
            values=[
                
            ],
            state="readonly",
            width=37
        )
        self.expiry_box.grid(row=1, column=1)
        self.type_box.grid(row=2, column=1)

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

        tk.Button(top_frame,text="Add Food",command=self.add_food).grid(row=3, column=2, padx=20)
        main_frame = tk.Frame(self.root,bg="#d9d9d9")
        main_frame.pack(expand=True)

        left_frame = tk.Frame(main_frame,bg="#d9d9d9")
        left_frame.grid(row=0,column=0,padx=20)

        self.box1 = self.create_info_box(left_frame)
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
        right_frame = tk.Frame(main_frame,bg="#d9d9d9")
        right_frame.grid(row=0,column=2,padx=20)

        self.box2 = self.create_info_box(right_frame)
        self.box4 = self.create_info_box(right_frame)

        self.region_boxes = {
            1: self.box1,
            2: self.box2,
            3: self.box3,
            4: self.box4
        }
    def add_food(self):
        name = self.name_entry.get()
        expiry = self.expiry_box.get()
        food_type = self.type_box.get()
        storage = self.storage_box.get()

        if not name:
            return
        if not food_type:
            return
        if not storage:
            return
        
        #It Will change icons
        colors = {
            "Dairy": "#5DADE2",
            "Meat": "#EC7063",
            "Vegetable": "#58D68D",
            "Fruits": "#F4D03F",
            "frozen food": "#2A98E2"
        }

        if storage == "Frozen":
            count = self.frozen_count
            x = 110 + (count % 6) * 55
            y = 90 + (count // 6) * 55
            self.frozen_count += 1

        else:
            count = self.refrigerated_count
            if count < 12:
                x = 110 + (count % 6) * 55
                y = 270 + (count // 6) * 55

            else:
                count -= 12
                x = 110 + (count % 6) * 55
                y = 450 + (count // 6) * 55

            self.refrigerated_count += 1

        fridge_center_x = 260
        fridge_center_y = 320

        if x < fridge_center_x:
            if y < fridge_center_y:
                region = 1
            else:
                region = 3

        else:
            if y < fridge_center_y:
                region = 2
            else:
                region = 4

        food = Food(
            name,
            expiry,
            food_type,
            storage,
            region
        )

        rect = self.canvas.create_rectangle(
            x,
            y,
            x + 30,
            y + 30,
            fill=colors[food_type],
            outline="black"
        )

        self.food_objects[rect] = food

        self.canvas.tag_bind(
            rect,
            "<Button-1>",
            lambda e, r=rect: self.show_info(r)
        )



    def show_info(self, rect):
        food = self.food_objects[rect]
        box = self.region_boxes[
            food.region
        ]
        box["name"].config(text=f"Name: {food.name}")
        box["expiry"].config(text=f"Expiry: {food.expiry}")
        box["type"].config(text=f"Type: {food.food_type}")
        box["storage"].config(text=f"Storage: {food.storage}")


root = tk.Tk()
app = FridgeApp(root)
root.mainloop()