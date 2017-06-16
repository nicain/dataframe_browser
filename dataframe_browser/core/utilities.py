from bokeh.io import show, curdoc, output_notebook
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application

def in_ipynb():

    try:
        from ipykernel.zmqshell import ZMQInteractiveShell
        return isinstance(get_ipython(), ZMQInteractiveShell)
    except NameError:
        return False

def launch(get_layout, title='Default', notebook_url="localhost:8888"):
    def modify_doc(doc):
        layout = get_layout()
        doc.add_root(layout)
        doc.title = title

    if in_ipynb():

        output_notebook()
        handler = FunctionHandler(modify_doc)
        app = Application(handler)
        doc = app.create_document()
        show(app, notebook_url=notebook_url)

        return doc

    else:
        modify_doc(curdoc())
        return curdoc()