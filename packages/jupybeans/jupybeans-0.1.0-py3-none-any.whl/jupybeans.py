from nbconvert.preprocessors import Preprocessor


class RemoveSkip(Preprocessor):
    def preprocess(self, notebook, resources):
        notebook.cells = [
            cell for cell in notebook.cells
            if not ((md := cell.metadata.get('slideshow')) and (st := md.get('slide_type')) and st == 'skip')
        ]
        return notebook, resources
