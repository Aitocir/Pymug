
def pack_text(text):
    return bytes(text, encoding='utf-8')

def print_responses(q):
    while True:
        print(str(q.get(), encoding='utf-8'))