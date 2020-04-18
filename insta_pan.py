from PIL import Image
import sys
import os
import getopt
import math


def show_help():
    """
    Shows Help Text
    """
    print("""usage: python insta_pan.py -i source_file [-d | -r | -o]
-d : output destination folder, default is {current working directory}/{image_name}
-r : aspect ratio, default is 1:1
-o : optimize image for uploading to instagram, dafault is False
    """)


def crop(image_path, destination_path, aspect_ratio, optimize):
    """
    Crop panorama image into seperate images
    Parameters
    ----------
    image_path : string
        path to panorama image

    destination_path : string
        destination path for saving cropped images

    aspect_ratio : string
        ratio used to split the image. ex : 1:1 or 3:4

    optimize : bool
        resize cropped images to an optimized size for uploading to instagram
    """
    # parsing the ratio
    width_ratio = int(aspect_ratio[:aspect_ratio.find(":")])
    height_ratio = int(aspect_ratio[aspect_ratio.find(":") + 1:])
    # create the destination folder if not exist
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    with Image.open(image_path) as img:
        width, height = img.size
        ratio = width_ratio / height_ratio
        # maximum box count inside the image size with given ratio
        box_len = math.ceil(width / (height * ratio))
        # calcualte each box's width and height
        box_width = width / box_len
        box_height = box_width / ratio
        # usualy box hieghts are less than actual image height, find out how much offset is needed to put the box in center
        height_offset = (height - box_height) / 2
        extension = os.path.splitext(image_path)[1]
        for box_number in range(box_len):
            width_offset = box_number * box_width
            box = (width_offset, height_offset, width_offset + box_width,
                   height - height_offset)
            crop = img.crop(box)
            if (optimize and width_offset > 1080):
                # calculate optimized width and heights
                optimized_width = 1080
                optimized_height = int(optimized_width * box_height /
                                       box_width)
                # resize the cropped image
                crop = crop.resize((optimized_width, optimized_height))
            # save the image to destination folder
            crop.save(f"{destination_path}/{box_number + 1}{extension}")


def main(argv):
    optlist, _ = getopt.getopt(argv, 'i:d:r:oh')
    image_path = None
    images_destination = None
    ratio = "1:1"
    optimize = False
    for opt, arg in optlist:
        if opt == "-i":
            image_path = arg
        if opt == "-d":
            images_destination = arg
        if opt == "-r":
            ratio = arg
        if opt == "-o":
            optimize = True
        if opt == "-h":
            return show_help()
    if not image_path:
        return show_help()
    if not images_destination:
        images_destination = os.getcwd(
        ) + f"/{os.path.splitext(os.path.basename(image_path))[0]}"
    crop(image_path, images_destination, ratio, optimize)


if __name__ == "__main__":
    main(sys.argv[1:])