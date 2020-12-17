import featuremap as fm
import os

input_img_size = (28, 28)
#create dir
def saveSlicedImage(created_dir="slicedImDir", srcpathdir="./dataset"):
    if os.path.exists(created_dir):
        os.remove(created_dir)
    os.mkdir(created_dir)
    openFiles(created_dir, srcpathdir)

def openFiles(created_dir, pathdir):
    for filename in os.listdir(pathdir):
        # if os.path.isdir(filename) is False:
        if not os.path.isdir(os.path.join(pathdir, filename)):
            iL = fm.ImageLoader((5, 5), 1, input_img_size)
            print(pathdir + "/" + filename)
            print(os.path.isdir(filename))
            slicedIm = iL.getOutput(pathdir + "/" + filename)
            fm.TensorFileManager().save(created_dir + "/" + filename + ".tensorfile", slicedIm)
        else:
            print(filename)
            openFiles(created_dir, pathdir + "/" + filename)

    # input_img_size = (244, 244)
    # for path in pathlib.Path(pathdir).iterdir():
    #     if path.is_file():
    #         iL = featuremap.ImageLoader((5, 5), 1, input_img_size)
    #         slicedIm = iL.getOutput(rp_dataset + pathdir + path)

    #         # current_file = open(path, "r")
    #         # print(current_file.read())
    #         # current_file.close()
    #     else
    #         openFiles(pathdir + path)


