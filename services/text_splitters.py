from langchain_text_splitters import RecursiveCharacterTextSplitter

class MyCharacterTextSplitter(RecursiveCharacterTextSplitter):

    def __init__(self, chunk_size=1000, chunk_overlap=200, add_start_index=True):
        super().__init__(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=add_start_index
        )