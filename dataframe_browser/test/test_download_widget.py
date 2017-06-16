from dataframe_browser.core.download_widget import DownloadWidget
import pandas as pd

def test_callback():


    df = pd.DataFrame(dict(A=[1,2], B=[3,4]))
    dw = DownloadWidget(lambda :df)
    dw.get_button()
    dw.send_data_callback()

if __name__ == '__main__':                                    # pragma: no cover
    test_callback()                                              # pragma: no cover