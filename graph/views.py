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

def detail(request, face):
    EMOTIONS = ['angry', 'disgusted', 'fearful',
                'happy', 'sad', 'surprised', 'neutral']
    person = get_object_or_404(TestPerson, face=face)
    print(person.face)
    # load face image by convert array to image
    image = person.face_image
    image = np.asarray(image, dtype=np.float32)
    img = Image.fromarray(image)
    img = img.convert('RGB')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    person.emotion_detail = [json.loads(x) for x in person.emotion_detail]

    times = []
    angry = []
    disgusted = []
    fearful = []
    happy = []
    sad = []
    surprised = []
    neutral = []

    for i in person.emotion_detail:
        times.append(i['timestamp'])
        angry.append(i['emotion'][0])
        disgusted.append(i['emotion'][1])
        fearful.append(i['emotion'][2])
        happy.append(i['emotion'][3])
        sad.append(i['emotion'][4])
        surprised.append(i['emotion'][5])
        neutral.append(i['emotion'][6])
    plt.plot(times, angry)
    plt.plot(times, disgusted)
    plt.plot(times, fearful)
    plt.plot(times, happy)
    plt.plot(times, sad)
    plt.plot(times, surprised)
    plt.plot(times, neutral)
    plt.xticks(rotation='vertical', fontsize=7)
    plt.legend(EMOTIONS)
    plt.tight_layout()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figdata_png = base64.b64encode(figfile.getvalue()).decode()
    plt.clf()

    return render(request, 'graph/detail.html', {'person': person, 'img_str': img_str, 'graph': figdata_png})
