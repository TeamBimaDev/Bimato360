from reportlab.platypus import BaseDocTemplate


class NumberedCanvas(BaseDocTemplate):
    def __init__(self, *args, **kwargs):
        BaseDocTemplate.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def after_flowable(self, flowable):
        if "PageCount" in flowable.__dict__:
            self._saved_page_states.append(dict(self.canv.getPageState()))

    def before_draw_page(self, canvas, doc):
        canvas.saveState()
        self.draw_page_number(canvas)
        canvas.restoreState()

    def draw_page_number(self, canvas):
        pageNumber = canvas.getPageNumber()
        total_pages = len(self._saved_page_states) + 1
        if pageNumber == total_pages:
            self._saved_page_states.append(dict(self.canv.getPageState()))
        canvas.setFont('Helvetica', 10)
        page_num = "%s/%s" % (pageNumber, total_pages)
        canvas.drawString(550, 30, page_num)
