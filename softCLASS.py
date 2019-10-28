import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import cv2
from PIL import Image,ImageTk ,ImageEnhance,ImageOps
import PIL
import imghdr
from functools import partial
from ttkthemes import ThemedStyle
import numpy

class App:
   
  def __init__(self, master):
     
    self.master=master
    self.canvaswidth=None
    self.canvasheight=None
    self.image=None
    self.folderImages=[]
    self.originalImage=None
    self.imageSize=None
    self.imageForTk=None
    self.histCanvasHeight=100
    self.histCanvasWidth=256  

   
#==============================================================================
# Scree Size
#==============================================================================
   
    self.screenHeight=root.winfo_screenheight()
    self.screenWidth=root.winfo_screenwidth()
    self.rootWidth=int(self.screenWidth*80/100)
    self.rootHeight=int(self.screenHeight*80/100)
   
    self.master.title("Image Editor by AUG")
    self.master.configure()
    self.master.minsize(self.rootWidth,self.rootHeight)
 
# =============================================================================
# Grids  layout  
# =============================================================================
    self.top_frame = ttk.Frame(self.master,  relief="flat",height=60)
    self.right_frame = ttk.Frame(self.master, relief="flat",width=300)
    self.center_frame = ttk.Frame(self.master, relief="flat")
    self.left_frame = ttk.Frame(self.master, relief="flat",width=200)
    self.bottom_frame = ttk.Frame(self.master, relief="flat",height=150)

    self.top_frame.grid(row=0, column=0, columnspan =2 ,sticky="nsew")
   
    self.right_frame.grid(row=0, column=2, rowspan =3, sticky="wens")
    self.center_frame.grid(row=1, column=1,  sticky="ewns")
    self.left_frame.grid(row=1, column=0, sticky="nsew")
    self.bottom_frame.grid(row=2, column=0,columnspan=3 ,  sticky="nsew")
   
    self.master.grid_rowconfigure(0, weight=0)
    self.master.grid_rowconfigure(1, weight=1)
    self.master.grid_rowconfigure(2, weight=0)
   
    self.master.grid_columnconfigure(0, weight=0)
    self.master.grid_columnconfigure(1, weight=1)
    self.master.grid_columnconfigure(2, weight=0)
   
    self.top_frame.grid_propagate(1)
    self.left_frame.grid_propagate(0)
    self.right_frame.grid_propagate(0)
    self.bottom_frame.grid_propagate(0)

# =============================================================================
#  Init  
# =============================================================================
    self.set_app_style()    
    self.menuInit()
    self.topFrame()
    self.leftFrame()
    self.centerFrame()
    self.bottomFrame()
    self.rightFrame()

#==============================================================================
#
#==============================================================================

  def set_app_style(self):
     
    self.style = ThemedStyle(self.master)
    self.style.set_theme('black')
#    self.style.theme_settings('equilux', {"TNotebook.Tab": {"configure": {"padding": [30, 15]}}})
#    self.style.theme_settings('equilux', {'TButton': {"configure": {"padding": [30, 15]}}})
    self.style.map("TButton",foreground=[('pressed', 'white'), ('active', 'white')],background=[('pressed', '!disabled', 'gray60'), ('active', 'gray50')])

   
  def update_app_style(self,s):
     
      self.style.set_theme(s)
#      self.style.theme_settings(s, {"TNotebook.Tab": {"configure": {"padding": [30, 15]}}})  
#      self.style.theme_settings(s, {'TButton': {"configure": {"padding": [30, 15]}}})
   
  def menuInit(self):
     
    menubar=tk.Menu(self.master)
    filemenu=tk.Menu(menubar,tearoff=0)    
    filemenu.add_command(label="New", command=lambda :self.newImage())                  
    filemenu.add_separator()
    filemenu.add_command(label="Save", command=lambda:self.save())
    filemenu.add_separator()
    filemenu.add_command(label="Save As", command=lambda:self.saveAs())
    filemenu.add_separator()
    menubar.add_cascade(label="File",menu=filemenu)
   
    skinmenu=tk.Menu(menubar,tearoff=0)
    for s in self.style.theme_names():
        print(s)
        skinmenu.add_command(label=s, command= partial(self.update_app_style , s))                  
    menubar.add_cascade(label="Skin",menu=skinmenu)
   
    self.master.config(menu=menubar)
   
