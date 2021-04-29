import os
import cv2
from django.http import StreamingHttpResponse
from django.http import JsonResponse, HttpResponse

from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode
from detectron2.engine.defaults import DefaultPredictor
from detectron2.data.catalog import MetadataCatalog, DatasetCatalog
from detectron2.data.datasets import register_coco_instances
from detectron2.config import get_cfg

BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + '\\..\\'

register_coco_instances("youtube-od", {}, "D:/OD_Project_Data/youtube-od/annotations/instances_train2021.json",
                        "D:/OD_Project_Data/youtube-od/train2021")
dataset_dicts = DatasetCatalog.get("youtube-od")
ship_metadata = MetadataCatalog.get("youtube-od")

cfg = get_cfg()
cfg.merge_from_file("D:/Git_workspace/detectron2/configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4
cfg.MODEL.WEIGHTS = "D:/OD_Project_Data/myoutput/model_final_0419.pth"
print('loading from: {}'.format(cfg.MODEL.WEIGHTS))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.25  # set a custom testing threshold
predictor = DefaultPredictor(cfg)

videoname = ""
iteration = 0
raw = False

class VideoCamera(object):
    def __init__(self, videoname):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        if raw:
            self.video = cv2.VideoCapture(os.path.join(BASE_DIR, 'static/Upload_File/' + videoname))
        else :
            self.video = cv2.VideoCapture(os.path.join(BASE_DIR, 'static/Processed_File/' + videoname))

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global iteration
        iteration += 1
        success, im = self.video.read()
        if raw and iteration % 2 == 0:
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
            outputs = predictor(im)
            v = Visualizer(im[:, :, ::-1],
                           metadata=ship_metadata,
                           scale=0.5,
                           instance_mode=ColorMode.IMAGE_BW
                           # remove the colors of unsegmented pixels. This option is only available for segmentation models
                           )
            out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            ####
            ret, jpeg = cv2.imencode('.jpg', out.get_image()[:, :, ::-1])
        else:
            ret, jpeg = cv2.imencode('.jpg', im)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def streamhr(request):
    return StreamingHttpResponse(gen(VideoCamera(videoname)), content_type='multipart/x-mixed-replace; boundary=frame')


def tellName(request):
    global videoname
    global raw
    videoname = request.POST.get("videoname")
    if request.POST.get("type") == "processed":
        raw = False
    if request.POST.get("type") == "raw":
        raw = True
    return HttpResponse(videoname)

def savingpic(request):
    picname = request.POST.get("picname")
    im = cv2.imread(BASE_DIR + '/static/Upload_File/' + picname)
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1],
                   metadata=ship_metadata,
                   scale=0.5,
                   instance_mode=ColorMode.IMAGE_BW
                   # remove the colors of unsegmented pixels. This option is only available for segmentation models
                   )
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2.imwrite(BASE_DIR + '/static/Processed_File/' + picname, out.get_image()[:, :, ::-1])

    return HttpResponse('Saved')
