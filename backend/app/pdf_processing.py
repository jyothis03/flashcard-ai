import fitz

def extract_text_from_pdf(file_bytes: bytes) ->str:
    pdf = fitz.open(stream=file_bytes, filetype="pdf")
    full_text=""

    for page in pdf:
        full_text += page.get_text() + "\n"

    pdf.close()

    return full_text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    words=text.split()
    start=0
    chunks=[]

    while start<len(words):
        end=start+chunk_size
        chunk=" ".join(words[start:end])
        chunks.append(chunk)
        start= end - overlap

    return chunks