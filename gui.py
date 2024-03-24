from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from digitaize import get_photo_from_webcam
from digitaize import get_video_from_webcam
from digitaize import run_from_image
from digitaize import run_from_video
import cv2

image_to_convert = None
video_to_convert = []


# Opens file explorer to facilitate selection of image file to be loaded in program
def open_image():

    filename = filedialog.askopenfilename(initialdir = ".", title = "Select an Image",
                                          filetypes = (("Image files", "*.png* *.jpg"), 
                                                       ("all files", "*.*")))
    
    # Display image in image frame if valid file
    if filename != "":
        
        # Open image
        frame = cv2.imread(filename, 1)
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Set global filepath for image to convert
        global image_to_convert
        image_to_convert = framergb

        display_image()        


# Displays "image_to_convert" in the GUI
def display_image():

    # Convert cv2 image to something tkinter can read
    image = Image.fromarray(image_to_convert)

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


# Displays the first frame of the video to convert
def display_video():

    # Convert cv2 image to something tkinter can read
    image = Image.fromarray(video_to_convert[0])

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


# Converts the displayed image/video into a landmarks written to JSON file
def convert_image_or_video():
    
    if image_to_convert.any():
        
        run_from_image(image_to_convert)
    
    elif len(video_to_convert):

        run_from_video(video_to_convert)


# Opens webcam
def take_photo():

    global image_to_convert
    global video_to_convert
    image_to_convert = get_photo_from_webcam()
    video_to_convert = None
    display_image()


# Opens webcam
def record_video():

    global video_to_convert
    global image_to_convert
    image_to_convert = None
    video_to_convert = get_video_from_webcam()
    display_video()


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
take_photo_button = Button(window, text='Take Photo', command=take_photo)
record_video_button = Button(window, text='Record Video', command=record_video)
import_image_button = Button(window, text='Import Image/Video', command=open_image)
view_results_button = Button(window, text='View results')
image_frame = Frame(window, width="1000", height="1000", borderwidth=1, relief='solid')
image_label = Label(image_frame, text='Imported image will display here', height=20)
image_label.pack(fill=BOTH, expand=True)
convert_button = Button(window, text='Convert', command=convert_image_or_video)

# Arrange widgets
take_photo_button.grid(column=0, row=0, sticky='nesw', padx=4, pady=4)
record_video_button.grid(column=1, row=0, sticky='nesw', padx=4, pady=4)
import_image_button.grid(column=2, row=0, sticky='nesw', padx=4, pady=4)
view_results_button.grid(column=3, row=0, sticky='nesw', padx=4, pady=4)
image_frame.grid(column=0, row=1, sticky='nesw', columnspan=3, padx=4, pady=4)
convert_button.grid(column=0, row=2, sticky='nesw', padx=4, pady=4)

# Begin main loop
window.mainloop()