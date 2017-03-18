mkdir FDDB-folds/annotations
mkdir FDDB-folds/paths

mv FDDB-folds/FDDB-fold-*-ellipseList.txt FDDB-folds/annotations
mv FDDB-folds/FDDB-fold-*.txt FDDB-folds/paths

cat FDDB-folds/annotations/FDDB-fold-*-ellipseList.txt >> FDDB-folds/FDDB-annotations.txt
cat FDDB-folds/paths/FDDB-fold-*.txt >> FDDB-folds/FDDB-paths.txt
