from app.rag_pipeline import build_prompt

def test_build_prompt_hides_metadata():
    contexts = [{"chunk":"Hello world from services.","doc_path":"docs/x.docx","chunk_id":"abc123"}]
    p = build_prompt("What do you do?", contexts)
    assert "Hello world" in p
    assert "docs/x.docx" not in p and "abc123" not in p
    assert "DO NOT show citations" in p
