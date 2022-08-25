from __future__ import division
from PIL import Image
from random import randint
from collections import deque

def rubics_operation(image, k):
    j = 0
    while j < len(image):
        sum_pix = sum(image[j])
        x = deque(image[j])
        if sum_pix % 2 == 0:
            x.rotate(-k)
        else:
            x.rotate(k)

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

def operation():
    return "unscramble"

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
                idx[i]=idx[i-x]
                idx[i-x]=z
            else:
                z=idx[i]
                idx[i]=idx[i-y]
                idx[i-y]=z
    return idx

def scramblePixels(img):
    seed(img)
    pxs = getPixels(img)
    idx = scrambledIndex(pxs)
    out = []
    for i in idx:
        out.append(pxs[i])
    return out

def unScramblePixels(img,x,y):
    pxs = getPixels(img)
    idx = scrambledIndex(pxs,x,y)
    out = list(range(len(pxs)))
    cur = 0
    for i in idx:
        out[i] = pxs[cur]
        cur += 1
    return out

def storePixels(name, size, pxs):
    outImg = Image.new("RGB", size)
    w, h = size
    pxIter = iter(pxs)
    for x in range(w):
        for y in range(h):
            outImg.putpixel( (x, y), next(pxIter))
    outImg.save(name)

def imgDecrypt(file_name, iterations, kr, kc):
    #file_name = input("enter the file name to be decrypt:\t")
    im = Image.open("enc_result/"+file_name)
    pixels = list(im.getdata())
    grey_image1 = list()
    for pix in pixels:
        grey_image1.append(int(pix[0]))
    grey_image2 = list()
    sp = 0
    for rows in range(im.size[1]):
        fp = sp + im.size[0]
        x = grey_image1[sp:fp]
        sp = fp
        grey_image2.append(x)

  
    
    #kr = int(input("kr : "))
    #kc = int(input("kc : "))
  
    if operation() == "unscramble":
        pxs = unScramblePixels(im,kr,kc)
        #storePixels("unscrambled.png", im.size, pxs)
    else:
        sys.exit("Unsupported operation: " + operation())

    itr = iterations
    i = 0
    while i < itr:
        i += 1

        grey_image2 = xor_operation(grey_image2, kc)
        grey_image2 = row_col_inversion(grey_image2)
        grey_image2 = xor_operation(grey_image2, kr)
        grey_image2 = row_col_inversion(grey_image2)
        grey_image2 = rubics_operation(grey_image2, kc)
        grey_image2 = row_col_inversion(grey_image2)
        grey_image2 = rubics_operation(grey_image2, kr)


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

    im.putdata(grey_image4)
    im.save("dec_result/" + file_name)
    print("decryption done")
