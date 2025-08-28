from app.deps.chunking import chunk_text

def test_chunk_windowing():
    text = " ".join([f"w{i}" for i in range(300)])
    chunks = list(chunk_text(text, chunk_size=100, overlap=20))
    # Expect sliding windows with overlap
    assert len(chunks) >= 3
    assert chunks[0].split()[:5] == ["w0","w1","w2","w3","w4"]
    # Overlap check: last 20 of chunk0 == first 20 of chunk1
    assert chunks[0].split()[-20:] == chunks[1].split()[:20]
