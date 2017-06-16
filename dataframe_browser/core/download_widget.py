from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Button

class DownloadWidget(object):

    def __init__(self, get_source_df_callback, to_csv=lambda x:x.to_csv()):

        self.get_source_df_callback = get_source_df_callback
        self._button = None
        self.to_csv = to_csv
        self.dowload_source = ColumnDataSource(data=dict())
        self.jscb = CustomJS(args=dict(source=self.dowload_source), code='''
        var txt = source.data['data'][0];
        if ((txt != "_begin") && (txt != "_end")) {
                var filename = 'data.csv';
                var blob = new Blob([txt], { type: 'text/csv;charset=utf-8;' });

                //addresses IE
                if (navigator.msSaveBlob) {
                    navigator.msSaveBlob(blob, filename);
                }

                else {
                    var link = document.createElement("a");
                    link = document.createElement('a')
                    link.href = URL.createObjectURL(blob);
                    link.download = filename
                    link.target = "_blank";
                    link.style.visibility = 'hidden';
                    link.dispatchEvent(new MouseEvent('click'))
                }
        }
        ''')

        self.dowload_source.js_on_change('data', self.jscb)

    def initialize(self):
        '''
        Include any initialization that references objects outside of this object
        :return:
        '''
        pass

    @property
    def df(self):
        return self.get_source_df_callback()

    def send_data_callback(self):
        self.dowload_source.data = {'data': ['_begin']}
        self.dowload_source.data = {'data': [self.to_csv(self.df)]}
        self.dowload_source.data = {'data': ['_end']}

    def get_button(self, label='Download data'):

        self._button = Button(label=label)
        self.button.on_click(self.send_data_callback)

        return self.button

    @property
    def button(self):
        return self._button