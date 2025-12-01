import pytest
from main import segment_audio, compute_features, get_transcript_excerpts

def test_segment_audio():
    "tests segmentation of audio"
    segments = segment_audio("dummy.wav")
    assert len(segments) == 5

def test_compute_features():
    "tests feature computation"
    segments = [{"id": 0}, {"id": 1}]
    features = compute_features(segments)
    assert len(features) == 2
    assert "rms" in features[0]

def test_transcript():
    "tests transcript excerpting"
    #create test file
    with open("test.txt", "w") as f: 
        f.write("hello world test")
    
    segments = [{"id": 0}]
    excerpts = get_transcript_excerpts("test.txt", segments)
    assert len(excerpts) == 1
    
    import os
    os.remove("test.txt")