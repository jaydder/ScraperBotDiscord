class HelpService:
    def __init__(self, embed_builder):
        self.embed_builder = embed_builder

    def get_help_embed(self):
        return self.embed_builder.build()
