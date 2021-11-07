import os
import random

import tkinter as tk
from PIL import Image, ImageTk
from playsound import playsound
import datetime as dt
import requests, json

import pyowm


token = "input token here"
databaseId = "input database id"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16",
}
# change any of these constants to style and make it your own!
WINDOW_TITLE = ""
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 800
IMG_HEIGHT = 230
IMG_WIDTH = 230
WHITE_COLOR_HEX = "#FFFFFF"
SOUND_EFFECT_FILE_PATH = "assets/yes-2.wav"
TODAY_PATH = "assets/TODAY.png"
# dynamically open folders and make a list, while ignoring any hidden files that start with "."
# just add any image file into these folders and they will magically appear in your wardrobe!
# for fun, try to expand this wardrobe to support shoes!
ALL_TOPS = [
    str("tops/") + file for file in os.listdir("tops/") if not file.startswith(".")
]
ALL_BOTTOMS = [
    str("bottoms/") + file
    for file in os.listdir("bottoms/")
    if not file.startswith(".")
]
CHILL_TOPS = [
    str("chill_tops/") + file
    for file in os.listdir("chill_tops/")
    if not file.startswith(".")
]
CHILL_BOTTOMS = [
    str("chill_bottoms/") + file
    for file in os.listdir("chill_bottoms/")
    if not file.startswith(".")
]
CUTE_TOPS = [
    str("cute_tops/") + file
    for file in os.listdir("cute_tops/")
    if not file.startswith(".")
]
CUTE_BOTTOMS = [
    str("cute_bottoms/") + file
    for file in os.listdir("cute_bottoms/")
    if not file.startswith(".")
]


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.title(WINDOW_TITLE)
        self.geometry("{0}x{1}".format(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.switch_frame(TestPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""

        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()

        self._frame = new_frame
        print(self._frame)
        self._frame.pack()
        tk.Tk.update(self)


class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


class PageOne(tk.Frame):
    # def __init__(self, master):
    #

    #     Outfit.pack(root)

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        # collecting all the clothes
        self.top_images = CUTE_TOPS
        self.bottom_images = CUTE_BOTTOMS

        # first pictures for top and bottom
        self.tops_image_path = self.top_images[0]
        self.bottom_image_path = self.bottom_images[0]

        # creating 2 frames
        self.tops_frame = tk.Frame(self, bg="white")
        self.bottoms_frame = tk.Frame(self, bg="white")
        self.footer = tk.Frame(self, bg="white")
        self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.bottoms_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.footer.pack(fill=tk.BOTH, expand=tk.YES)
        self.top_image_label = self.create_photo(self.tops_image_path, self.tops_frame)
        self.top_image_label.pack(pady=25, side=tk.TOP)

        # Adding number of times worn

        # adding bottom
        self.bottom_image_label = self.create_photo(
            self.bottom_image_path, self.bottoms_frame
        )

        self.bottom_image_label.pack(pady=(25, 0))
        next = ImageTk.PhotoImage(file="assets/next.png")
        prev = ImageTk.PhotoImage(file="assets/prev.png")
        create = ImageTk.PhotoImage(file="assets/create.png")
        back = ImageTk.PhotoImage(file="assets/BACK.png")
        send2 = ImageTk.PhotoImage(file="assets/send.png")
        top_prev_button = tk.Button(
            self.tops_frame,
        )
        top_prev_button.config(
            image=prev,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            compound="top",
            command=self.get_prev_top,
        )
        top_prev_button.image = prev
        top_prev_button.pack(side=tk.LEFT)

        top_next_button = tk.Button(
            self.tops_frame,
        )
        top_next_button.config(
            image=next,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            compound="top",
            command=self.get_next_top,
        )
        top_next_button.image = next
        top_next_button.pack(side=tk.RIGHT)

        create_outfit_button = tk.Button(
            self.footer,
        )
        create_outfit_button.config(
            image=create,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            compound="top",
            command=self.create_outfit,
        )
        create_outfit_button.image = create
        create_outfit_button.pack()

        bottom_prev_button = tk.Button(
            self.bottoms_frame,
        )
        bottom_prev_button.config(
            image=prev,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            compound="top",
            command=self.get_prev_bottom,
        )
        bottom_prev_button.image = prev
        bottom_prev_button.pack(side=tk.LEFT)

        bottom_next_button = tk.Button(
            self.bottoms_frame,
        )
        bottom_next_button.config(
            image=next,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            compound="top",
            command=self.get_next_bottom,
        )
        bottom_next_button.image = next
        bottom_next_button.pack(side=tk.RIGHT)

        redo = tk.Button(
            self.footer,
        )
        redo.config(
            image=back,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            compound="top",
            command=lambda: master.switch_frame(TestPage),
        )
        redo.image = back

        redo.pack(pady=30, side=tk.LEFT)

        notion = tk.Button(
            self.footer,
        )
        notion.config(
            image=send2,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            command=lambda: self.readDatabase(databaseId, headers, master),
        )
        notion.image = send2

        notion.pack(pady=30, side=tk.RIGHT)

    def create_photo(self, image, frame):
        top_image_file = Image.open(image)
        image = top_image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo, anchor=tk.CENTER)
        image_label.image = photo

        return image_label

    def update_photo(self, new_image, image_label):
        new_image_file = Image.open(new_image)
        image = new_image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo

    def _get_next_item(self, current_item, category, increment=True):
        """Gets the Next Item In a Category depending on if you hit next or prev
        Args:
            current_item, str
            category, list
            increment, boolean
        """
        item_index = category.index(current_item)
        final_index = len(category) - 1
        next_index = 0

        if increment and item_index == final_index:
            next_index = 0  # cycle back to the beginning
        elif not increment and item_index == 0:
            next_index = final_index  # cycle back to the end
        else:
            incrementor = 1 if increment else -1
            next_index = item_index + incrementor

        next_image = category[next_index]

        # reset the image object
        if current_item in self.top_images:
            image_label = self.top_image_label
            self.tops_image_path = next_image
        else:
            image_label = self.bottom_image_label
            self.bottom_image_path = next_image

        # update the photo
        self.update_photo(next_image, image_label)

    def get_next_top(self):
        self._get_next_item(self.tops_image_path, self.top_images, increment=True)

    def get_prev_top(self):
        self._get_next_item(self.tops_image_path, self.top_images, increment=False)

    def get_prev_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottom_images, increment=False)

    def get_next_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottom_images, increment=True)

    def create_outfit(self):
        # randomly select an outfit

        new_top_index = random.randint(0, len(self.top_images) - 1)
        new_bottom_index = random.randint(0, len(self.bottom_images) - 1)

        # add the clothes onto the screen
        self.update_photo(self.top_images[new_top_index], self.top_image_label)
        self.update_photo(self.bottom_images[new_bottom_index], self.bottom_image_label)

       

    def readDatabase(self, databaseId, headers, master):

        # get the name of the garments we are looking for
        topbefore = self.tops_image_path
        bottombefore = self.bottom_image_path

        # removing the folder name
        i = topbefore.index("/")
        top = topbefore[i + 1 :]
        j = bottombefore.index("/")
        bottom = bottombefore[j + 1 :]

        # removing the extension
        i = top.index(".")
        topfinal = top[:i]
        j = bottom.index(".")
        bottomfinal = bottom[:j]

        readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

        res = requests.request("POST", readUrl, headers=headers)
        data = res.json()
        print(res.status_code)

        with open("./db.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)
        # print(res.text)

        # create a map with all the names of garments , # worn and id
        d = {}
        for result in data["results"]:

            d[result["properties"]["Name"]["title"][0]["text"]["content"]] = [
                result["id"],
                result["properties"]["# worn"]["number"],
            ]

        id_top = d[topfinal][0]
        id_bottom = d[bottomfinal][0]
        worn_top = d[topfinal][1]
        worn_bottom = d[bottomfinal][1]

        self.updatePage(
            headers,
            id_top,
            id_bottom,
            worn_top,
            worn_bottom,
            topfinal,
            bottomfinal,
            master,
        )

    def updatePage(
        self,
        headers,
        id_top,
        id_bottom,
        worn_top,
        worn_bottom,
        topfinal,
        bottomfinal,
        master,
    ):

        newworn_top = worn_top + 1
        newworn_bottom = worn_bottom + 1
        updateUrl_top = f"https://api.notion.com/v1/pages/{id_top}"

        updateData_top = {
            "properties": {
                "# worn": {"number": newworn_top},
                "Pairing": {"rich_text": [{"text": {"content": bottomfinal}}]},
            }
        }

        data_top = json.dumps(updateData_top)

        response = requests.request(
            "PATCH", updateUrl_top, headers=headers, data=data_top
        )

        # bottom
        updateUrl_bottom = f"https://api.notion.com/v1/pages/{id_bottom}"

        updateData_bottom = {
            "properties": {
                "# worn": {"number": newworn_bottom},
                "Pairing": {"rich_text": [{"text": {"content": topfinal}}]},
            }
        }

        data_bottom = json.dumps(updateData_bottom)

        response2 = requests.request(
            "PATCH", updateUrl_bottom, headers=headers, data=data_bottom
        )
        master.switch_frame(TestPage)


class TestPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # self.self.title(WINDOW_TITLE)
        # self.self.geometry("{0}x{1}".format(WINDOW_WIDTH, WINDOW_HEIGHT))

        # creating 2 frames

        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(10, weight=1)
        x1 = tk.Button(self)
        x2 = tk.Button(self)
        x3 = tk.Button(self)
        x4 = tk.Button(self)
        x5 = tk.Button(self)

        couch = ImageTk.PhotoImage(file="assets/chill2.png")
        work = ImageTk.PhotoImage(file="assets/work2.png")
        workout = ImageTk.PhotoImage(file="assets/gym.png")
        cute = ImageTk.PhotoImage(file="assets/cute2.png")
        out = ImageTk.PhotoImage(file="assets/out2.png")
        weather = ImageTk.PhotoImage(file="assets/weather2.png")
        x1.config(
            image=couch,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            compound="top",
            command=lambda: master.switch_frame(PageOne),
        )
        x2.config(
            image=work,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            command=lambda: master.switch_frame(PageOne),
        )
        x3.config(
            image=workout,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            command=lambda: master.switch_frame(PageOne),
        )
        x4.config(
            image=cute,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            command=lambda: master.switch_frame(PageOne),
        )
        x5.config(
            image=out,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
            bd=0,
            pady=0,
            padx=0,
            command=lambda: master.switch_frame(PageOne),
        )

        x = tk.Label(
            self, text="TODAY", fg="#333333", bg="white", font=("montserrat", 40)
        )
        e = tk.Label(self, image=weather)
        w = tk.Label(
            self,
            text=f"{dt.datetime.now(): %d %b  }".upper(),
            fg="#333333",
            bg="white",
            font=("montserrat thin", 20),
        )
        chill = tk.Label(
            self,
            text="chill",
            fg="#333333",
            bg="white",
            font=("montserrat thin", 20),
        )
        x1.image = couch
        x2.image = work
        x3.image = workout
        x4.image = cute
        x5.image = out
        e.image = weather
        # Position image

        # Get the weather
        owm = pyowm.OWM("your token")
        mng = owm.weather_manager()
        obs = mng.weather_at_place("Montreal")

        weather = obs.weather
        temp = weather.temperature("celsius")["temp"]

        temp_f = tk.Label(
            self,
            text=f"{temp}°C",
            fg="#333333",
            bg="white",
            font=("montserrat thin", 20),
        )

        x.grid(row=0, column=2)
        w.grid(row=1, column=2)
        x1.grid(row=5, column=0, pady=100, padx=(4, 0))
        x2.grid(row=5, column=2, padx=(10, 0))
        x3.grid(row=5, column=4, padx=(0, 4))
        x4.grid(row=6, column=1, padx=12)
        x5.grid(row=6, column=3, padx=12)
        e.grid(row=10, column=2, pady=(100, 0))
        temp_f.grid(row=11, column=2)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
