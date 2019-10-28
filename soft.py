from __future__ import division
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image,ImageTk ,ImageEnhance
import PIL
import imghdr
import numpy
import cv2
from functools import partial
import os
import cv2
#def getBool(event):
#    print(canvas.data.c.get())


def manualResize(canvas,char):
    
    print(char,canvas.data.h.get())  
    if canvas.data.image!=None:    
        
        if canvas.data.c.get()==1 and char == 'h':
            canvas.data.w.delete(0, 'end')      
            
        if canvas.data.c.get()==1 and char == 'w':
            canvas.data.h.delete(0, 'end')                
      

        if canvas.data.c.get()==1:
            
            dw=float(canvas.data.image.size[0]/canvas.data.image.size[1])
            dh=float(canvas.data.image.size[1]/canvas.data.image.size[0])
#            print(dw,dh,canvas.data.h.get())
#            
            if canvas.data.h.get()!='':
                canvas.data.w.delete(0, 'end')                
                if int(canvas.data.h.get()) >= 2 and char == 'e':
                    
                    neww=int(int(canvas.data.h.get())*dw)
                    canvas.data.w.insert(1,str(neww))
                    
                    timg=canvas.data.image.resize((neww,int(canvas.data.h.get())))
                    canvas.data.image=timg
                    canvas.data.imageForTk=makeImageForTk(canvas)
                    drawImage(canvas)
                    
            elif canvas.data.w.get()!='':
                canvas.data.h.delete(0, 'end')                
                if int(canvas.data.w.get()) >= 2 and char == 'e':
#                    
                    neww=int(int(canvas.data.w.get())*dh)
                    canvas.data.h.insert(1,str(neww))
                    
                    timg=canvas.data.image.resize((int(canvas.data.w.get()),neww))
                    canvas.data.image=timg
                    canvas.data.imageForTk=makeImageForTk(canvas)
                    drawImage(canvas)


        if canvas.data.c.get()==0:
        
            if canvas.data.h.get()!=''and canvas.data.w.get()!='':
               if int(canvas.data.h.get()) >= 2 and int(canvas.data.w.get()) >= 2 and char=='e':
                    timg=canvas.data.image.resize((int(canvas.data.w.get()),int(canvas.data.h.get())))
                    canvas.data.image=timg
                    canvas.data.imageForTk=makeImageForTk(canvas)
                    drawImage(canvas)
                    

       
        
    canvas.delete('all')
    
    makeImageForTk(canvas)
    drawImage(canvas)
    

def convertFace(canvas):
    face_cascade = cv2.CascadeClassifier('C:/Users/user/Anaconda3/Library/etc/haarcascades/haarcascade_frontalface_default.xml')
    path=canvas.data.infolder
    valid_images = [".jpg",".gif",".png",".tga",".pgm"]

    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        image=cv2.imread(os.path.join(path,f),0)
        image2=cv2.imread(os.path.join(path,f))
    
        
        faces = face_cascade.detectMultiScale(image, 1.3, 5)
        
        count=0
        for (x,y,w,h) in faces:
    #        img = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            
            roi_color = image2[y:y+h, x:x+w]
            a,b,_=roi_color.shape
            z=a*10//100
            temp=image2[y-z:y+h+z, x-z:x+w+z]
            
            resized=cv2.resize(temp,(200,200))
#            cv2.imshow('cc',resized)
#            cv2.waitKey(0)

            
            if count>0:
                ff=os.path.splitext(f)[0]
                fe=os.path.splitext(f)[1]            
                cv2.imwrite(canvas.data.outfolder+'/'+ff+str(count)+fe,resized)
            else:
                cv2.imwrite(canvas.data.outfolder+'/'+f,resized)           
            count=count+1
    

def inputfolder(canvas,inLabel):
    canvas.data.infolder = filedialog.askdirectory()
    inLabel.config(text=canvas.data.infolder)
    
    
def outputfolder(canvas,outLabel):
    canvas.data.outfolder = filedialog.askdirectory()
    outLabel.config(text=canvas.data.outfolder)


