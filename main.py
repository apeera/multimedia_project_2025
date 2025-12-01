import argparse
import json
import os
from pathlib import Path

def extract_audio(video_path):
    """
    Extracts audio from a video file and returns path to .wav file.
    """
    wav_path = Path(video_path).with_suffix(".wav")

    return str(wav_path)


def segment_audio(audio_path):
    """
    Splits audio into 10-second segments.
    Returns list of dicts: [{"id":0,"start":0,"end":10,"path":"chunk_000.wav"}, ...]
    """
    segments = []
    for i in range(5):  
        segments.append({
            "id": i,
            "start": i * 10,
            "end": (i + 1) * 10,
            "path": f"chunk_{i:03d}.wav"
        })
    return segments


def compute_features(segments):
    """
    Computes RMS or other metrics.
    Returns {segment_id: {"rms": value, ...}}
    """
    features = {}
    for s in segments:
        features[s["id"]] = {"rms": 0.1, "peak": 0.2} 
    return features


def get_transcript_excerpts(transcript_path, segments):
    """
    Matches transcript text roughly to segments.
    """
    with open(transcript_path, "r") as f:
        text = f.read()

    words = text.split()
    chunk_size = max(len(words) // len(segments), 1)

    mapping = {}
    for s in segments:
        start = s["id"] * chunk_size
        end = (s["id"] + 1) * chunk_size
        mapping[s["id"]] = " ".join(words[start:end])

    return mapping


def apply_remediation(segments, rule_outputs):
    """
    Applies audio fixes (placeholder).
    Returns updated segment paths.
    """
    updated = {}
    for s in segments:
        updated[s["id"]] = s["path"]  
    return updated


def export_results(segments, rule_outputs, out_dir):
    """
    Writes a final JSON file with:
    - segments
    - features
    - transcript excerpts
    - rule outputs
    """
    os.makedirs(out_dir, exist_ok=True)
    
    out = {
        "segments": segments,
        "rules": rule_outputs
    }

    json_path = os.path.join(out_dir, "results.json")
    with open(json_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Results exported to {json_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--out", default="output")
    args = parser.parse_args()

    # Pipeline
    audio_path = extract_audio(args.video)
    segments = segment_audio(audio_path)
    features = compute_features(segments)
    excerpts = get_transcript_excerpts(args.transcript, segments)

    #simple rule output 
    rule_outputs = {
        seg["id"]: {
            "too_quiet": features[seg["id"]]["rms"] < 0.2,
            "excerpt": excerpts[seg["id"]],
            "audio_path": seg["path"]
        }
        for seg in segments
    }

    export_results(segments, rule_outputs, args.out)


if __name__ == "__main__":
    main()
