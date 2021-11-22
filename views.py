from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser

import numpy as np
from scipy.io import wavfile
from scipy import signal

# Create your views here.

def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
@parser_classes([FileUploadParser])
def process_spectogram(request):
    """
    headers: {
        Content-Disposition: attachment: filename="file.wav",
        Content-Type: audio/wav
    }
    """
    data = request.FILES
    response = {}
    if not data:
        response['message'] = f"File not provided."
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    try:
        file = data['file']
        fs, Audiodata = wavfile.read(file, mmap=True)
        if len(Audiodata.shape) > 1:
            Audiodata = Audiodata[:, 0]
        Audiodata = Audiodata / (2.0 ** 15)  # Normalized between [-1,1]
        # Spectrogram
        N = 512  # Number of points in the fft
        w = signal.windows.blackman(N)
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
        freqs, time_segment, spectogram_of_x = signal.spectrogram(Audiodata, fs, window=w, nfft=N)
        spectogram_of_x = 10 * np.log10(spectogram_of_x)
        response['data'] = {"time": time_segment.tolist(), "frequency": freqs.tolist(), "spectogram": spectogram_of_x.tolist()}
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        response['error'] = { f"{e.__class__.__name__}": f"{e}" }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)