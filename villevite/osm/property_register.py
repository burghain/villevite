class PropertyRegister():

    def __init__(self):
        self.writers = []

    def register_writers(self, writer):
        self.writers += writer

    def process_all_props(self, row):
        for writer in self.writers:
            writer.process_prop(row)

    def write_all_props(self, e):
        for writer in self.writers:
            writer.write_prop(e)

    def get_prop_names(self):
        return [writer.name for writer in self.writers]

    def get_prop_dtypes(self):
        return [writer.dtype for writer in self.writers]

    def get_prop_defaults(self):
        return [writer.default for writer in self.writers]
