from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

import json
import numpy as np
from PIL import Image
import base64
from io import StringIO, BytesIO
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt

from .models import Person, TestPerson
# from graph.ml2_face_emoji_swap.database import Database

# Create your views here.
def index(request):
    latest_person_list = TestPerson.objects.all()
    context = {
        'latest_person_list': latest_person_list,
    }
    return render(request, 'graph/index.html', context)

def graph_plot(EMOTIONS, times, emotion):
    for e in emotion:
        plt.plot(times, e)
    plt.xticks(rotation='vertical', fontsize=7)
    plt.ylim(0,1)
    plt.legend(EMOTIONS)
    plt.tight_layout()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figdata_png = base64.b64encode(figfile.getvalue()).decode()
    plt.clf()
    return figdata_png


def detail(request, face):
    EMOTIONS = ['angry', 'disgusted', 'fearful',
                'happy', 'sad', 'surprised', 'neutral']
    person = get_object_or_404(TestPerson, face=face)
    # load face image by convert array to image
    image = person.face_image
    image = np.asarray(image, dtype=np.float32)
    img = Image.fromarray(image)
    img = img.convert('RGB')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    person.emotion_detail = [json.loads(x) for x in person.emotion_detail]

    times, angry, disgusted, fearful, happy, sad, surprised, neutral = ([] for i in range(8))

    for i in person.emotion_detail:
        times.append(i['timestamp'])
        angry.append(i['emotion'][0])
        disgusted.append(i['emotion'][1])
        fearful.append(i['emotion'][2])
        happy.append(i['emotion'][3])
        sad.append(i['emotion'][4])
        surprised.append(i['emotion'][5])
        neutral.append(i['emotion'][6])

    summary_graph = graph_plot(EMOTIONS, times, [angry, disgusted, fearful, happy, sad, surprised, neutral])

    return render(request, 'graph/detail.html', {
        'person': person, 
        'img_str': img_str, 
        'graphs': summary_graph, 
        'emotion': ['summary'] + EMOTIONS,
        'path': 'summary'
        })

def detail_emotion(request, face, emotion):
    EMOTIONS = ['angry', 'disgusted', 'fearful',
                'happy', 'sad', 'surprised', 'neutral']
    emotions = enumerate(EMOTIONS)
    person = get_object_or_404(TestPerson, face=face)
    image = person.face_image
    image = np.asarray(image, dtype=np.float32)
    img = Image.fromarray(image)
    img = img.convert('RGB')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    person.emotion_detail = [json.loads(x) for x in person.emotion_detail]

    times, emotion_arr = ([] for i in range(2))
    index = [idx for idx, e in emotions if e == emotion][0]

    for i in person.emotion_detail:
        times.append(i['timestamp'])
        emotion_arr.append(i['emotion'][index])

    emotion_arr_graph = graph_plot([EMOTIONS[index]], times, [emotion_arr])

    return render(request, 'graph/detail.html', {
        'person': person, 
        'img_str': img_str, 
        'graphs': emotion_arr_graph, 
        'emotion': ['summary'] + EMOTIONS,
        'path': emotion
        })
