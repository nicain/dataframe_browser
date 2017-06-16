from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.layouts import column
import pandas as pd
from dataframe_browser.core.utilities import launch

def get_layout():
    data_df = pd.DataFrame(dict(A=[0, 1, .2], B=[0, .5, .9]))
    source = ColumnDataSource(data=data_df)
    data_table = DataTable(source=source, width=600, height=600)
    data_table.columns = [TableColumn(field='A', title='A'),
                          TableColumn(field='B', title='B')]

    layout = column([data_table])

    return layout

launch(get_layout)