def Batch(canvas):
    
    SelectWindow = tk.Toplevel(canvas.data.mainWindow,height=300,width=300)
    SelectWindow.resizable(0,0)
    SelectWindow.title("Select Folder")
    
    inLabel=tk.Label(SelectWindow,text='',width=25)
    inLabel.place(relx=0.2,rely=0.3)
    inButton=tk.Button(SelectWindow,text='Select Input Folder',width=25,command = lambda : inputfolder(canvas,inLabel))
    inButton.place(relx=0.2,rely=0.2)
    
    outLabel=tk.Label(SelectWindow,text='',width=25)
    outLabel.place(relx=0.2,rely=0.6)

    outButton=tk.Button(SelectWindow,text='Select Output Folder',width=25,command = lambda : outputfolder(canvas,outLabel))
    outButton.place(relx=0.2,rely=0.5)
    
    convert=tk.Button(SelectWindow,text='convert',width=25, command = lambda : convertFace(canvas))
    convert.place(relx=0.2,rely=0.7)

   
# =============================================================================
# Save
# =============================================================================

def saveAs(canvas):
    if canvas.data.image!=None:
        filename=filedialog.asksaveasfilename(defaultextension=".jpg")
        im=canvas.data.image
        im.save(filename)

def save(canvas):
    if canvas.data.image!=None:
        im=canvas.data.image
        im.save(canvas.data.imageLocation)

# =============================================================================
# Reset
# =============================================================================

def reset(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    ### change back to original image
    if canvas.data.image!=None:
        canvas.data.image=canvas.data.originalImage.copy()
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

#==============================================================================
# Crop
#==============================================================================


def crop(canvas):
    canvas.data.rect=False
    canvas.data.cropPopToHappen=True
    tk.messagebox.showinfo(title="Crop",message="Draw cropping rectangle and press Enter" ,parent=canvas.data.mainWindow)    
    if canvas.data.image!=None:
        canvas.data.mainWindow.bind("<ButtonPress-1>",lambda event: startCrop(event, canvas))
        canvas.data.mainWindow.bind("<B1-Motion>",lambda event: drawCrop(event, canvas))
        canvas.data.mainWindow.bind("<ButtonRelease-1>",lambda event: endCrop(event, canvas))

def startCrop(event, canvas):
    print(canvas.data.cropPopToHappen)

    # detects the start of the crop rectangle
    if canvas.data.rect is not None:
            canvas.delete(canvas.data.rect)
       
    if canvas.data.endCrop==False and canvas.data.cropPopToHappen==True:
        canvas.data.startCropX=event.x
        canvas.data.startCropY=event.y
        canvas.data.rect=canvas.create_rectangle(canvas.data.startCropX,canvas.data.startCropY,canvas.data.startCropX,canvas.data.startCropY, fill="green", stipple="gray50", width=0)


def drawCrop(event,canvas):
    print(2)
    # keeps extending the crop rectange as the user extends
    # his desired crop rectangle
    if canvas.data.endCrop==False and canvas.data.cropPopToHappen==True:
        canvas.data.tempCropX=event.x
        canvas.data.tempCropY=event.y       
        canvas.coords( canvas.data.rect, canvas.data.startCropX,canvas.data.startCropY,canvas.data.tempCropX,canvas.data.tempCropY)
        canvas.data.mainWindow.bind("<ButtonPress-1>",lambda event: startCrop(event, canvas))

def endCrop(event, canvas):
    print(3)
    # set canvas.data.endCrop=True so that button pressed movements
    # are not caught anymore but set it to False when "Enter"
    # is pressed so that crop can be performed another time too
    if canvas.data.cropPopToHappen==True:
        canvas.data.endCrop=False
        canvas.data.endCropX=event.x
        canvas.data.endCropY=event.y
        canvas.itemconfig( canvas.data.rect,fill='black')
#        CropMsgBox = messagebox.askquestion (title="Crop Image",message="Crop the selected region ?" , parent=canvas.data.mainWindow)
        
#    if CropMsgBox=='yes':
#            lambda event: performCrop(event,canvas)           
    if canvas.data.rect is not None:
        canvas.data.mainWindow.bind("<Return>", lambda event: performCrop(event, canvas))

def performCrop(event,canvas):
    
    print(4)
    canvas.data.image=canvas.data.image.crop(\
    (int(round((canvas.data.startCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.startCropY-canvas.data.imageTopY)*canvas.data.imageScale)),
    int(round((canvas.data.endCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.endCropY-canvas.data.imageTopY)*canvas.data.imageScale))))
    canvas.data.endCrop=False
    canvas.data.cropPopToHappen=False
    canvas.data.imageForTk=makeImageForTk(canvas)
    canvas.delete(canvas.data.rect)

    drawImage(canvas)


#==============================================================================
# Sharpen
#==============================================================================
def closeSharpenWindow(canvas):
    
    if canvas.data.image!=None:
        canvas.data.image=canvas.data.bimage
        canvas.data.sharpenWindowClose=True


def changeSharpen(canvas, sharpenWindow, sharpenSlider):
        
    if canvas.data.sharpenWindowClose==True:
        sharpenWindow.destroy()
        canvas.data.sharpenWindowClose=False
        
    if canvas.data.image!=None and sharpenWindow.winfo_exists():
        
            sliderVal=sharpenSlider.get()
            scale = sliderVal

            bimg=canvas.data.image 
            enhancer = ImageEnhance.Sharpness(bimg)
            enhanced_im = enhancer.enhance(scale)                 
            canvas.data.image = enhanced_im
            canvas.data.bimage = enhanced_im
            
            
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            canvas.data.image=bimg            
            
            canvas.after(100, lambda: changeSharpen(canvas, sharpenWindow, sharpenSlider))       

def sharpen(canvas):
    
    sharpenWindow=tk.Toplevel(canvas.data.mainWindow)
    sharpenWindow.title("Sharpen")

    mainframe = ttk.Frame(sharpenWindow, padding="24 24 24 24")
    mainframe.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))
    
    slider = tk.DoubleVar()
    ttk.Scale(mainframe, from_=1, to_=10, length=500,  variable=slider).grid(column=1, row=4, columnspan=1)
    ttk.Label(mainframe, textvariable=slider).grid(column=1, row=0, columnspan=5)
    tk.Button(mainframe, width=20,text="OK", command=lambda: closeSharpenWindow(canvas)).grid(column=1, row=5, columnspan=5)
    slider.set(1)
    
    changeSharpen(canvas, sharpenWindow, slider)

