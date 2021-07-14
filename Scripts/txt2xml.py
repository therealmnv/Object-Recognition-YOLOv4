import os

out='toXML'
folder='testOutputs'
classes = ['head','helmet']
flag = 0

for i in os.listdir(folder):
    path = os.path.join(folder,i)
    print(path)
    outPath = os.path.join(out,i)

    fname = str(outPath)[:-3]+'xml'
    file = open(fname,'w')

    file.write('<annotation>\n')
    
    file.write('\t<folder>toXML</folder>\n')
    file.write(f'\t<filename>{str(i)}</filename>\n')
    
    file.write('\t<size>\n')
    file.write('\t\t<width>416</width>\n')
    file.write('\t\t<height>416</height>\n')
    file.write('\t\t<depth>3</depth>\n')
    file.write('\t</size>\n')

    file.write('\t<segmented>0</segmented>\n')

    f = open(path,'r')
    Lines = f.readlines()
    
    if len(Lines)!=0:  
        for line in Lines:
            content = line.split()

            label = str(classes[int(content[0])])
            x = int(content[1])
            y = int(content[2])
            w = int(content[3])
            h = int(content[4])

            xmin = x    #int((x*416+1-(w*416)/2)/416)
            xmax = x+w  #int((x*416+1+(w*416)/2)/416)
            ymin = y    #int((y*416+1-(h*416)/2)/416)
            ymax = y+h  #int((y*416+1+(h*416)/2)/416)

            file.write('\t<object>\n')
            file.write(f'\t\t<name>{label}</name>\n')

            file.write('\t\t<pose>Unspecified</pose>\n')
            file.write('\t\t<truncated>0</truncated>\n')
            file.write('\t\t<occluded>0</occluded>\n')
            file.write('\t\t<difficult>0</difficult>\n')

            file.write('\t\t<bndbox>\n')
            file.write(f'\t\t\t<xmin>{xmin}</xmin>\n')
            file.write(f'\t\t\t<ymin>{ymin}</ymin>\n')
            file.write(f'\t\t\t<xmax>{xmax}</xmax>\n')
            file.write(f'\t\t\t<ymax>{ymax}</ymax>\n')
            file.write('\t\t</bndbox>\n')

            file.write('\t</object>\n')

    file.write('</annotation>')






