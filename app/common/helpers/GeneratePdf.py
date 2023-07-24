from reportlab.platypus import Frame, PageTemplate


class GeneratePdf:
    def __init__(self, response, template, pdf_table):
        self.response = response
        self.template = template
        self.pdf_table = pdf_table

    def generate(self):
        self.pdf_table.get_data()

        data_chunks = list(self.pdf_table.chunks(self.pdf_table.data, 40))
        story = [self.pdf_table.create_table(chunk) for chunk in data_chunks]

        frame = Frame(30, 50, 550, 700)
        template = PageTemplate(frames=[frame])
        self.template.addPageTemplates([template])

        self.template.build(story)

        return self.response