#==============================================================================
# frames
#==============================================================================
  def centerFrame(self):
     
    self.canvas = tk.Canvas(self.center_frame,bg="gray60")
    self.canvas.place(relx=0,rely=0,relheight=1,relwidth=1)
    self.canvas.config(highlightbackground='gray60')
    self.canvas.bind("<Configure>", self.configure)
   
    self.canvasheight=self.canvas.winfo_height()
    self.canvaswidth=self.canvas.winfo_width()

  def topFrame(self):
     
     openimg=ImageTk.PhotoImage(file = r"icons/file.png")
     saveimg=ImageTk.PhotoImage(file = r"icons/save.png")    
     camimg=ImageTk.PhotoImage(file = r"icons/cam.png")    
     helpimg=ImageTk.PhotoImage(file = r"icons/help.png")    
     webimg=ImageTk.PhotoImage(file = r"icons/web.png")    
     buyimg=ImageTk.PhotoImage(file = r"icons/buy.png")    
     
     topButton_style=self.style
     topButton_style.configure('B1.TButton',padding=[30,12],relif='flat')

     b1=ttk.Button(self.top_frame,image = openimg,style='B1.TButton',command=lambda :self.newImage())
     b1.grid()
     b1.image=openimg
     
     b2=ttk.Button(self.top_frame,style='B1.TButton',image = saveimg ,command=lambda :self.saveAs())      

     b2.grid(row=0,column=1)
     b2.image=saveimg
     

     b3=ttk.Button(self.top_frame,style='B1.TButton',image = camimg,command=lambda :self.winDisp())
     b3.grid(row=0,column=2)
     b3.image=camimg

     b4=ttk.Button(self.top_frame,style='B1.TButton',image = webimg)
     b4.grid(row=0,column=3)
     b4.image=webimg

     b5=ttk.Button(self.top_frame,style='B1.TButton',image = helpimg)
     b5.grid(row=0,column=4)
     b5.image=helpimg
     
     b6=ttk.Button(self.top_frame,style='B1.TButton',image = buyimg)
     b6.grid(row=0,column=5)
     b6.image=buyimg
     
     
  def bottomFrame(self):
     
      self.bottom_frame.grid_rowconfigure(0, weight=0)
      self.bottom_frame.grid_rowconfigure(1, weight=1)      
      self.bottom_frame.grid_columnconfigure(0, weight=1)
     
      bframe1=ttk.Frame(self.bottom_frame)
      bframe1.grid(row=0,column=0,sticky="NESW",padx=200)  
      bframe2=ttk.Frame(self.bottom_frame)
      bframe2.grid(row=1,column=0,sticky="NESW")  

      ttk.Button(bframe1,text='Select folder',command=lambda :self.changeFolder()).grid(row=0,column=0)
      ttk.Button(bframe1,text='Batch operation').grid(row=0,column=1)
     
      self.folderCanvas=tk.Canvas(bframe2,bg='gray20')
      self.folderCanvas.config(highlightbackground='gray20')

      self.scrollFolder = ttk.Scrollbar(self.folderCanvas, orient='horizontal', command=self.folderCanvas.xview)

      self.folderCanvas.pack(side='bottom',fill='both',expand=True)
      self.scrollFolder.pack(side='top',fill='both')

  def leftFrame(self):
     
      self.left_frame.grid_rowconfigure(0, weight=0)
      self.left_frame.grid_rowconfigure(1, weight=1)
      self.left_frame.grid_rowconfigure(2, weight=0)
      self.left_frame.grid_rowconfigure(3, weight=2)
      self.left_frame.grid_rowconfigure(4, weight=0)
     
      self.left_frame.grid_columnconfigure(0, weight=1)
      self.left_frame.grid_columnconfigure(1, weight=0)
     
      ttk.Label(self.left_frame,text='Dummy ').grid(row=0,column=0)      


      lframe1=ttk.Frame(self.left_frame)
      lframe1.grid(row=1,column=0,sticky="NESW")      
      self.faceDetectLabel=ttk.Label(self.left_frame,text='Detected Faces  0')
      self.faceDetectLabel.grid(row=2,column=0)          
      lframe2=ttk.Frame(self.left_frame)
      lframe2.grid(sticky="NESW",row=3,column=0)

      lframe2.grid_rowconfigure(0, weight=1)
      lframe2.grid_rowconfigure(1, weight=1)      
      lframe2.grid_columnconfigure(0, weight=1)
      lframe2.grid_columnconfigure(1, weight=1)
      lframe2.grid_propagate(0)

      self.faceCanvas=tk.Canvas(lframe2,bg='gray20')
      self.faceCanvas.config(highlightbackground='gray20')

      self.scrollFace = ttk.Scrollbar(self.faceCanvas, orient='vertical', command=self.faceCanvas.yview)


     
      self.faceCanvas.pack(side='left',fill='both',expand=True)
      self.scrollFace.pack(side='right',fill='y')
     
      btnFrame=ttk.Frame(self.left_frame)
      btnFrame.grid(row=4,column=0)
      ttk.Button(btnFrame,text='Save').grid()
      ttk.Button(btnFrame,text='Dummy').grid(row=0,column=1)
     
     
     
  def rightFrame(self):
     
   
    self.right_frame.grid_rowconfigure(0,weight=0)
    self.right_frame.grid_rowconfigure(1,weight=0)
    self.right_frame.grid_rowconfigure(2,weight=1)
   
    self.right_frame.grid_columnconfigure(0,weight=1)
    self.right_frame.grid_columnconfigure(0,weight=1)
   
    ttk.Label(self.right_frame,text='Histogram ').grid(row=0,column=0)      

   
    self.histCanvas=tk.Canvas(self.right_frame,bg='gray20',highlightcolor='black',width=self.histCanvasWidth,height=self.histCanvasHeight)
    self.histCanvas.grid(row=1,column=0,sticky='n')
    self.histCanvas.config(highlightbackground='gray20')
    self.histCanvas.bind("<ButtonPress-1>",lambda event: self.switch(self.editTab3,'hist'))
   
   
    self.mainTab = ttk.Notebook(self.right_frame,style='TNotebook')  
    self.mainTab.grid( row=2,column=0,sticky='wnes')
   
    self.cropTab = ttk.Frame(self.mainTab)
    self.cropTab.grid_rowconfigure(0, weight=0)
    self.cropTab.grid_columnconfigure(0, weight=1)

    self.editTab = ttk.Frame(self.mainTab)
    self.editTab.grid_rowconfigure(0, weight=1)
    self.editTab.grid_columnconfigure(0, weight=1)

   
    self.printTab = ttk.Frame(self.mainTab)

    self.mainTab.add(self.cropTab, text = "Crop", compound=tk.TOP)
    self.mainTab.add(self.editTab, text = "Edit")
    self.mainTab.add(self.printTab, text = "Print")


    cropButton = ttk.Button(self.cropTab, text='Crop',command=lambda:self.crop())
    cropButton.grid(row=0,column=0,sticky='n',pady=5,ipadx=30,ipady=15)
    faceButton = ttk.Button(self.cropTab, text='Face',command=lambda:self.face())
    faceButton.grid(row=1,column=0,sticky='n',pady=5,ipadx=30,ipady=15)
    mirrorButton = ttk.Button(self.cropTab, text='Flip',command=lambda:self.flip())
    mirrorButton.grid(row=2,column=0,sticky='n',pady=5,ipadx=30,ipady=15)
    flipButton = ttk.Button(self.cropTab, text='Rotate',command=lambda:self.rotate())
    flipButton.grid(row=3,column=0,sticky='n',pady=5,ipadx=30,ipady=15)
    resetButton = ttk.Button(self.cropTab, text='Reset',command=lambda:self.reset())
    resetButton.grid(row=4,column=0,sticky='n',pady=5,ipadx=30,ipady=15)


    self.editTab1=ttk.Frame(self.editTab)
    self.editTab1.grid_rowconfigure(0,weight=0)
    self.editTab1.grid_columnconfigure(0,weight=1)
    self.editTab1.grid(sticky='news')
    self.editTab1.grid(row=0,column=0)

    self.editTab1.grid_propagate(0)
   
   
    self.editTab2=ttk.Frame(self.editTab)
    self.editTab2.grid_rowconfigure(0,weight=0)
    self.editTab2.grid_columnconfigure(0,weight=1)
    self.editTab2.grid(sticky='news')
    self.editTab2.grid(row=0,column=0)

    self.editTab2.grid_propagate(0)
   
    self.editTab3=ttk.Frame(self.editTab)
    self.editTab3.grid_rowconfigure(0,weight=0)
    self.editTab3.grid_columnconfigure(0,weight=1)
    self.editTab3.grid(sticky='news')
    self.editTab3.grid(row=0,column=0)

    self.editTab3.grid_propagate(0)

   
    generalButton = ttk.Button(self.editTab1, text='General settings',command=lambda:self.switch(self.editTab2,'open'))
    generalButton.grid(row=0,column=0,pady=10,ipadx=30,ipady=20)
    setting1 = ttk.Button(self.editTab1, text=' settings 1',command=lambda:self.switch(self.editTab2))
    setting1.grid(row=1,column=0,pady=10)
    setting2 = ttk.Button(self.editTab1, text=' settings 2',command=lambda:self.switch(self.editTab2))
    setting2.grid(row=2,column=0,pady=10)
    setting3 = ttk.Button(self.editTab1, text=' settings 3',command=lambda:self.switch(self.editTab2))
    setting3.grid(row=3,column=0,pady=10)

    self.list = tk.StringVar()
    ttk.OptionMenu(self.editTab2, self.list, "Custom", "Dark", "White").grid(row=0,column=0,pady=5,ipadx=100)
    self.list.set("Custom")
   
    ttk.Label(self.editTab2, text='Brightness').grid(row=1,column=0,)
    self.bslider = tk.DoubleVar()
    ttk.Scale(self.editTab2, from_=0, to_=2, length=200,  variable=self.bslider,takefocus=False).grid(row=2,column=0,pady=5)
    self.bslider.set(1)
   
    ttk.Label(self.editTab2, text='Contrast').grid(row=3,column=0,)
    self.cslider = tk.DoubleVar()
    ttk.Scale(self.editTab2, from_=0, to_=2, length=200,  variable=self.cslider,takefocus=False).grid(row=4,column=0,pady=5)
    self.cslider.set(1)
   
    ttk.Label(self.editTab2, text='Saturation').grid(row=5,column=0,)
    self.sslider = tk.DoubleVar()
    ttk.Scale(self.editTab2, from_=0, to_=2, length=200,   variable=self.sslider,takefocus=False).grid(row=6,column=0,pady=5)
    self.sslider.set(1)
   
    ttk.Label(self.editTab2, text='Sharpen').grid()
    self.shslider = tk.DoubleVar()
    ttk.Scale(self.editTab2, from_=0, to_=2, length=200,  variable=self.shslider,takefocus=False).grid(pady=5)
    self.shslider.set(1)

    applyButton = ttk.Button(self.editTab2, text='Apply',command=lambda:self.switch(self.editTab1,'apply'))
    applyButton.grid(pady=0,ipadx=30,ipady=0)
    cancelButton = ttk.Button(self.editTab2, text='Cancel',command=lambda:self.switch(self.editTab1,'cancel'))
    cancelButton.grid(pady=5,ipadx=30,ipady=0)

