PACKAGE_NAME=`python setup.py --name`
CONDA_ENV_NAME=test_$PACKAGE_NAME

# Stash changes to ensure code outside of commit is not tested
git stash -q --keep-index

source activate $CONDA_ENV_NAME
RESULT=$?
[ $RESULT -ne 0 ] && conda create -n $CONDA_ENV_NAME --file requirements.txt
[ $RESULT -ne 0 ] && source activate $CONDA_ENV_NAME
[ $RESULT -ne 1 ] && conda install -n $CONDA_ENV_NAME --file requirements.txt

py.test
RESULT=$?

# Unstash
git stash pop -q
[ $RESULT -ne 0 ] && echo "Testing failed, aborting commit."
[ $RESULT -ne 0 ] && exit 1
exit 0

