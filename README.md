# FDDB

This repository contains scripts automating conversion of the FDDB dataset to a format required by the Darknet framework.

## Usage

1. Clone and navigate to the repository
2. Use the following links in order to download a complete FDDB dataset.

        wget http://vis-www.cs.umass.edu/fddb/FDDB-folds.tgz
        wget http://vis-www.cs.umass.edu/fddb/README.txt
        wget http://tamaraberg.com/faceDataset/originalPics.tar.gz

3. Create a new folder and call it *images*. Unpack the supplied images inside of it. 

        tar -xzvf FDDB-folds.tgz
        mdkir images && tar -xzvf originalPics.tar.gz -C images

4. Prepare data.

        find FDDB-folds -type f -regex ".*[0-9]-.*txt" -exec cat {} >> FDDB-folds/FDDB-annotations.txt \;
        find FDDB-folds -type f -regex ".*[0-9]+.txt" -exec cat {} >> FDDB-folds/FDDB-paths.txt \;

5. Install the required Python libraries. 

        pip install Pillow

6. Generate all the files required by the Darknet.

        python ./scripts/cs_fddb_convert_to_darknet.py

## License

This is free and unencumbered software released into the public domain. For more information, please refer to the [LICENSE](./LICENSE) file.