#Histogram channel tab intalization    
    ttk.Label(self.editTab3, text='Red').grid(row=0,column=0,pady=5)
    self.redslider = tk.DoubleVar()
    ttk.Scale(self.editTab3, from_=0, to_=2, length=200,  variable=self.redslider,takefocus=False).grid(row=1,column=0,pady=5)
    self.redslider.set(1)

    ttk.Label(self.editTab3, text='Green').grid(row=2,column=0,pady=5)
    self.greenslider = tk.DoubleVar()
    ttk.Scale(self.editTab3, from_=0, to_=2, length=200,  variable=self.greenslider,takefocus=False).grid(row=3,column=0,pady=5)
    self.greenslider.set(1)

    ttk.Label(self.editTab3, text='Blue').grid(row=4,column=0,pady=5)
    self.blueslider = tk.DoubleVar()
    ttk.Scale(self.editTab3, from_=0, to_=2, length=200,  variable=self.blueslider,takefocus=False).grid(row=5,column=0,pady=5)
    self.blueslider.set(1)

    applyButton = ttk.Button(self.editTab3, text='Apply',command=lambda:self.switch(self.editTab1,'apply'))
    applyButton.grid(pady=0,ipadx=30,ipady=0)
    cancelButton = ttk.Button(self.editTab3, text='Cancel',command=lambda:self.switch(self.editTab1,'cancel'))
    cancelButton.grid(pady=5,ipadx=30,ipady=0)
   
    self.switch(self.editTab1,'close')


  def switch(self,frame,tab):
     
    frame.tkraise()      
    if tab=='open':
        self.settingstab='open'
        self.settings(tab)
    elif tab=='hist':
        self.settingstab='hist'
        self.settings(tab)
    elif tab=='apply':
        self.settingstab='apply'
    elif tab=='cancel':
        self.settingstab='cancel'
