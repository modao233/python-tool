from PIL import Image

#填充图片成正方形
def fill_image(image):
    width, height = image.size
    # 选取较大值作为矩形图片的边长
    new_image_length = width if width > height else height
    #生成新图片，白底
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    #将之前的图片粘贴在新图上，居中
    if width > height:#(upper, left)
        new_image.paste(image, (0, int((new_image_length - height)/2)))
    else:
        new_image.paste(image, (int((new_image_length - width)/2), 0))

    return new_image

def cut_image(image):
    width, height = image.size
    item_width = int(width/3)
    item_height = int(width/3)
    box_list = []
    for i in range(0, 3):
        for j in range(0, 3):#四元组(左边距，上边距，右边距， 下边距)
            box = (j*item_width, i*item_height, (j+1)*item_width, (i+1)*item_height)
            box_list.append(box)
        image_list = [image.crop(box) for box in box_list]
    return image_list

def save_images(image_list):
    index = 1
    for image in image_list:
        image.save('D:/python-download/wechat-photo/' + str(index) + '.png')
        index += 1

file_path = 'C:/Users/modao/Desktop/QQ图片20190822145840.jpg'
image = Image.open(file_path)
image = fill_image(image)
image_list = cut_image(image)
new_list = []
for image in image_list:
    image = fill_image(image)
    new_list.append(image)
save_images(new_list)


