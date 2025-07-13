import tiktoken

def chunk_text(text, model="gpt-4.1", max_tokens=400):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    words = text.split()
    
    chunks = []
    current_chunk = []
    current_len = 0

    for word in words:
        word_tokens = len(encoding.encode(word))
        if current_len + word_tokens > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_len = 0
        current_chunk.append(word)
        current_len += word_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