#==============================================================================
# settings
#==============================================================================
  def settings(self,tab):
     
      if self.list.get()=='Dark':
         
          self.bslider.set(2)
          self.cslider.set(2)
          self.sslider.set(2)
          self.shslider.set(2)
         
      if self.list.get()=='White':
         
          self.bslider.set(0)
          self.cslider.set(0)
          self.sslider.set(0)
          self.shslider.set(0)
         
      if self.settingstab=='open':
         
          self.tempimg=self.image
          enhancer1 = ImageEnhance.Brightness(self.tempimg)
          bimg = enhancer1.enhance(self.bslider.get())                                  
           
          enhancer2 = ImageEnhance.Contrast(bimg)
          cimg = enhancer2.enhance(self.cslider.get())

          enhancer3 = ImageEnhance.Color(cimg)
          simg = enhancer3.enhance(self.sslider.get())
         
          enhancer4 = ImageEnhance.Sharpness(simg)
          shimg = enhancer4.enhance(self.shslider.get())
         
          self.enhanced_im=shimg
          self.image = self.enhanced_im
         
         
         
          self.imageForTk=self.makeImageForTk()
          self.drawImage()
          self.image=self.tempimg
          self.canvas.after(100, lambda:self.settings(tab) )                
         
      if self.settingstab=='apply':
          self.image=self.enhanced_im
          self.imageForTk=self.makeImageForTk()
          self.drawImage()
          self.bslider.set(1)

         
      if self.settingstab=='cancel':
         
          self.image=self.tempimg
          self.imageForTk=self.makeImageForTk()
          self.drawImage()
         
          self.bslider.set(1)
          self.cslider.set(1)
          self.sslider.set(1)
          self.shslider.set(1)
          self.redslider.set(1)
          self.greenslider.set(1)
          self.blueslider.set(1)
         
         
      if self.settingstab=='hist':
          print(self.blueslider.get())
          self.tempimg=self.image
          R, G, B= self.image.split()
          enhancer5 = ImageEnhance.Brightness(R)
          Rc = enhancer5.enhance(self.redslider.get())
          enhancer6 = ImageEnhance.Brightness(G)
          Gc = enhancer6.enhance(self.greenslider.get())
          enhancer7 = ImageEnhance.Brightness(B)
          Bc = enhancer7.enhance(self.blueslider.get())

          self.enhanced_im =Image.merge(self.image.mode, (Rc, Gc, Bc))
          self.image = self.enhanced_im
         
          self.imageForTk=self.makeImageForTk()
          self.drawImage()
          self.image=self.tempimg
          self.canvas.after(100, lambda:self.settings(tab) )                

