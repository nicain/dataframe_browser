PACKAGE_NAME=template_package
CONDA_ENV_NAME=test_$PACKAGE_NAME

# Stash changes to ensure code outside of commit is not tested
git stash -q --keep-index

source activate $CONDA_ENV_NAME
RESULT=$?
[ $RESULT -ne 0 ] && conda create -n $CONDA_ENV_NAME --file requirements.txt
[ $RESULT -ne 0 ] && source activate $CONDA_ENV_NAME



conda install -n $CONDA_ENV_NAME --file requirements.txt

conda env export -n $CONDA_ENV_NAME

py.test
RESULT=$?

# Unstash
git stash pop -q
[ $RESULT -ne 0 ] && echo "Testing failed, aborting commit."
[ $RESULT -ne 0 ] && exit 1
exit 0