#==============================================================================
# Sauration
#==============================================================================
    
def closeSaturationWindow(canvas):
    
    if canvas.data.image!=None:
        
        canvas.data.image=canvas.data.bimage
        canvas.data.saturationWindowClose=True

def changeSaturation(canvas, saturationWindow, saturationSlider):
        
    if canvas.data.saturationWindowClose==True:
        saturationWindow.destroy()
        canvas.data.saturationWindowClose=False
        
    if canvas.data.image!=None and saturationWindow.winfo_exists():
        
            sliderVal=saturationSlider.get()
            scale = sliderVal

            bimg=canvas.data.image 
            enhancer = ImageEnhance.Color(bimg)
            enhanced_im = enhancer.enhance(scale)  
               
            canvas.data.image = enhanced_im
            canvas.data.bimage = enhanced_im
            
            
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            canvas.data.image=bimg            
            
            canvas.after(100, lambda: changeSaturation(canvas, saturationWindow, saturationSlider))       

def saturation(canvas):
    
    saturationWindow=tk.Toplevel(canvas.data.mainWindow)
    saturationWindow.title("saturation")

    mainframe = ttk.Frame(saturationWindow, padding="24 24 24 24")
    mainframe.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))
    
    slider = tk.DoubleVar()
    ttk.Scale(mainframe, from_=0, to_=2, length=500,  variable=slider).grid(column=1, row=4, columnspan=1)
    ttk.Label(mainframe, textvariable=slider).grid(column=1, row=0, columnspan=5)
    tk.Button(mainframe, width=20,text="OK", command=lambda: closeSaturationWindow(canvas)).grid(column=1, row=5, columnspan=5)
    slider.set(1)
    changeSaturation(canvas, saturationWindow, slider)

#==============================================================================
# Contrast
#==============================================================================
    
def closeContrastWindow(canvas):
    
    if canvas.data.image!=None:
        canvas.data.image=canvas.data.bimage
        canvas.data.contrastWindowClose=True
        
def changeContrast(canvas, contrastWindow, contrastSlider):
        
    if canvas.data.contrastWindowClose==True:
        contrastWindow.destroy()
        canvas.data.contrastWindowClose=False
        
    if canvas.data.image!=None and contrastWindow.winfo_exists():
        
            sliderVal=contrastSlider.get()
            scale = sliderVal

            bimg=canvas.data.image
            
            enhancer = ImageEnhance.Contrast(bimg)
            enhanced_im = enhancer.enhance(scale)                        
            canvas.data.image = enhanced_im
            canvas.data.bimage = enhanced_im
            
            
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            canvas.data.image=bimg            
            
            canvas.after(100, lambda: changeContrast(canvas, contrastWindow, contrastSlider))       