# =============================================================================
# Images display      
# =============================================================================
     
  def newImage(self):
       
        self.imageName= filedialog.askopenfilename()
        filetype=""
        try: filetype=imghdr.what(self.imageName)
        except:
           messagebox.showinfo(title="Image File",message="Choose an Image File!" , parent=self.master)
        # restrict filetypes to .jpg, .bmp, etc.
        self.path=os.path.split(self.imageName)[0]
       
        if filetype in ['jpeg', 'bmp', 'png', 'tiff']:            
            im= PIL.Image.open(self.imageName)
            self.image=im
            self.originalImage=im.copy()
            self.imageSize=im.size
             
            self.imageForTk=self.makeImageForTk()            
            self.drawImage()
           
            self.folderImg()
        self.faceDetect()
           
           
  def makeImageForTk(self):
    if self.image!=None:
           
        self.imageWidth=self.image.size[0]
        self.imageHeight=self.image.size[1]

        if self.imageWidth>self.imageHeight:
            resizedImage=self.image.resize((self.canvaswidth,int(round(float(self.imageHeight)*self.canvaswidth/self.imageWidth))))
            # store the scale so as to use it later
            self.imageScale=float(self.imageWidth)/self.canvaswidth
        else:
            resizedImage=self.image.resize((int(round(float(self.imageWidth)*self.canvasheight/self.imageHeight)),\
                                    self.canvasheight))
            self.imageScale=float(self.imageHeight)/self.canvasheight
        # we may need to refer to ther resized image atttributes again
        self.resizedIm=resizedImage
        return ImageTk.PhotoImage(resizedImage)

       
  def drawImage(self):
    if self.image!=None:        
        self.canvas.create_image(self.canvaswidth/2.0-self.resizedIm.size[0]/2.0,
                        self.canvasheight/2.0-self.resizedIm.size[1]/2.0,
                            anchor='nw', image=self.imageForTk)
        self.imageTopX=int(round(self.canvaswidth/2.0-self.resizedIm.size[0]/2.0))
        self.imageTopY=int(round(self.canvasheight/2.0-self.resizedIm.size[1]/2.0))

    self.displayHistogram()
   
  def displayHistogram0(self):
         
    margin=2    
    if self.image!=None:
       
        self.histCanvas.delete('all')
       
        im=self.image
       
        R, G, B=im.histogram()[:256], im.histogram()[256:512], im.histogram()[512:768]
        for i in range(len(R)):
            pixelNo=R[i]
            self.histCanvas.create_oval(i+margin, self.histCanvasHeight -pixelNo/100.0-1-margin, i+2+margin,self.histCanvasHeight-pixelNo/100.0+1-margin, fill="red", outline="red")
        for i in range(len(G)):
            pixelNo=G[i]
            self.histCanvas.create_oval(i+margin, self.histCanvasHeight -pixelNo/100.0-1-margin, i+2+margin, self.histCanvasHeight-pixelNo/100.0+1-margin, fill="green", outline="green")
        for i in range(len(B)):
            pixelNo=B[i]
            self.histCanvas.create_oval(i+margin, self.histCanvasHeight -pixelNo/100.0-1-margin, i+2+margin,self.histCanvasHeight-pixelNo/100.0+1-margin,fill="blue", outline="blue")


  def displayHistogram(self):
     
    margin=2    
    if self.image!=None:
        im=self.image
        self.histCanvas.delete('all')
        gray=im.convert('LA')
       
        GG=gray.histogram()        
        R, G, B=im.histogram()[:256], im.histogram()[256:512], im.histogram()[512:768]

        R1 =[(((z - min(R)) * (100 - 0)) / (max(R) - min(R))) + 0 for z in R]
        G1=[(((z1 - min(G)) * (self.histCanvasHeight - 0)) / (max(G) - min(G))) + 0 for z1 in G]
        B1=[(((z2 - min(B)) * (self.histCanvasHeight - 0)) / (max(B) - min(B))) + 0 for z2 in B]
        GG1=[(((z2 - min(GG)) * (self.histCanvasHeight - 0)) / (max(GG) - min(GG))) + 0 for z2 in GG]
           
        for i in range(len(GG1)):
            pixelNo=GG1[i]
            self.histCanvas.create_line(margin+i, self.histCanvasHeight, margin+i,abs(pixelNo-self.histCanvasHeight),fill="gray50")            
             
        for i in range(len(R1)):
            pixelNo=R1[i]
            self.histCanvas.create_line(margin+i, self.histCanvasHeight, margin+i,abs(pixelNo-self.histCanvasHeight),fill="red")

        for i in range(len(G1)):
            pixelNo=G1[i]
            self.histCanvas.create_line(margin+i, self.histCanvasHeight, margin+i,abs(pixelNo-self.histCanvasHeight),fill="green")

        for i in range(len(B1)):
            pixelNo=B1[i]
            self.histCanvas.create_line(margin+i, self.histCanvasHeight, margin+i,abs(pixelNo-self.histCanvasHeight),fill="blue")


  def changehistogram(self):
      print(0)
                     
  def winDisp(self):
    self.image.show()  
   
  def flip(self):
     
    if self.image!=None:
        self.image=ImageOps.mirror(self.image)
        self.imageForTk=self.makeImageForTk()            
        self.drawImage()

  def rotate(self):
     
       
    if self.image!=None:
        imageData=list(self.image.getdata())
        newData=[]
        newimg=PIL.Image.new(self.image.mode,(self.image.size[1], self.image.size[0]))
        for i in range(self.image.size[0]):
            addrow=[]
            for j in range(i, len(imageData), self.image.size[0]):
                addrow.append(imageData[j])
            addrow.reverse()
            newData+=addrow
           
        newimg.putdata(newData)
        self.image=newimg.copy()        
        self.imageForTk=self.makeImageForTk()            
        self.drawImage()
