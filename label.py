import cv2
import argparse
import matplotlib
import random
import os

'''
show label of image
'''


class Colors:
    # Ultralytics color palette https://ultralytics.com/
    def __init__(self):
        self.palette = [
            self.hex2rgb(c) for c in matplotlib.colors.TABLEAU_COLORS.values()
        ]
        self.n = len(self.palette)

    def __call__(self, i, bgr=False):
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):  # rgb order (PIL)
        return tuple(int(h[1 + i : 1 + i + 2], 16) for i in (0, 2, 4))


colors = Colors()  # create instance for 'from utils.plots import colors'


def plot_one_box(x, im, color=None, label=None, line_thickness=3):
    # Plots one bounding box on image 'im' using OpenCV
    assert (
        im.data.contiguous
    ), "Image not contiguous. Apply np.ascontiguousarray(im) to plot_on_box() input image."
    tl = (
        line_thickness or round(0.002 * (im.shape[0] + im.shape[1]) / 2) + 1
    )  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(im, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(im, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(
            im,
            label,
            (c1[0], c1[1] - 2),
            0,
            tl / 3,
            [225, 255, 255],
            thickness=tf,
            lineType=cv2.LINE_AA,
        )


names = ["person", "bike", "car", "motor", "bus", "truck"]


def index2name(index: int) -> str:
    return names[index]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help="image path", required=True, type=str)
    args = parser.parse_args()
    imagePath = args.image
    labelPath = imagePath.replace(".jpg", ".txt")
    if not os.path.exists(imagePath) or not os.path.exists(labelPath):
        print("图片或者标签不存在")
        exit()
    img = cv2.imread(imagePath)
    w, h = img.shape[1], img.shape[0]
    with open(labelPath) as f:
        for line in f:
            temp = line.split(" ")
            name = temp[0]
            old_label = temp[1:]
            old_label = [float(x) for x in old_label]
            label = {}
            label[0] = (old_label[0] - old_label[2] / 2) * w
            label[2] = (old_label[0] + old_label[2] / 2) * w
            label[1] = (old_label[1] - old_label[3] / 2) * h
            label[3] = (old_label[1] + old_label[3] / 2) * h
            plot_one_box(label, img, color=colors(name), label=index2name(int(name)))

        cv2.imshow(imagePath, img)
        cv2.waitKey(0)

