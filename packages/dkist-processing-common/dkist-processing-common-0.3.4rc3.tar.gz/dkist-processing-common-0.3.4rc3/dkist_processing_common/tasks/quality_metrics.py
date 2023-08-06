from dataclasses import dataclass
from dataclasses import field
from typing import Generator
from typing import List

import numpy as np

from dkist_processing_common.models.tags import Tag
from dkist_processing_common.parsers.quality import L0QualityFitsAccess
from dkist_processing_common.parsers.quality import L1QualityFitsAccess
from dkist_processing_common.tasks.base import WorkflowDataTaskBase
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin
from dkist_processing_common.tasks.mixin.quality import QualityMixin


@dataclass
class _QualityTaskTypeData:
    quality_task_type: str
    average_values: List[float] = field(default_factory=list)
    rms_values_across_frame: List[float] = field(default_factory=list)
    datetimes: List[str] = field(default_factory=list)

    @property
    def has_values(self) -> bool:
        return bool(self.average_values)


class QualityL0Metrics(WorkflowDataTaskBase, FitsDataMixin, QualityMixin):
    def run(self) -> None:
        frames: Generator[L0QualityFitsAccess, None, None] = self.fits_data_read_fits_access(
            tags=[Tag.input()],
            cls=L0QualityFitsAccess,
        )

        # determine quality metrics to calculate base upon task types defined in the quality mixin
        quality_task_type_data = [
            _QualityTaskTypeData(quality_task_type=t) for t in self.quality_task_types
        ]

        with self.apm_step("Calculating L0 quality metrics"):
            for frame in frames:
                for quality_task_type_datum in quality_task_type_data:
                    if frame.ip_task_type == quality_task_type_datum.quality_task_type:
                        # find the rms across frame
                        quality_task_type_datum.rms_values_across_frame.append(
                            (np.sqrt(np.mean(frame.data ** 2))) / frame.exposure_time
                        )
                        # find the average value across frame
                        quality_task_type_datum.average_values.append(
                            np.average(frame.data) / frame.exposure_time
                        )
                        quality_task_type_datum.datetimes.append(frame.time_obs)

        with self.apm_step("Sending lists for storage"):
            for quality_task_type_datum in quality_task_type_data:
                if quality_task_type_datum.has_values:
                    self.quality_store_frame_average(
                        datetimes=quality_task_type_datum.datetimes,
                        values=quality_task_type_datum.average_values,
                        task_type=quality_task_type_datum.quality_task_type,
                    )
                    self.quality_store_frame_rms(
                        datetimes=quality_task_type_datum.datetimes,
                        values=quality_task_type_datum.rms_values_across_frame,
                        task_type=quality_task_type_datum.quality_task_type,
                    )


class QualityL1Metrics(WorkflowDataTaskBase, FitsDataMixin, QualityMixin):
    @staticmethod
    def avg_noise(frame) -> float:
        if len(frame.data.shape) == 2:  # 2D data
            corner_square_length = int(frame.data.shape[0] * 0.2)  # 1/5th of x dimension of array
            corner_square_height = int(frame.data.shape[1] * 0.2)  # 1/5th of y dimension of array

            square_1 = frame.data[0:corner_square_length, 0:corner_square_height]  # top left

            square_2 = frame.data[-corner_square_length:, 0:corner_square_height]  # top right

            square_3 = frame.data[0:corner_square_length, -corner_square_height:]  # bottom left

            square_4 = frame.data[-corner_square_length:, -corner_square_height:]  # bottom right

            return np.average(
                [
                    np.std(square_1),
                    np.std(square_2),
                    np.std(square_3),
                    np.std(square_4),
                ]
            )

        if len(frame.data.shape) == 3:  # 3D data
            corner_cube_length = int(frame.data.shape[0] * 0.2)  # 1/5th of x dimension of array
            corner_cube_height = int(frame.data.shape[1] * 0.2)  # 1/5th of y dimension of array
            corner_cube_width = int(frame.data.shape[2] * 0.2)  # 1/5th of z dimension of array

            cube_1 = frame.data[
                0:corner_cube_length, 0:corner_cube_height, 0:corner_cube_width
            ]  # top left front

            cube_2 = frame.data[
                0:corner_cube_length, 0:corner_cube_height, -corner_cube_width:
            ]  # top left back

            cube_3 = frame.data[
                -corner_cube_length:, 0:corner_cube_height, 0:corner_cube_width
            ]  # top right front

            cube_4 = frame.data[
                -corner_cube_length:, 0:corner_cube_height, -corner_cube_width:
            ]  # top right back

            cube_5 = frame.data[
                0:corner_cube_length, -corner_cube_height:, 0:corner_cube_width
            ]  # bottom left front

            cube_6 = frame.data[
                0:corner_cube_length, -corner_cube_height:, -corner_cube_width:
            ]  # bottom left back

            cube_7 = frame.data[
                -corner_cube_length:, -corner_cube_height:, 0:corner_cube_width
            ]  # bottom right front

            cube_8 = frame.data[
                -corner_cube_length:, -corner_cube_height:, -corner_cube_width:
            ]  # bottom right back

            return np.average(
                [
                    np.std(cube_1),
                    np.std(cube_2),
                    np.std(cube_3),
                    np.std(cube_4),
                    np.std(cube_5),
                    np.std(cube_6),
                    np.std(cube_7),
                    np.std(cube_8),
                ]
            )

    def run(self) -> None:
        frames: Generator[L1QualityFitsAccess, None, None] = self.fits_data_read_fits_access(
            tags=[Tag.output(), Tag.frame()], cls=L1QualityFitsAccess
        )

        fried_parameter_values: List[float] = []
        datetimes: List[str] = []
        light_level_values: List[float] = []
        health_stati: List[str] = []  # clever naming
        ao_stati: List[int] = []
        dataset_noise: List[float] = []

        with self.apm_step("Calculating L1 quality metrics"):
            for frame in frames:
                # find the date
                datetimes.append(frame.time_obs)
                # find the Fried Parameter
                fried_parameter_values.append(frame.fried_parameter)
                # find the light level
                light_level_values.append(frame.light_level)
                # find the health status
                health_stati.append(frame.health_status)
                # find the AO status
                ao_stati.append(frame.ao_status)
                # find the average noise value
                dataset_noise.append(self.avg_noise(frame))

        with self.apm_step("Sending lists for storage"):
            self.quality_store_fried_parameter(datetimes=datetimes, values=fried_parameter_values)
            self.quality_store_light_level(datetimes=datetimes, values=light_level_values)
            self.quality_store_noise(datetimes=datetimes, values=dataset_noise)
            self.quality_store_ao_status(ao_statuses=ao_stati)
            self.quality_store_health_status(statuses=health_stati)