def contrast(canvas):
    
    contrastWindow=tk.Toplevel(canvas.data.mainWindow)
    contrastWindow.title("contrast")

    mainframe = ttk.Frame(contrastWindow, padding="24 24 24 24")
    mainframe.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))
    
    slider = tk.DoubleVar()
    ttk.Scale(mainframe, from_=0, to_=3, length=500,  variable=slider).grid(column=1, row=4, columnspan=1)
    ttk.Label(mainframe, textvariable=slider).grid(column=1, row=0, columnspan=5)
    tk.Button(mainframe, width=20,text="OK", command=lambda: closeContrastWindow(canvas)).grid(column=1, row=5, columnspan=5)
    slider.set(1)
    changeContrast(canvas, contrastWindow, slider)
    
#==============================================================================
#     Brightness
#==============================================================================

def closeBrightnessWindow(canvas):
    
    if canvas.data.image!=None:
        canvas.data.image=canvas.data.bimage
        canvas.data.brightnessWindowClose=True


def changeBrightness(canvas, brightnessWindow, brightnessSlider):
        
    if canvas.data.brightnessWindowClose==True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose=False
        
    if canvas.data.image!=None and brightnessWindow.winfo_exists():
        
            sliderVal=brightnessSlider.get()
            scale = sliderVal
            
            bimg=canvas.data.image
            enhancer = ImageEnhance.Brightness(bimg)
            enhanced_im = enhancer.enhance(scale)                        
            canvas.data.image = enhanced_im
            canvas.data.bimage = enhanced_im
            
            
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            canvas.data.image=bimg            
            
            canvas.after(100, lambda: changeBrightness(canvas, brightnessWindow, brightnessSlider))                   
def brightness(canvas):

    brightnessWindow=tk.Toplevel(canvas.data.mainWindow)
    brightnessWindow.title("Brightness")

    mainframe = ttk.Frame(brightnessWindow, padding="24 24 24 24")
    mainframe.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))

    slider = tk.DoubleVar()
    ttk.Scale(mainframe, from_=0, to_=2, length=400,  variable=slider).grid(column=1, row=4, columnspan=1)
    ttk.Label(mainframe, textvariable=slider).grid(column=1, row=0, columnspan=5)
    tk.Button(mainframe, width=20,text="OK", command=lambda: closeBrightnessWindow(canvas)).grid(column=1, row=5, columnspan=5)
    slider.set(1)
    changeBrightness(canvas, brightnessWindow, slider)

#==============================================================================
# Face    
#==============================================================================
    
def closeFace(canvas,faceAdjustWindow):
    
     canvas.data.image=canvas.data.bimage  
     canvas.data.imageForTk=makeImageForTk(canvas)
     drawImage(canvas)
     canvas.data.closeFace=True

    
def faceEdit(canvas,t,y,b,l,x,r,faceAdjustWindow,faceCanvas,topSlider,bottomSlider,LeftSlider,RightSlider):
    
    if canvas.data.closeFace==True:
        faceAdjustWindow.destroy()
        canvas.data.closeFace=False

    else:
        faceHeight=400
        faceWidth=400
        
        faceImg0=numpy.array(canvas.data.image)
        faceImg=PIL.Image.fromarray(faceImg0[t:y+b,l:x+r])
        
        fimWidth=faceImg.size[0]
        fimHeight=faceImg.size[1]
        
        faceCanvas1=tk.Canvas(faceCanvas,bg='gray')
        faceCanvas1.place(relx=0.5,rely=0.5,width=faceWidth,height=faceHeight,anchor="center")        
        
        if fimWidth>fimHeight:
                fImage=faceImg.resize((faceWidth,int(round(float(fimHeight)*faceWidth/fimWidth))))
        else:
                fImage=faceImg.resize((int(round(float(fimWidth)*faceHeight/fimHeight)),faceHeight))
        
        faceImg1=ImageTk.PhotoImage(fImage)
        faceCanvas1.create_image(faceWidth/2.0-fImage.size[0]/2.0,faceHeight/2.0-fImage.size[1]/2.0,anchor='nw', image=faceImg1)
        faceCanvas1.image=faceImg1
        canvas.data.bimage=fImage
        
        
        t1=topSlider.get()    
        b1=bottomSlider.get()
        l1=LeftSlider.get()
        r1=RightSlider.get()
        
        
        canvas.after(100, lambda: faceEdit(canvas,t1,y,b1,l1,x,r1,faceAdjustWindow,faceCanvas,topSlider,bottomSlider,LeftSlider,RightSlider))


