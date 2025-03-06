from astropy.io import fits
from astropy.wcs import WCS
from reproject import reproject_interp
import glob
import os

os.chdir("/home/maverick/Pictures/SirilPWD/")

reference_file = "jw02739-o001_t001_nircam_clear-f200w_i2d.fits"
fits_files = glob.glob("jw02739-o001_t001_*.fits")

# Open the reference FITS to get its WCS and shape
with fits.open(reference_file) as ref_hdul:
    ref_wcs = WCS(ref_hdul[1].header)
    ref_shape = ref_hdul[1].data.shape

for file in fits_files:
    with fits.open(file) as hdul:
        target_wcs = WCS(hdul[1].header)
        target_data = hdul[1].data

        # Reproject (align & scale) using WCS
        reprojected_data, _ = reproject_interp((target_data, target_wcs), ref_wcs, shape_out=ref_shape)

        new_filename = f"reprojected_{file}"
        fits.writeto(new_filename, reprojected_data, ref_hdul[1].header, overwrite=True)
        print(f"Saved: {new_filename}")

print("\n✅ All FITS images have been rescaled and WCS is preserved!")
