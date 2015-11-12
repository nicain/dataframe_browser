# Stash changes to ensure code outside of commit is not tested
git stash -q --keep-index

py.test .
RESULT=$?

# Unstash
git stash pop -q
[ $RESULT -ne 0 ] && echo "Testing failed, aborting commit."
[ $RESULT -ne 0 ] && exit 1
exit 0