#==============================================================================
# Face detect    
#==============================================================================

   
  def faceDetect(self):
     
        self.facelist=[]
        img=self.image
        cv_img=numpy.array(img)
        cv_img2=cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        cv_img3=cv2.cvtColor(cv_img2, cv2.COLOR_BGR2GRAY)
       
#        face_cascade = cv2.CascadeClassifier('C:/Users/user/Anaconda3/Library/etc/haarcascades/haarcascade_frontalface_default.xml')
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
       
        faces = face_cascade.detectMultiScale(cv_img3, 1.3, 5)
       
       
        if len(faces) !=0:
                for (x,y,w,h) in faces:
                    temp=[y,h,x,w]                
                    roi_color = cv_img[y:y+h, x:x+w]
                    self.facelist.append([roi_color,temp])
                   
        self.faceDetectLabel.config(text='Detected Faces '+str(len(self.facelist)))
        self.faceLeftTabdisplay()
       
       
#==============================================================================
# folder        
#==============================================================================
       
       
  def faceLeftTabdisplay(self):
     
      self.faceCanvas.delete('all')
     
      button_style=self.style
      button_style.configure('B2.TButton',padding=[0,0],relif='flat')

     
      if len(self.facelist)!=0:
               
          for f ,faceIm in enumerate(self.facelist):                
            imm=PIL.ImageTk.PhotoImage(PIL.Image.fromarray(faceIm[0]).resize((100,100)))
            btn=tk.Button(self.faceCanvas,image=imm)#command = partial(faceButtonPress,canvas,faceWindow,f)

            self.faceCanvas.create_window(100, f*150, anchor='n', window=btn)
            self.faceCanvas.configure(scrollregion=self.faceCanvas.bbox('all'), yscrollcommand=self.scrollFace.set)
            self.faceCanvas.config(highlightbackground='black')
   
            btn.image=imm

  def folderImg(self):
    self.folderCanvas.delete('all')
    self.folderImages=[]

    path=self.path
    valid_images = [".jpg",".gif",".png",".tga",".pgm"]

    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        foldIm=cv2.imread(os.path.join(path,f))
        foldIm=cv2.cvtColor(foldIm, cv2.COLOR_RGB2BGR)
        foldIm=PIL.Image.fromarray(foldIm)

        self.folderImages.append(foldIm)
       
    if len(self.folderImages)!=0:
       
        bw=80
        bh=80
        for fl ,foldIm1 in enumerate(self.folderImages):
           
            foldIm1_Width=foldIm1.size[0]
            foldIm1_Height=foldIm1.size[1]

            if foldIm1_Width>100:
               
                refoldIm1=foldIm1.resize((bw,int(round(float(foldIm1_Height)*bh/foldIm1_Width))))
            else:
                refoldIm1=foldIm1.resize((int(round(float(foldIm1_Width)*bh/foldIm1_Height)),bh))
           
                     
            imf=PIL.ImageTk.PhotoImage(refoldIm1)
                                   
            btn2=tk.Button(self.folderCanvas,image=imf,width=bw,height=bh,bg='gray10',relief='flat',command = partial(self.changeImage,fl))#command = partial(faceButtonPress,canvas,faceWindow,f)
