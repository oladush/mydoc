from tkinter import Tk, Menu, Canvas, Toplevel, filedialog
from PIL import ImageTk, Image
import PyPDF2
import ctypes
import io

# Config
IMPORT_FORMAT = "PNG"
MAX_WIDTH = 1000
MAX_HEIGHT = 1000
ctypes.windll.shcore.SetProcessDpiAwareness(True)

class ImageViewerGui:
    def __init__(self, master, images, information):
        self.page = 0
        self.master = master
        self.images = images
        self.information = information

        self.canvas = None
        self.set_image(images[self.page])

        self.master.title(information[0])

        self.menu = Menu(master=self.master)
        self.master.config(menu=self.menu)

        self.menu.add_command(label="Save as..", command=self.export_pic)
        self.menu.add_command(label="Properties", command=self.view_properties)
        self.menu.add_command(label="Previous page", command=self.previous_page)
        self.menu.add_command(label="Next page", command=self.next_page)

    def set_image(self, img):
        width, height = img.size
        rat = width / height
        if width > MAX_WIDTH:
            width = MAX_WIDTH
            height = round(width / rat)
        if height > MAX_HEIGHT:
            height = MAX_HEIGHT
            width = round(height * rat)

        self.master.minsize(width, height)
        self.master.geometry(f"{width + 1}x{height + 1}")

        img = img.resize((width, height), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(img)

        if self.canvas:
            self.canvas.destroy()

        self.canvas = Canvas(self.master, height=height, width=width)
        self.image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.next_page)
        self.canvas.bind("<Button-3>", self.previous_page)
        self.canvas.bind("<KeyPress>", self.next_page)
        self.canvas.bind("<Left>", self.previous_page)

        self.canvas.bind("<Configure>", self.scalability_)

    def next_page(self, event=None):
        if self.page < len(self.images) - 1:
            self.page += 1
        else:
            self.page = 0
        self.set_image(self.images[self.page])

    def previous_page(self, event=None):
        if self.page > 0:
            self.page -= 1
        else:
            self.page = len(self.images) - 1
        self.set_image(self.images[self.page])

    def view_properties(self, event=None):
        properties = Toplevel(master=self.master)
        properties.geometry("300x300")

    def export_pic(self, event=None):
        filename = self.information[0]
        if len(self.images) > 0:
            filename = "%s_%d.png" % (filename.split(".")[0], self.page)

        save_as = self.save_dialog = filedialog.asksaveasfilename(
            filetypes=(
                ("JPEG files", "*.jpg;*.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ),
            initialfile=filename
        )
        if save_as:
            import_format = IMPORT_FORMAT
            if save_as.split(".")[-1].lower() in ("jpeg", "jpg"):
                import_format = "JPEG"

            img_data = io.BytesIO()
            self.images[self.page].save(img_data, format=import_format)
            with open(save_as, "wb") as wf:
                wf.write(img_data.getvalue())

    def scalability_(self, event=None):
        print(self.master.geometry())


class ImageViewerApp:
    def __init__(self, master, file=None):
        self.master = master
        self.content = []
        if file:
            self.open_file(file)

    def open_file(self, file):
        if file.split('.')[-1].lower() == "pdf":
            pdf = PyPDF2.PdfFileReader(open(file, "rb"))

            for i in range(pdf.numPages):
                page = pdf.getPage(i)
                xObject = page['/Resources']['/XObject'].getObject()

                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                        data = xObject[obj].getData()

                        if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                            mode = 'RGB'
                        else:
                            mode = 'P'
                        if xObject[obj]['/Filter'] == '/FlateDecode':
                            img = Image.frombytes(mode, size, data)
                            self.content.append(img)
        else:
            img = Image.open(file)
            self.content.append(img)

        gui = ImageViewerGui(master=self.master, images=self.content, information=[file])


root = Tk()
app = ImageViewerApp(root, "Hkr06.pdf")

root.mainloop()
