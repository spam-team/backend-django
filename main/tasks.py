from collections import defaultdict

import cv2
import numpy as np

from config.celery import app
from utils.face_emotion import FaceEmotionDetect
from utils.emotion_detect import LABELS

face_emotion_detect = FaceEmotionDetect()


@app.task
def set_video_emotions(video_id):
    from main.models import VideoExample

    emotions = list()
    video = VideoExample.objects.get(video_id)
    emotions_stats = defaultdict(int)

    cap = cv2.VideoCapture(video.video.path)
    
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        items = face_emotion_detect.find_all_emotions(frame)
        
        if not items:
            emotions.append([0] * len(LABELS))
        else:
            emotions.append(list(map(lambda x: round(x * 100), items[0][1].detach().numpy())))
            emotions_stats[LABELS[np.argmax(emotions[-1])]] += 1

    overall = []
    sum_count = sum(emotions_stats.values()) + 1

    for label in LABELS:
        overall.append(round(emotions_stats[label] / sum_count * 100))

    video.emotions = {
        "labels": LABELS,
        "emotions": emotions,
        "overall": overall,
    }
    video.save()
