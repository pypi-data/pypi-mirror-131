import logging
from typing import Union, List, Optional
import numpy as np
import astropy.units as u

from pyobs.mixins.pipeline import PipelineMixin
from pyobs.object import Object
from pyobs.utils.archive import Archive
from pyobs.utils.enums import ImageType
from pyobs.images import Image, ImageProcessor
from pyobs.utils.time import Time

log = logging.getLogger(__name__)


class Pipeline(Object, PipelineMixin):
    """Pipeline based on the astropy package ccdproc."""

    def __init__(self, steps: List[Union[dict, ImageProcessor]], *args, **kwargs):
        """Pipeline for science images.

        Args:
            steps: List of pipeline steps to perform.
        """
        Object.__init__(self, *args, **kwargs)
        PipelineMixin.__init__(self, steps)

    def _combine_calib_images(self, images: List[Image], bias: Image = None, normalize: bool = False,
                              method: str = 'average'):
        """Combine a list of given images.

        Args:
            images: List of images to combine.
            bias: If given, subtract from images before combining them.
            normalize: If True, images are normalized to median of 1 before and after combining them.
            method: Method for combining images.
        """
        import ccdproc

        # get CCDData objects
        data = [image.to_ccddata() for image in images]

        # subtract bias?
        if bias is not None:
            bias_data = bias.to_ccddata()
            data = [ccdproc.subtract_bias(d, bias_data) for d in data]

        # normalize?
        if normalize:
            data = [d.divide(np.median(d.data), handle_meta='first_found') for d in data]

        # combine image
        combined = ccdproc.combine(data, method=method,
                                   sigma_clip=True, sigma_clip_low_thresh=5, sigma_clip_high_thresh=5,
                                   mem_limit=350e6, unit='adu',
                                   combine_uncertainty_function=np.ma.std)

        # normalize?
        if normalize:
            combined = combined.divide(np.median(combined.data), handle_meta='first_found')

        # to Image and copy header
        image = Image.from_ccddata(combined)

        # add history
        for i, src in enumerate(images, 1):
            basename = src.header['FNAME'].replace('.fits.fz', '').replace('.fits', '')
            image.header['L1AVG%03d' % i] = (basename, 'Image used for average')
        image.header['RLEVEL'] = (1, 'Reduction level')

        # finished
        return image

    def create_master_bias(self, images: List[Image]) -> Image:
        """Create master bias frame.

        Args:
            images: List of raw bias frames.

        Returns:
            Master bias frame.
        """
        return self._combine_calib_images(images)

    def create_master_dark(self, images: List[Image], bias: Image) -> Image:
        """Create master dark frame.

        Args:
            images: List of raw dark frames.
            bias: Bias frame to subtract from images.

        Returns:
            Master dark frame.
        """
        return self._combine_calib_images(images, bias=bias)

    def create_master_flat(self, images: List[Image], bias: Image) -> Image:
        """Create master flat frame.

        Args:
            images: List of raw flat frames.
            bias: Bias frame to subtract from images.

        Returns:
            Master flat frame.
        """
        return self._combine_calib_images(images, bias=bias, normalize=True, method='median')

    def calibrate(self, image: Image) -> Image:
        """Calibrate a single science frame.

        Args:
            image: Image to calibrate.

        Returns:
            Calibrated image.
        """

        # copy image
        calibrated = image.copy()

        # run pipeline
        return self.run_pipeline(calibrated)

    @staticmethod
    def find_master(archive: Archive, image_type: ImageType, time: Time, instrument: str,
                    binning: str, filter_name: Optional[str] = None, max_days: float = 30.) -> Optional[Image]:
        """Find and download master calibration frame.

        Args:
            archive: Image archive.
            image_type: Image type.
            time: Time to search at.
            instrument: Instrument to use.
            binning: Used binning.
            filter_name: Used filter.
            max_days: Maximum number of days from DATE-OBS to find frames.

        Returns:
            FrameInfo for master calibration frame or None.
        """

        # find reduced frames from +- N days
        log.info('Searching for %s %s master calibration frames%s from instrument %s.',
                 binning, image_type.value, '' if filter_name is None else ' in ' + filter_name, instrument)
        infos = archive.list_frames(start=time - max_days * u.day, end=time + max_days * u.day,
                                    instrument=instrument, image_type=image_type, binning=binning,
                                    filter_name=filter_name, rlevel=1)

        # found none?
        if len(infos) == 0:
            log.warning('Could not find any matching %s calibration frames.', image_type.value)
            return None

        # sort by diff to time and take first
        s = sorted(infos, key=lambda i: abs((i.dateobs - time).sec))
        info = s[0]
        log.info('Found %s frame %s.', image_type.name, info.filename)

        # download it
        return archive.download_frames([info])[0]


__all__ = ['Pipeline']
