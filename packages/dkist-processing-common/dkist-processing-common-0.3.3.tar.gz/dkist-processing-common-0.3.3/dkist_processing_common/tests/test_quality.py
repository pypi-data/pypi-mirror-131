import json
import random

import numpy as np
import pytest
from astropy.io import fits
from astropy.wcs import WCS
from dkist_data_simulator.spec122 import Spec122Dataset
from dkist_data_simulator.spec214 import Spec214Dataset

from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.quality_metrics import QualityL0Metrics
from dkist_processing_common.tasks.quality_metrics import QualityL1Metrics


class BaseSpec214l0Dataset(Spec122Dataset):
    def __init__(self, instrument="vbi"):
        self.array_shape = (1, 10, 10)
        super().__init__(
            dataset_shape=(10, 10, 10),
            array_shape=self.array_shape,
            time_delta=1,
            instrument=instrument,
            file_schema="level0_spec214",
        )


class BaseSpec214Dataset(Spec214Dataset):
    def __init__(self, instrument="vbi"):
        self.array_shape = (10, 10)
        super().__init__(
            dataset_shape=(2, 10, 10),
            array_shape=self.array_shape,
            time_delta=1,
            instrument=instrument,
        )

    @property
    def fits_wcs(self):
        w = WCS(naxis=2)
        w.wcs.crpix = self.array_shape[1] / 2, self.array_shape[0] / 2
        w.wcs.crval = 0, 0
        w.wcs.cdelt = 1, 1
        w.wcs.cunit = "arcsec", "arcsec"
        w.wcs.ctype = "HPLN-TAN", "HPLT-TAN"
        w.wcs.pc = np.identity(self.array_ndim)
        return w


