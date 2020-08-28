#!python
# -*- coding: utf-8 -*-

"""
Refine image center for diffraction images in CXI file by fit of sphere form factor.
Author: Sergey Bobkov
"""

import os
import sys
import shutil
import subprocess
import argparse
import numpy as np
from tqdm import tqdm

from spi_processing import center, cxidata, sphere


def main():
    parser = argparse.ArgumentParser(description="Refine image center for diffraction images by fit of sphere form factor")
    parser.add_argument('files', metavar='FILE', nargs='+', help='Input files')
    parser.add_argument('-o', '--out', dest='output_dir', help="Output directory")
    parser.add_argument('-s', '--same', action='store_true',
                        help="Consider all input files to have the same center position")
    parser.add_argument('-r', '--report', default="estimate_center_report.pdf",
                        help="Report file")
    parser.add_argument('--max-shift', type=int, default=5,
                        help="Maximum allowed shift in pixels")
    parser.add_argument('-R', '--radius', type=int, default=128, help="Maximum radius in pixels")
    parser.add_argument('-w', '--wavelength', type=float, required=True,
                        help="Radiation wavelength (Angstrom)")
    parser.add_argument('-d', '--distance', type=float, required=True,
                        help="Detector distance (meters)")
    parser.add_argument('--pix', dest='pixel', type=float, required=True,
                        help="Pixel size (meters)")
    parser_args = parser.parse_args()

    input_files = parser_args.files
    output_dir = parser_args.output_dir
    same_pos = parser_args.same
    report_path = parser_args.report
    max_shift = parser_args.max_shift
    radius = parser_args.radius
    wavelength = parser_args.wavelength
    distance = parser_args.distance
    pixel_size = parser_args.pixel

    for fname in input_files:
        if not os.path.isfile(fname):
            parser.error("File {} doesn't exist".format(fname))

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        sys.stderr.write("Copying to output\n")
        os.makedirs(output_dir, exist_ok=True)
        new_input_files = []
        for fname in tqdm(input_files):
            new_fname = os.path.join(output_dir, os.path.basename(fname))
            shutil.copy(fname, new_fname)
            subprocess.call(["/bin/chmod", "u+w", new_fname])
            new_input_files.append(new_fname)
        input_files = new_input_files

    if same_pos:
        sum_data_stack = []
        mask_stack = []
        sys.stderr.write("Reading files\n")
        for fname in tqdm(input_files):
            sum_data_stack.append(center.compute_sum_image(fname))
            mask_stack.append(center.compute_common_mask(fname))

        sum_data = np.stack(sum_data_stack).sum(axis=0)

        # Get pixels that are good for all datasets
        mask = np.abs(np.stack(mask_stack)).min(axis=0)

        image_id = cxidata.get_image_groups(input_files[0])[0]
        start_center = cxidata.read_dataset(input_files[0], image_id, "image_center")
        if "psd/size" in cxidata.get_names(input_files[0], image_id):
            start_size = cxidata.read_dataset(input_files[0], image_id, "psd/size").mean()
        else:
            start_size = sphere.compute_size(sum_data[1]/10, pixel_size/(wavelength*distance))

        sys.stderr.write("Refining center\n")
        image_center = center.refine_center_by_sphere_pattern(sum_data, mask, wavelength, distance,
                                                              pixel_size, start_center, start_size,
                                                              max_shift, radius)

        sys.stderr.write("Saving result\n")
        for fname in tqdm(input_files):
            center.save(fname, image_center)

        sys.stderr.write("Creating report\n")
        center.generate_report(["Summary image"], [sum_data], [image_center], report_path)
    else:
        sum_data_stack = []
        center_values = []
        sys.stderr.write("Processing files\n")
        for fname in tqdm(input_files):
            sum_data = center.compute_sum_image(fname)
            mask = center.compute_common_mask(fname)

            image_id = cxidata.get_image_groups(fname)[0]
            start_center = cxidata.read_dataset(fname, image_id, "image_center")

            if "psd/size" in cxidata.get_names(fname, image_id):
                start_size = cxidata.read_dataset(fname, image_id, "psd/size").mean()
            else:
                start_size = sphere.compute_size(sum_data[1]/10, pixel_size/(wavelength*distance))

            image_center = center.refine_center_by_sphere_pattern(
                sum_data, mask, wavelength, distance, pixel_size,
                start_center, start_size, max_shift, radius)

            center.save(fname, image_center)
            sum_data_stack.append(sum_data)
            center_values.append(image_center)

        sys.stderr.write("Creating report\n")
        center.generate_report(input_files, sum_data_stack, center_values, report_path)


if __name__ == '__main__':
    main()
