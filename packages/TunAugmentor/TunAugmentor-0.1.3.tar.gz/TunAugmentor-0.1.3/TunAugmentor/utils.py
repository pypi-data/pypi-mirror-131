import  cv2
import glob

def is_rgb_image(image):
    return len(image.shape) == 3 and image.shape[-1] == 3

def is_grayscale_image(image):
    return (len(image.shape) == 2) or (len(image.shape) == 3 and image.shape[-1] == 1)

def read_images(path):
    images=[]
    files = glob.glob (path+"/*.jpg")
    for myFile in files:
        image = cv2.imread(myFile)
        images.append(image)
    return images

def read_image(path):
    image=[cv2.imread(path)]
    return image
def export(images,path,base="img"):
    i=0
    res=True
    for im in images:
        i+=1
        img_name='/'+base+str(i)+'.jpg'
        res=cv2.imwrite(path+img_name,im) and res
    return res