#            btn2=ttk.Button(self.folderCanvas,image=imf,style='B3.TButton')#command = partial(faceButtonPress,canvas,faceWindow,f)
#            btn2.grid()
            self.folderCanvas.create_window( fl*150,20, anchor='n', window=btn2)
            self.folderCanvas.configure(scrollregion=self.folderCanvas.bbox('all'), xscrollcommand=self.scrollFolder.set)
            self.folderCanvas.config(highlightbackground='black')
       
            btn2.image=imf
           
           
  def changeImage(self,fl):
     
      self.image=self.folderImages[fl]
      self.originalImage=self.folderImages[fl].copy()
      self.imageSize=self.folderImages[fl].size
     
      self.imageForTk=self.makeImageForTk()            
      self.drawImage()
      self.faceDetect()

  def changeFolder(self):
    newPath=''  
    newPath = filedialog.askdirectory()
    if len(newPath)!=0:
            self.path=newPath            
            self.folderImg()
    else:messagebox.showinfo(title="No Folder",message="Choose an Image Folder!" , parent=self.master)

         
#==============================================================================
# save
#==============================================================================

  def saveAs(self):
   
    if self.image!=None:
        filename=filedialog.asksaveasfilename(defaultextension=".png")
        im=self.image
        im.save(filename)

  def save(self):
    if self.image!=None:
        im=self.image
        im.save(self.imageName)
        print(self.imageName)
       
  def reset(self):
      self.image=self.originalImage
      self.imageForTk=self.makeImageForTk()            
      self.drawImage()


