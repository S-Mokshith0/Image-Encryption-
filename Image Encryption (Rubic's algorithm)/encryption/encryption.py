from __future__ import division         # change the / operator to mean true division throughout the module.  always floating point result
from PIL import Image
from random import randint
from collections import deque
import smtplib
from PIL import Image
import sys
import os
import random



def rubics_operation(image, k):
    j = 0
    while j < len(image):
        sum_pix = sum(image[j])
        x = deque(image[j])                     #adding and removing elements from either end
        if sum_pix % 2 == 0:
            x.rotate(k)
        else:
            x.rotate(-k) 

        image[j] = list(x)
        j +=1

    return image


def row_col_inversion(image):
    other = list()
    temp = list()
    i = 0
    while i < len(image[0]):
        temp = []
        for row in image:
            temp.append(row[i])
        other.append(temp)
        i += 1

    return other


def xor_operation(image, k):
    i = 1
    for row in image:
        if i % 2 == 0:
            j = 0
            temp_k = 255 - k
            for pix in row:
                row[j] = temp_k ^ pix
                j += 1
        else:
            j = 0
            for pix in row:
                row[j] = k ^ pix
                j += 1
    i += 1

    return image

    
def send_email(email, kr, kc, itr):
    email_adderss = 'senkumokshith2002'
    email_password = 'senkumokshith4687'

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email_adderss, email_password)

        subject = "Image Encryption"
        body = 'Image encrypted successfully! kr = ', kr, ' kc = ', kc, 'Number of Iterations = ', itr

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(email_adderss, email, msg)    
def operation():
    return "scramble"

def seed(img):
    random.seed(hash(img.size))

def getPixels(img):
    w, h = img.size
    pxs = []
    for x in range(w):
        for y in range(h):
            pxs.append(img.getpixel((x, y)))
    return pxs

def scrambledIndex(pxs,x,y):
    idx = list(range(len(pxs)))
    for  i in range(int(len(pxs)/2)):
        if(i==idx[i]):
            if(i%2==0):
                z=idx[i]
                idx[i]=idx[i+x]
                idx[i+x]=z
            else:
                z=idx[i]
                idx[i]=idx[i+y]
                idx[i+y]=z
    return idx

def scramblePixels(img,x,y):
    pxs = getPixels(img)
    idx = scrambledIndex(pxs,x,y)
    out = []
    for i in idx:
        out.append(pxs[i])
    return out



def storePixels(name, size, pxs):
    outImg = Image.new("RGB", size)
    w, h = size
    pxIter = iter(pxs)
    for x in range(w):
        for y in range(h):
            outImg.putpixel( (x, y), next(pxIter))
    outImg.save(name)


def inputImg(file_name, itr, email):
    #file_name = input("enter the file name to be encrypt:\t")
    im = Image.open(file_name)#simage details
    
    pixels = list(im.getdata())
    grey_image1 = list()
    grey_image1_value=list()
    count=0
    for pix in pixels:
        grey_image1.append(int(pix[0]))
        count=count+1
        grey_image1_value.append(count)
    grey_image2 = list()
    grey_image2_value=list()
    sp = 0
    count=0
    for rows in range(im.size[1]):
        fp = sp + im.size[0]            #length or size of list
        x = grey_image1[sp:fp]
        y=grey_image1_value[sp:fp]
        sp = fp
        grey_image2.append(x)
        grey_image2_value.append(y)

    #itr = int(input("enter the no of iterations :\t"))
    kr = randint(1, 255)

    kc = randint(1, 255)

    print("random integers are " + str(kr) + " , " + str(kc))

    send_email(email, kr, kc, itr)
    

    if operation() == "scramble":
        pxs = scramblePixels(im,kr,kc)
        #storePixels("scrambled.png", im.size, pxs)
    
    else:
        sys.exit("Unsupported operation: " + operation())
    
    i = 0

    while i < itr:
        i += 1

        grey_image2 = rubics_operation(grey_image2, kr)

        grey_image2 = row_col_inversion(grey_image2)

        grey_image2 = rubics_operation(grey_image2, kc)

        grey_image2 = row_col_inversion(grey_image2)

        grey_image2 = xor_operation(grey_image2 , kr)

        grey_image2 = row_col_inversion(grey_image2)

        grey_image2 = xor_operation(grey_image2 , kc)
    


   
    grey_image3 = list()
    for row in grey_image2:
        for pix in row:
            grey_image3.append(pix)

    grey_image4 = list()

    for pix in grey_image3:
        x = (pix, pix, pix)
        grey_image4.append(x)
    # generating the output

    x, y = im.size
    im2 = Image.new("RGB", (x, y))

    im2.putdata(grey_image4)
    im2.save("enc_result/" + file_name)

    print("encryption done")


