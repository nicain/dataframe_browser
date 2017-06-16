from dataframe_browser.core.utilities import in_ipynb

def test_in_ipynb():

    assert in_ipynb() == False




if __name__ == '__main__':  # pragma: no cover
    test_in_ipynb()  # pragma: no cover