#==============================================================================
# crop
#==============================================================================
  def crop(self):
    self.croprect = None
    tk.messagebox.showinfo(title="Crop",message="Draw cropping rectangle and press Enter", parent=self.master)    
    if self.image!=None:
        self.canvas.bind("<ButtonPress-1>",lambda event: self.startCrop(event))    
        self.canvas.bind("<B1-Motion>",lambda event: self.drawCrop(event))
        self.canvas.bind("<ButtonRelease-1>",lambda event: self.endCrop(event))
     
  def startCrop(self,event):
   
    if self.croprect is not None:
        self.canvas.delete(self.croprect)
        self.startCropX=0
        self.startCropY=0
        self.tempCropX=0
        self.tempCropY=0
        self.endCropX=0
        self.endCropY=0
       
    self.startCropX=event.x
    self.startCropY=event.y
    self.croprect=self.canvas.create_rectangle(self.startCropX,self.startCropY,self.startCropX,self.startCropY, fill="green", stipple="gray50", width=0)
         
  def drawCrop(self,event):
     
        self.tempCropX=event.x
        self.tempCropY=event.y      
        self.canvas.coords( self.croprect, self.startCropX,self.startCropY,self.tempCropX,self.tempCropY)
        self.canvas.bind("<ButtonPress-1>",lambda event: self.startCrop(event))
       
  def endCrop(self,event):

#        canvas.data.endCrop=False
        self.endCropX=event.x
        self.endCropY=event.y
        self.canvas.itemconfig(  self.croprect,fill='black')
        self.master.bind("<Return>",lambda event: self.performCrop(event))
       
  def performCrop(self,event):
   
    self.image=self.image.crop(\
    (int(round((self.startCropX-self.imageTopX)*self.imageScale)),
    int(round((self.startCropY-self.imageTopY)*self.imageScale)),
    int(round((self.endCropX-self.imageTopX)*self.imageScale)),
    int(round((self.endCropY-self.imageTopY)*self.imageScale))))
   
    self.imageForTk=self.makeImageForTk()
    self.drawImage()
    self.canvas.delete(self.croprect)
    self.master.unbind("<Return>")
   
# =============================================================================
# Events
# =============================================================================

  def configure(self,event):
     
    self.canvas.delete("all")
    w, h = event.width, event.height        
    self.canvaswidth=w
    self.canvasheight=h
    self.imageForTk=self.makeImageForTk()
    self.drawImage()
   
   
     
root = tk.Tk()
app = App(root)
root.mainloop()