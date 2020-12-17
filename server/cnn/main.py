
import featuremap as fm

rp_dataset = "./dataset/"

input_img_size = (244, 244)
# input_img_size = (28, 28)
iL = fm.sImageLoader((5, 5), 1, input_img_size)
iL.getOutput(rp_dataset + "daisy/" + "5547758_eea9edfd54_n.jpg")