def faceButtonPress(canvas,faceWindow,z):
    
    
    MsgBox = messagebox.askquestion (title="Image File",message="select this image" , parent=faceWindow)
    if MsgBox == 'yes':
        faceWindow.destroy()

        faceHeight=500
        faceWidth=500
        
        y,h,x,w=canvas.data.facelist[z][1]
    
        faceAdjustWindow = tk.Toplevel(canvas.data.mainWindow,height=faceHeight,width=faceWidth)
        faceAdjustWindow.title("Face Adjust")
        faceAdjustWindow.resizable(0,0)
        
        faceCanvas=tk.Canvas(faceAdjustWindow,height=faceHeight,width=faceWidth,bg='gray')
        faceCanvas.pack(side='left')
        
        topSlider=tk.Scale(faceAdjustWindow,from_=0, to=canvas.data.imageSize[1],orient=tk.HORIZONTAL)
        topSlider.pack()
        topSlider.set(y)
        
        bottomSlider=tk.Scale(faceAdjustWindow,from_=0, to=canvas.data.imageSize[1],orient=tk.HORIZONTAL)
        bottomSlider.pack()
        bottomSlider.set(h)
    
    
        LeftSlider=tk.Scale(faceAdjustWindow,from_=0, to=canvas.data.imageSize[0],orient=tk.HORIZONTAL)
        LeftSlider.pack()
        LeftSlider.set(x)
        
        RightSlider=tk.Scale(faceAdjustWindow,from_=0, to=canvas.data.imageSize[0],orient=tk.HORIZONTAL)
        RightSlider.pack()
        RightSlider.set(w)
        
        OkButton=tk.Button(faceAdjustWindow,width=10, text='Apply',command=lambda: closeFace(canvas,faceAdjustWindow))
        OkButton.pack()
        
        t=y
        b=h
        l=x
        r=w
    
        faceEdit(canvas,t,y,b,l,x,r,faceAdjustWindow,faceCanvas,topSlider,bottomSlider,LeftSlider,RightSlider)
    
#    img3=PIL.Image.fromarray(canvas.data.facelist[z])  
#    canvas.data.image=img3    
#    canvas.data.imageSize=img3.size
#    canvas.data.imageForTk=makeImageForTk(canvas)
#    drawImage(canvas)
    
def faceButtondisplay(canvas):
    
    faceWindow=tk.Toplevel(canvas.data.mainWindow)
    faceWindow.title("Detected Faces")
    
    faceframe = tk.Frame(faceWindow)
    faceframe.grid(column=0, row=0, sticky=('n', 'w', 'e', 's'))
    
    for f ,faceIm in enumerate(canvas.data.facelist):
        
        imm=PIL.ImageTk.PhotoImage(PIL.Image.fromarray(faceIm[0]).resize((200,200)))
        btn=tk.Button(faceframe,image=imm, command = partial(faceButtonPress,canvas,faceWindow,f))
        btn.grid(column=f, row=0)
        btn.image=imm


def faceDetect(canvas):
    try:        
        canvas.data.facelist=[]
        canvas.data.cropPopToHappen=False    
        img=canvas.data.image
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
                    canvas.data.facelist.append([roi_color,temp])                 
                faceButtondisplay(canvas)
        else:
            tk.messagebox.showinfo(title="No Face Detected",message="No Face Detected in Image or Image bad Quality!" , parent=canvas.data.mainWindow)
    except:
           tk.messagebox.showinfo(title="Image File",message="No Image File!" , parent=canvas.data.mainWindow)
#==============================================================================
# 
#==============================================================================
def configure(event):
    
    canvas.delete("all")
    w, h = event.width, event.height
    print(w,h)
        
    canvas.data.width=w
    canvas.data.height=h
    canvas.data.imageForTk=makeImageForTk(canvas)

    drawImage(canvas)

    

