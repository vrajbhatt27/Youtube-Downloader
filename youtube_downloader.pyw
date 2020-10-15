import pafy
import youtube_dl
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import filedialog
import os


class YouTube:
    def __init__(self,url,srm=None,path=None):
        self.url = url
        self.vid = pafy.new(url)
        self.lst = []
        self.map = {}
        self.srm = srm
        self.path = path
        self.mapings()

    def get_res(self,res):
        x = res.split('x')
        return x[1]

    def mapings(self):
        srm = self.vid.streams
        for i in srm:
            ex = i.extension
            res = self.get_res(i.resolution)
            self.lst.append((ex, res))
            self.map[(ex, res)] = i

    def get_params(self):
        return self.lst

    def get_mapping(self):
        return self.map

    def mycb(self,total, recvd, ratio, rate, eta):
        pass

    def download(self):
        try:
            if self.path == None:
                self.srm.download(quiet=True,callback=self.mycb)
            else:
                self.srm.download(filepath=self.path,quiet=True, callback=self.mycb)
        except:
            return False

        return True

    def download_audio(self):
        try:
            self.srm = self.vid.getbestaudio()

            if self.path == None:
                self.srm.download(quiet=True,callback=self.mycb)
            else:
                self.srm.download(filepath=self.path,quiet=True, callback=self.mycb)

        except:
            return False

        return True


root = Tk()
root.geometry('400x350')
root.minsize(400, 350)
root.maxsize(400, 350)
root.config(bg="grey")
root.title("Youtube Downloader")
link = StringVar()
url = None
selected_value_ext_cb = None
ext_cb = None  # combobox widgit
mapping = None
top = None
filepath = None
default = os.getcwd()


# YD module--------------------------------------
# Get Available Extensions from YD module
def extention_contents(yt):
    global mapping, url
    try:
        mapping = yt.get_mapping()
        ls = yt.get_params()
        ext = []
        for e in ls:
            s = e[0] + " " + e[1]
            ext.append(s)
        return ext
    except:
        messagebox.showinfo("Error", "Some Error Occured")
        return


def download_vid():
    try:
        srm = None
        tup = tuple(selected_value_ext_cb.split(" "))
        for t in mapping.keys():
            if t == tup:
                srm = mapping[t]

        fin_yt = YouTube(url, srm, filepath)
        stat = fin_yt.download()
        if stat == True:
            messagebox.showinfo("Status", "Downloaded Successfully")
            top.destroy()
    except:
        messagebox.showinfo("Error", "Cannot Download Video")
        top.destroy()


def download_aud():
    global link
    url = str(link.get())
    try:
        yt = YouTube(url, path=filepath)
        stat = yt.download_audio()
        if stat == True:
            messagebox.showinfo("Status", "Downloaded Successfully")
    except:
        messagebox.showinfo("Error", "Cannot Download Audio")


##################################################

# Gets the selected value of combobox
def cb_val(event):
    global ext_cb, selected_value_ext_cb, flag
    selected_value_ext_cb = ext_cb.get()


def browsefunc(lbl):
    global filepath, default
    filepath = filedialog.askdirectory()
    lbl.config(text=str(filepath))


# Top Level
def open():
    global url, ext_cb, top
    url = str(link.get())

    try:
        yt = YouTube(url)
    except:
        messagebox.showinfo("Error", "Cannot Download Video")
        return

    # Basics Setup-------------------------------------
    top = Toplevel(root)
    top.geometry('400x350')
    top.minsize(400, 350)
    top.maxsize(400, 350)
    top.config(bg="grey")
    top.title("Video Download")

    fr_cb = Frame(top, borderwidth=8, bg="grey")
    fr_cb.grid(pady=25)
    ###################################################

    # for extension combobox---------------------------------------------------
    try:
        ext = extention_contents(yt)
    except:
        messagebox.showinfo("Error", "Some Error Occured")
        top.destroy()

    lbl_extCB = Label(fr_cb, text="Extension", font="Helvetica 16 bold", bg="grey")
    lbl_extCB.grid(row=0, column=0, pady=25)

    ext_cb = Combobox(fr_cb, values=ext)
    ext_cb.grid(row=0, column=1, pady=25)

    ext_cb.bind("<<ComboboxSelected>>", cb_val)
    ###############################################################

    # frame for button----------------------------------------------------------
    frb = Frame(top, borderwidth=8, bg="grey")
    frb.grid()

    b1 = Button(frb, text="Download", width=10, bg='gray21', fg='white', command=download_vid)
    b1.grid(padx=150)
    ###########################################################################

    top.mainloop()


# main window
def master_win():
    global root, link, default

    # ///////////////////////////////////////////////////////////////////////////
    # Frame for url ------------------------------------------------------
    fr = Frame(root, borderwidth=8, bg="grey")
    fr.grid(pady=50)

    url = Label(fr, text="URL: ", font="Helvetica 16 bold", bg="grey")
    url.grid(row=0, column=0)

    entry1 = Entry(fr, textvariable=link, width=50)
    entry1.grid(row=0, column=1)

    # frame for button----------------------------------------------------------
    frb = Frame(root, borderwidth=8, bg="grey")
    frb.grid(row=2, column=0)

    b1 = Button(frb, text="Video", width=10, bg='gray21', fg='white', command=open)
    b1.grid(row=0, column=0, padx=10)

    b2 = Button(frb, text="Audio", width=10, bg='gray21', fg='white', command=download_aud)
    b2.grid(row=0, column=1, padx=25)
    # ///////////////////////////////////////////////////////////////////////////

    # frame for Browse----------------------------------------------------------
    frf = Frame(root, borderwidth=8, bg="grey")
    frf.grid()

    dp = Label(frf, text="Download Path:", font="Helvetica 10", bg="grey")
    dp.grid(row=0, column=0)

    fpath = Label(frf, text=str(default), font="Helvetica 10", bg="white")
    fpath.grid(row=1, column=0)

    browse = Button(frf, text="Browse", width=10, bg='gray21', fg='white', command=lambda: browsefunc(fpath))
    browse.grid(row=2, column=0, padx=25)
    # ///////////////////////////////////////////////////////////////////////////

    root.mainloop()


master_win()

