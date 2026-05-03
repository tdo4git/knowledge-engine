class QueryEmbedder:

    def __init__(self, embedding_model):
        self.model = embedding_model

    def embed(self, query: str):

        vector = self.model.encode([query])

        return vector