def displayHistogram(canvas):
    
    margin=0    
    if canvas.data.image!=None:
        histCanvas.delete('all')
        
        im=canvas.data.image
        #x-axis 
        histCanvas.create_line(margin-1, histCanvasHeight-margin+1,margin-1+ 258, histCanvasHeight-margin+1)
        xmarkerStart=margin-1
        
        for i in range(0,257,64):
            xmarker="%d" % (i)
        #y-axis
        histCanvas.create_line(margin-1, histCanvasHeight-margin+1, margin-1, margin)
        ymarkerStart= histCanvasHeight-margin+1
        for i in range(0, histCanvasHeight-2*margin+1, 50):
            ymarker="%d" % (i)            
        R, G, B=im.histogram()[:256], im.histogram()[256:512], im.histogram()[512:768]
        for i in range(len(R)):
            pixelNo=R[i]
            histCanvas.create_oval(i+margin, histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,histCanvasHeight-pixelNo/100.0+1-margin, fill="red", outline="red")
        for i in range(len(G)):
            pixelNo=G[i]
            histCanvas.create_oval(i+margin, histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin, histCanvasHeight-pixelNo/100.0+1-margin, fill="green", outline="green")
        for i in range(len(B)):
            pixelNo=B[i]
            histCanvas.create_oval(i+margin,histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,histCanvasHeight-pixelNo/100.0+1-margin,fill="blue", outline="blue")


def drawImage(canvas):
    if canvas.data.image!=None:
        # make the canvas center and the image center the same
        canvas.create_image(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0,
                        canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0,
                            anchor='nw', image=canvas.data.imageForTk)

        
        canvas.data.imageTopX=int(round(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0))
        canvas.data.imageTopY=int(round(canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0))
        displayHistogram(canvas)


def makeImageForTk(canvas):
    im=canvas.data.image
    if canvas.data.image!=None:
        # Beacuse after cropping the now 'image' might have diffrent
        # dimensional ratios
            
        imageWidth=canvas.data.image.size[0] 
        imageHeight=canvas.data.image.size[1]
        #To make biggest version of the image fit inside the canvas
        if imageWidth>imageHeight:
            resizedImage=im.resize((canvas.data.width,int(round(float(imageHeight)*canvas.data.width/imageWidth))))
            # store the scale so as to use it later
            canvas.data.imageScale=float(imageWidth)/canvas.data.width
        else:
            resizedImage=im.resize((int(round(float(imageWidth)*canvas.data.height/imageHeight)),\
                                    canvas.data.height))
            canvas.data.imageScale=float(imageHeight)/canvas.data.height
        # we may need to refer to ther resized image atttributes again
        canvas.data.resizedIm=resizedImage
        return ImageTk.PhotoImage(resizedImage)
        
def newImage(canvas):
    
    imageName= filedialog.askopenfilename()
    filetype=""
    try: filetype=imghdr.what(imageName)
    except:
       messagebox.showinfo(title="Image File",message="Choose an Image File!" , parent=canvas.data.mainWindow)
    # restrict filetypes to .jpg, .bmp, etc.
    if filetype in ['jpeg', 'bmp', 'png', 'tiff']:
        
        canvas.data.imageLocation=imageName
        im= PIL.Image.open(imageName)
        canvas.data.image=im
        canvas.data.originalImage=im.copy()
        canvas.data.imageSize=im.size #Original Image dimensions
        
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

        
def init(root, canvas):
  
    canvas.data.image=None
    canvas.data.originalImage=None
    canvas.data.resizedIm=None
    canvas.data.bimage=None
    canvas.data.width=None
    canvas.data.height=None

    canvas.data.brightnessWindowClose=False
    canvas.data.closeFace=False
    canvas.data.sharpenWindowClose=False
    canvas.data.contrastWindowClose=False
    canvas.data.saturationWindowClose=False
    canvas.data.cropPopToHappen=False
    canvas.data.endCrop=False
    
    canvas.data.rect=None
    canvas.data.facelist=[]
    canvas.data.h=None
    canvas.data.w=None

def menuInit(root, canvas):
    
    menubar=tk.Menu(root)
    filemenu=tk.Menu(menubar,tearoff=0) 
    
    filemenu.add_command(label="New", command=lambda:newImage(canvas))                   
    filemenu.add_separator()
    filemenu.add_command(label="Save", command=lambda:save(canvas))
    filemenu.add_separator()
    filemenu.add_command(label="Save As", command=lambda:saveAs(canvas))
    filemenu.add_separator()
    filemenu.add_command(label="Batch Process", command=lambda:Batch(canvas))
  
    menubar.add_cascade(label="File",menu=filemenu)
    
    root.config(menu=menubar)


