from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# Opens file explorer to facilitate selection of image file to be loaded in program
def open_image():

    filename = filedialog.askopenfilename(initialdir = ".", title = "Select an Image",
                                          filetypes = (("Image files", "*.png* *.jpg"), 
                                                       ("all files", "*.*")))
    
    # Open image
    image = Image.open(filename)

    # Resize image
    base_height = 300
    hpercent = (base_height / float(image.size[1]))
    wsize = int((float(image.size[0]) * float(hpercent)))
    image = image.resize((wsize, base_height), Image.Resampling.LANCZOS)

    # Display image
    tkimage = ImageTk.PhotoImage(image)
    image_label.config(image=tkimage)
    image_label.config(height=base_height)
    image_label.image = tkimage

# Opens dialog box containing information on the program
def open_about_dialog():

    about_dialog = Toplevel(window)
    about_dialog.title('About')
    about_text = "Created by Annabelle Stokes, Ian Harris, Joel Clement, Louis Tracy, and Truan Leiker."
    about_label = Label(about_dialog, text=about_text)
    about_label.pack()

# Metadata
window = Tk()
window.title('DigitAIze')
window.geometry('600x400')

# Menu ribbon
menu_ribbon = Menu(window)
window.config(menu=menu_ribbon)
file_menu = Menu(menu_ribbon)
menu_ribbon.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=open_image)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=window.quit)
help_menu = Menu(menu_ribbon)
menu_ribbon.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='About', command=open_about_dialog)

# Create widgets
take_photo_button = Button(window, text='Take Photo')
import_image_button = Button(window, text='Import Image', command=open_image)
view_results_button = Button(window, text='View results')
image_frame = Frame(window, width="1000", height="1000", borderwidth=1, relief='solid')
image_label = Label(image_frame, text='Imported image will display here', height=20)
image_label.pack(fill=BOTH, expand=True)
convert_button = Button(window, text='Convert')

# Arrange widgets
take_photo_button.grid(column=0, row=0, sticky='nesw', padx=4, pady=4)
import_image_button.grid(column=1, row=0, sticky='nesw', padx=4, pady=4)
view_results_button.grid(column=2, row=0, sticky='nesw', padx=4, pady=4)
image_frame.grid(column=0, row=1, sticky='nesw', columnspan=3, padx=4, pady=4)
convert_button.grid(column=0, row=2, sticky='nesw', padx=4, pady=4)

# Begin main loop
window.mainloop()