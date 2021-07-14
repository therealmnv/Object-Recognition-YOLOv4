from xml.etree import ElementTree
import os

folder = 'annotations'
output_path = 'newAnnotations/'
classes = ['head', 'helmet']

flag = 0

for i in os.listdir(folder):
    tree = ElementTree.parse(os.path.join(folder,i))
    root = tree.getroot()
    objects = root.findall('object')
    for o in objects:
        name = o.find('name').text
        if name=='person':
            flag = 1
            root.remove(o)
    if flag == 1:
        flag = 0
        tree.write(os.path.join(folder,i))

if not os.path.exists(output_path):
    os.makedirs(output_path)

# YES, I COULD'VE IMPLEMENTED THE ABOVE AND THE FOLLOWIING TOGETHER, 
# BUT I CHOSE NOT TO, *FOR THE SIMPLICITY OF THE READER* 
for i in os.listdir(folder):
    tree = ElementTree.parse(os.path.join(folder,i))
    root = tree.getroot()

    objects = root.findall('object')
    shape = root.find('size')

    imgWidth = int(shape.find('width').text)
    imgHeight = int(shape.find('height').text)

    for j,o in enumerate(objects):
        name = o.find('name').text

        bndbox = o.find('bndbox')

        xmin = float(bndbox.find('xmin').text)
        ymin = float(bndbox.find('ymin').text)
        xmax = float(bndbox.find('xmax').text)
        ymax = float(bndbox.find('ymax').text)

        dw = 1./(imgWidth)
        dh = 1./(imgHeight)
        x = (xmin + xmax)/2.0 - 1
        y = (ymin + ymax)/2.0 - 1
        w = xmax - xmin
        h = ymax - ymin
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh

        cls_id = classes.index(name)
        if j==0:
            out_file = open(output_path + i[:-3] + 'txt', 'w')
        else:
            out_file = open(output_path + i[:-3] + 'txt', 'a')

        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in [x,y,w,h]]) + '\n')
    
    out_file.close()
        # if name=='person':
        #     print('ERROR JHAALA! NEE-NUU-NEE-NUU')