def buttonsInit(canvas,root, toolKitFrame): 
    
    backgroundColour="#474747"
    foregroundColour="white"   
    buttonWidth=20
    buttonHeight=2
    
    heightEntryL = tk.Label(toolKitFrame, text="Height",bg=backgroundColour ,fg=foregroundColour)
    heightEntryL.grid(row=1,column=0)   
    heightEntry=tk.Entry(toolKitFrame)
    heightEntry.grid(row=2,column=0)
    heightEntry.bind("<Return>",lambda _:manualResize(canvas,'e'))
    heightEntry.bind("<Key>",lambda _:manualResize(canvas,'h'))


    canvas.data.h=heightEntry
    
    

    widthEntryL = tk.Label(toolKitFrame, text="Width",bg=backgroundColour ,fg=foregroundColour)
    widthEntryL.grid(row=3,column=0)    
    widthEntry=tk.Entry(toolKitFrame)
    widthEntry.grid(row=4,column=0)    
    widthEntry.bind("<Key>",lambda _:manualResize(canvas,'w'))
    widthEntry.bind("<Return>",lambda _:manualResize(canvas,'e'))

    canvas.data.w=widthEntry
    
    canvas.data.c=tk.IntVar()
    chec=tk.Checkbutton(toolKitFrame,text='Fixed ratio',bg=backgroundColour ,activebackground=backgroundColour,fg=foregroundColour,selectcolor='black',variable=canvas.data.c)
    chec.grid(row=5,column=0)
#    chec.bind("<Button-1>", getBool)
       
    cropButton=tk.Button(toolKitFrame, text="Crop",highlightcolor='white',bg=backgroundColour ,fg=foregroundColour,width=buttonWidth, height=buttonHeight,command=lambda:crop(canvas))
    cropButton.grid(row=6,column=0)
    brightnessButton=tk.Button(toolKitFrame, text="Brightness",background=backgroundColour ,fg=foregroundColour,width=buttonWidth, height=buttonHeight,command=lambda: brightness(canvas))
    brightnessButton.grid(row=7,column=0) 
    ContrastButton=tk.Button(toolKitFrame, text="contrast",background=backgroundColour ,fg=foregroundColour,width=buttonWidth, height=buttonHeight,command=lambda: contrast(canvas))
    ContrastButton.grid(row=8,column=0)
    SaturationButton=tk.Button(toolKitFrame, text="saturation",background=backgroundColour ,fg=foregroundColour,width=buttonWidth, height=buttonHeight,command=lambda: saturation(canvas))
    SaturationButton.grid(row=9,column=0)
    SharpenButton=tk.Button(toolKitFrame, text="sharpen",background=backgroundColour ,fg=foregroundColour,width=buttonWidth, height=buttonHeight,command=lambda: sharpen(canvas))
    SharpenButton.grid(row=10,column=0)   
    faceButton=tk.Button(toolKitFrame, text="Face",background=backgroundColour ,fg=foregroundColour,width=buttonWidth, height=buttonHeight,command=lambda: faceDetect(canvas))
    faceButton.grid(row=11,column=0)
    resetButton=tk.Button(toolKitFrame, text="Reset",background=backgroundColour ,fg=foregroundColour,width=buttonWidth, height=buttonHeight, command=lambda: reset(canvas))
    resetButton.grid(row=12,column=0)
        


root = tk.Tk()
root.title("Image Editor by AUG")
root.configure(bg="black")
root.geometry('800x600')
root.minsize(800,600)

canvasbg = tk.Canvas(root,bg="#a19f9f")
canvasbg.place(relx=0,rely=0,relheight=1,relwidth=0.95)

canvas = tk.Canvas(canvasbg,bg="white")
canvas.place(relx=0.5, rely=0.5,relheight=0.7,relwidth=0.6 ,anchor="center")
toolKitFrame=tk.Frame(root,bg='#474747')    
toolKitFrame.pack(side='right',fill='both')

histCanvasHeight=90
histCanvasWidth=160
histCanvas=tk.Canvas(toolKitFrame,width=histCanvasWidth, height=histCanvasHeight,bg='gray20')
histCanvas.grid(row=0,column=0)


class Struct: pass
canvas.data = Struct()
canvas.data.mainWindow=root
init(root, canvas)

canvas.bind("<Configure>", configure)
menuInit(root, canvas)
buttonsInit(canvas,root, toolKitFrame)

root.mainloop()
