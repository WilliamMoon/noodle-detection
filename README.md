# noodle-detection

There are some data about the objective detection programming assignment of HW2 in Machine Learning class.

The whole project is based on [AlexeyAB/darknet](https://github.com/AlexeyAB/darknet.git).

## 1 Clone and make darknet

`git clone https://github.com/AlexeyAB/darknet.git`

edit `Makefile`: gpu cudnn opencv = 0

`make`

## 2 Set training params

### 2.1 CFG

`cp cfg/yolov4-tiny-custom.cfg yolov4-tiny-custom.cfg` and edit

> subdivisions=16
>
> max_batches=6000
>
> steps=4800,5400
>
> classes=3 in each [yolo]
>
> filters=24 in [cov...] before each [yolo]

Due to time-limit, I changed `max_batches=100`.

### 2.2 .name & .data

Create `data/obj.names`: save class name line by line

Create `data/obj.data`:

> classes = 3
>
> train = data/train.txt
>
> valid = data/test.txt
>
> names = data/obj.names
>
> backup = backup/

## 3 Prepare data

Use [tzutalin/labelImg](https://github.com/tzutalin/labelImg) to label training images with YOLO format. Put the images and label files into `data/obj/`.

Create `data/train.txt`: relative path to `darknet` of every train image line by line

> data/obj/train-0151.jpeg
> data/obj/train-0701.jpeg
> data/obj/train-0776.jpeg
> data/obj/train-0301.jpeg
>
> ...

## 4 Train

Download pre-trained weights [yolov4-tiny.conv.29](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29).

Start train: `./darknet detector train data/obj.data yolov4-tiny-custom.cfg yolov4.conv.29`.

## 5 Test

Since I do not make `darknet` with GPU and opencv, the video test function darknet provide is not available. So I used `ffmpeg` to convert test video to images, and take them as validation set to test.

`ffmpeg -i /Users/will/YOLOX/assets/test\ video.mp4 -r 30 -f image2 test-%04d.jpeg`

Create `data/test.txt`: relative path to `darknet` of every test image line by line

Test: `./darknet detector valid data/obj.data yolov4-tiny-custom.cfg backup/yolov4-tiny-custom_final.weights `

The predictions are saved in `results/` with content of filename, confidence, x, y, w, h.

I used OpenCV python to draw rectangles and labels in images. The script is in `label.py`. I do see the `batch_detection()` in`darknet_images.py` which detect and save images, but there comes some error.

Finally, use `ffmpeg` to convert labeled images to video. `ffmpeg -f image2 -i results/image/test-%04d.jpeg -vcodec libx264 -r 30 -b 1000k results/test.mp4`


-----
For a detailed guide, see [Readme](https://github.com/AlexeyAB/darknet) by AlexeyAB.
