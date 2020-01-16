import os
import errno
import math
from PIL import Image

topdir = os.path.abspath(__file__+"/../../")

# in
fddb_annotations = topdir+'/FDDB-folds/FDDB-annotations.txt'
fddb_paths = topdir+'/FDDB-folds/FDDB-paths.txt'

# out
fddb_absolute_paths = topdir+'/fddb.paths'
fddb_classes_file = topdir+'/fddb.names'
fddb_config_file = topdir+'/fddb.data'

# with open(fddb_paths, 'r') as paths:
#     for line in paths:
#         newline = line.rsplit('/')
#         print '/'.join(newline[0:len(newline)-1])


###############################
# individual annotation files #
###############################

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    finally:
        return path
        
with open(fddb_annotations, 'r') as annotations:
    for filepath in annotations:
        # make labels/<year>/<month>/<day>/big directory tree
        filepath_split = filepath.rsplit('/')
        filepath_dir = make_sure_path_exists(topdir + '/labels/' + '/'.join(filepath_split[0:len(filepath_split)-1]))
        # image annotation filepath
        filepath_clean = topdir+'/labels/'+filepath.rstrip('\n')
        # make annotation
        with open(filepath_clean + '.txt', 'w+') as annotation:
            # for each ellipse in image file
            for bbox in range(int(next(annotations))):
                # supplied values
                current_line = next(annotations)
                current_line_split = current_line.split()
                major_axis_radius = float(current_line_split[0])
                minor_axis_radius = float(current_line_split[1])
                angle = float(current_line_split[2])
                center_x = float(current_line_split[3])
                center_y = float(current_line_split[4])
                # find image dimensions
                img_width = 0
                img_height = 0
                with Image.open(filepath_clean.replace('labels','images') + '.jpg') as img:
                    img_width, img_height = img.size
                # calculate bounding box of rotated ellipse
                calc_x = math.sqrt(major_axis_radius**2 * math.cos(angle)**2 \
                                   + minor_axis_radius**2 * math.sin(angle)**2)
                calc_y = math.sqrt(major_axis_radius**2 * math.sin(angle)**2 \
                                   + minor_axis_radius**2 * math.cos(angle)**2)
                # 1 class
                label = 1
                # bounding box
                bbox_x = center_x / img_width
                bbox_y = center_y / img_height
                bbox_w = (2 * calc_x) / img_width
                bbox_h = (2 * calc_y) / img_height
                annotation.write('{} {} {} {} {}\n'.format(label, \
                                                         bbox_x, \
                                                         bbox_y, \
                                                         bbox_w, \
                                                         bbox_h))
################################################
# file containing absolute paths to image data #
################################################

with open(fddb_paths, 'r') as paths:
    with open(fddb_absolute_paths, 'w') as absolute_paths:
        for filepath in paths:
            absolute_paths.write(topdir+'/images/'+filepath.rstrip('\n')+'.jpg\n')

################
# classes file #
################

with open(fddb_classes_file, 'w') as classes:
    classes.write('0\n1')
    
######################
# configuration file #
######################

with open(fddb_config_file, 'wb') as cfg_file:
    # use binary classification
    cfg_file.write("{} = {}\n".format("classess", 2))
    cfg_file.write("{} = {}\n".format("train", fddb_absolute_paths))
    cfg_file.write("{} = {}\n".format("valid", fddb_absolute_paths))
    cfg_file.write("{} = {}\n".format("names", fddb_classes_file))
    cfg_file.write("{} = {}\n".format("backup","backup"))
