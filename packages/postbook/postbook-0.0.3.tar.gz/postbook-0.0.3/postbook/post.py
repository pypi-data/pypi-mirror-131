class HtmlPost:
    def __init__(self, title: str):
        self.title = title
        self.path = self.get_chapter_path()

    def get_chapter_path(self):
        path = "chapters/index_" + self.title.replace(' ','__') + ".html"
        return path

    def __str__(self):
        return self.path