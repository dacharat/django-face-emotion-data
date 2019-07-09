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

    # load face image by convert array to image
    image = person.face_image
    image = np.asarray(image, dtype=np.float32)
    img = Image.fromarray(image)
    img = img.convert('RGB')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    person.emotion_detail = [json.loads(x) for x in person.emotion_detail]

    # improve more performance
    for idx, i in enumerate(person.emotion_detail):
        y_pos = np.arange(len(EMOTIONS))
        level = i['emotion'][0]
        plt.rcdefaults()
        plt.barh(y_pos, level, align='center', alpha=0.5)
        plt.yticks(y_pos, EMOTIONS)
        plt.xlabel('Level')
        axes = plt.gca()
        axes.set_xlim([0, 1])

        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figdata_png = base64.b64encode(figfile.getvalue()).decode()
        person.emotion_detail[idx]['emotion'] = figdata_png
        plt.clf()

    return render(request, 'graph/detail.html', {'person': person, 'img_str': img_str})
