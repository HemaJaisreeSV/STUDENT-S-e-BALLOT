from tkinter import *
from PIL import *
import PIL.Image
from PIL.ImageTk import PhotoImage

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title="STUDENT'S e-BALLOT"
        self.root.geometry("1350x700+0+0")

        #=================All images==================#
        image1 = PIL.Image.open(r"C:\Users\HEMA\Pictures\d6rnj7n-99e2af63-0f6e-4dc5-97c2-848bfcabc6e7.jpg")
        self.bg_icon = PhotoImage(image1)

        image2 = PIL.Image.open(r"C:\Users\HEMA\Pictures\VOTE.jpg")
        self.user_icon = PhotoImage(image2)
        image3 = PIL.Image.open(r"C:\Users\HEMA\Pictures\GANESHA.jpg")
        self.pass_icon = PhotoImage(image3)

        bg_lbl=Label(self.root,image=self.bg_icon).pack()
        
        title=Label(self.root,text = "STUDENT'S e-BALLOT",font=("times new roman",40,"bold"),bg="yellow",fg="red",bd=10,relief=GROOVE)
        title.place(x=0,y=0,relwidth=1)

root = Tk()
obj=Login_System(root)
root.mainloop()