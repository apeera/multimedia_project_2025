import time
from main import segment_audio, compute_features

def benchmark_different_lengths():
    print("="*60)
    print("DIFFERNT AUDIO LENGTHS BENCHMARK")
    print("="*60)
    
    test_cases = [
        ("Short (30s)", 3),   #30 sec
        ("Medium (60s)", 6),   # 60 sec
        ("Long (120s)", 12),  #2 mins
        ("Very Long (300s)", 30),  #5 mins
    ]
    results = []
    
    for label, num_segments in test_cases:
        segments = [{"id": i} for i in range(num_segments)]
        start = time.time()
        features = compute_features(segments)
        end = time.time()
    
        elapsed = end - start
        results.append({
            "label": label,
            "segments": num_segments,
            "time": elapsed
        })
        print(f"{label:20} | {num_segments:3} segments | {elapsed:.4f}s")
    print("="*60)
    print(f"\nAvg time per segment: {sum(r['time'] for r in results) / sum(r['segments'] for r in results):.6f}s")
    return results

if __name__ == "__main__":
    benchmark_different_lengths()