@pytest.fixture
def quality_L0_task(tmp_path, recipe_run_id):
    with QualityL0Metrics(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        for i in range(10):
            header_dict = [
                d.header(required_only=False, expected_only=False) for d in BaseSpec214l0Dataset()
            ][0]
            data = np.ones(shape=BaseSpec214l0Dataset().array_shape)
            hdu = fits.PrimaryHDU(data=data)
            for key, value in header_dict.items():
                hdu.header[key] = value
            hdu.header["IPTASK"] = random.choice(
                [
                    "observe",
                    "focus",
                    "align",
                    "dark",
                    "gain",
                    "polcal",
                    "telcal",
                    "wavecal",
                    "scatteredlight",
                    "target",
                    "transmission",
                ]
            )
            hdul = fits.HDUList([hdu])
            task.fits_data_write(hdu_list=hdul, tags=[Tag.input()])
        yield task
    task.scratch.purge()
    task.constants.purge()


def test_dark_rms_across_frame(quality_L0_task):
    """
    Given: a task with the QualityL0Metrics class
    When: checking that the dark rms across frame metric was created and stored correctly
    Then: the metric is encoded as a json object, which when opened contains a dictionary with the expected schema
    """
    # call task and assert that things were created (tagged files on disk with quality metric info in them)
    task = quality_L0_task
    task()
    files = list(task.read(tags=[Tag.quality("FRAME_RMS"), Tag.task("DARK")]))
    for file in files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert all(isinstance(item, str) for item in data["x_values"])
            assert all(isinstance(item, float) for item in data["y_values"])


def test_gain_rms_across_frame(quality_L0_task):
    """
    Given: a task with the QualityL0Metrics class
    When: checking that the gain rms across frame metric was created and stored correctly
    Then: the metric is encoded as a json object, which when opened contains a dictionary with the expected schema
    """
    # call task and assert that things were created (tagged files on disk with quality metric info in them)
    task = quality_L0_task
    task()
    files = list(task.read(tags=[Tag.quality("FRAME_RMS"), Tag.task("GAIN")]))
    for file in files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert all(isinstance(item, str) for item in data["x_values"])
            assert all(isinstance(item, float) for item in data["y_values"])


def test_dark_average_value(quality_L0_task):
    """
    Given: a task with the QualityL0Metrics class
    When: checking that the dark average value metric was created and stored correctly
    Then: the metric is encoded as a json object, which when opened contains a dictionary with the expected schema
    """
    task = quality_L0_task
    task()
    files = list(task.read(tags=[Tag.quality("FRAME_AVERAGE"), Tag.task("DARK")]))
    for file in files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert all(isinstance(item, str) for item in data["x_values"])
            assert all(isinstance(item, float) for item in data["y_values"])


def test_gain_average_value(quality_L0_task):
    """
    Given: a task with the QualityL0Metrics class
    When: checking that the gain average value metric was created and stored correctly
    Then: the metric is encoded as a json object, which when opened contains a dictionary with the expected schema
    """
    task = quality_L0_task
    task()
    files = list(task.read(tags=[Tag.quality("FRAME_AVERAGE"), Tag.task("GAIN")]))
    for file in files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert all(isinstance(item, str) for item in data["x_values"])
            assert all(isinstance(item, float) for item in data["y_values"])


@pytest.fixture
def quality_L1_task(tmp_path, recipe_run_id):
    with QualityL1Metrics(
        recipe_run_id=recipe_run_id,
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        for i in range(10):
            header_dict = [
                d.header(required_only=False, expected_only=False) for d in BaseSpec214Dataset()
            ][0]
            data = np.ones(shape=BaseSpec214Dataset().array_shape)
            hdu = fits.PrimaryHDU(data=data)
            for key, value in header_dict.items():
                hdu.header[key] = value
            hdul = fits.HDUList([hdu])
            task.fits_data_write(hdu_list=hdul, tags=[Tag.output(), Tag.frame()])
        yield task
    task.scratch.purge()
    task.constants.purge()


def test_fried_parameter(quality_L1_task):
    """
    Given: a task with the QualityL1Metrics class
    When: checking that the fried parameter metric was created and stored correctly
    Then: the metric is encoded as a json object, which when opened contains a dictionary with the expected schema
    """
    task = quality_L1_task
    task()
    files = list(task.read(tags=Tag.quality("FRIED_PARAMETER")))
    for file in files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert all(isinstance(item, str) for item in data["x_values"])
            assert all(isinstance(item, float) for item in data["y_values"])
            # assert data["task_type"] == "observe"


def test_light_level(quality_L1_task):
    """
    Given: a task with the QualityL1Metrics class
    When: checking that the light level metric was created and stored correctly
    Then: the metric is encoded as a json object, which when opened contains a dictionary with the expected schema
    """
    task = quality_L1_task
    task()
    files = list(task.read(tags=Tag.quality("LIGHT_LEVEL")))
    for file in files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert all(isinstance(item, str) for item in data["x_values"])
            assert all(isinstance(item, float) for item in data["y_values"])
            # assert data["task_type"] == "observe"


def test_health_status(quality_L1_task):
    """
    Given: a task with the QualityL1Metrics class
    When: checking that the health status metric was created and stored correctly
    Then: the metric is encoded as a json object, which when opened contains a dictionary with the expected schema
    """
    task = quality_L1_task
    task()
    files = list(task.read(tags=Tag.quality("HEALTH_STATUS")))
    for file in files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, list)


def test_ao_status(quality_L1_task):
    """
    Given: a task with the QualityL1Metrics class
    When: checking that the AO status metric was created and stored correctly
    Then: the metric is encoded as a json object, which when opened contains a dictionary with the expected schema
    """
    task = quality_L1_task
    task()
    files = list(task.read(tags=Tag.quality("AO_STATUS")))
    for file in files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, list)


def test_noise(quality_L1_task):
    """
    Given: a task with the QualityL1Metrics class
    When: checking that the nosie metric was created and stored correctly
    Then: the metric is encoded as a json object, which when opened contains a dictionary with the expected schema
    """
    task = quality_L1_task
    task()
    files = list(task.read(tags=Tag.quality("NOISE")))
    for file in files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert all(isinstance(item, str) for item in data["x_values"])
            assert all(isinstance(item, float) for item in data["y_values"])
