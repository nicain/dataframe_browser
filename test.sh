PACKAGE_NAME=`python setup.py --name`
CONDA_ENV_NAME=test_$PACKAGE_NAME

source activate $CONDA_ENV_NAME
RESULT=$?
[ $RESULT -ne 0 ] && conda create -n $CONDA_ENV_NAME --file requirements.txt
[ $RESULT -ne 0 ] && source activate $CONDA_ENV_NAME
[ $RESULT -ne 1 ] && conda install -n $CONDA_ENV_NAME --file requirements.txt

py.test