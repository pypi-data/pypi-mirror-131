from typing import Generator
from typing import List

import numpy as np

from dkist_processing_common.models.tags import Tag
from dkist_processing_common.parsers.quality import L0QualityFitsAccess
from dkist_processing_common.parsers.quality import L1QualityFitsAccess
from dkist_processing_common.tasks.base import WorkflowDataTaskBase
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin
from dkist_processing_common.tasks.mixin.quality import QualityMixin


class QualityL0Metrics(WorkflowDataTaskBase, FitsDataMixin, QualityMixin):
    def run(self) -> None:
        frames: Generator[L0QualityFitsAccess, None, None] = self.fits_data_read_fits_access(
            tags=[Tag.input()],
            cls=L0QualityFitsAccess,
        )

        datetimes: List[str] = []
        dark_average_values: List[float] = []
        gain_average_values: List[float] = []
        dark_rms_values_across_frame: List[float] = []
        gain_rms_values_across_frame: List[float] = []
        task_type: List[str] = []

        with self.apm_step("Calculating L0 quality metrics"):
            for frame in frames:
                # find the date
                datetimes.append(frame.time_obs)
                # find the task type
                task_type.append(frame.ip_task_type)
                # find the rms across frame
                if frame.ip_task_type == "dark":
                    dark_rms_values_across_frame.append(
                        (np.sqrt(np.mean(frame.data ** 2))) / frame.exposure_time
                    )
                if frame.ip_task_type == "gain":
                    gain_rms_values_across_frame.append(
                        (np.sqrt(np.mean(frame.data ** 2))) / frame.exposure_time
                    )
                # find the average value across frame
                if frame.ip_task_type == "dark":
                    dark_average_values.append(np.average(frame.data) / frame.exposure_time)
                if frame.ip_task_type == "gain":
                    gain_average_values.append(np.average(frame.data) / frame.exposure_time)

        with self.apm_step("Sending lists for storage"):
            self.quality_store_frame_average(
                datetimes=datetimes, values=dark_average_values, task_type="dark"
            )
            self.quality_store_frame_average(
                datetimes=datetimes, values=gain_average_values, task_type="gain"
            )
            self.quality_store_frame_rms(
                datetimes=datetimes, values=dark_rms_values_across_frame, task_type="dark"
            )
            self.quality_store_frame_rms(
                datetimes=datetimes, values=gain_rms_values_across_frame, task_type="gain"
            )


class QualityL1Metrics(WorkflowDataTaskBase, FitsDataMixin, QualityMixin):
    @staticmethod
    def avg_noise(dataset_noise, frame):
        if len(frame.data.shape) == 2:  # 2D data
            corner_square_length = int(frame.data.shape[0] * 0.2)  # 1/5th of x dimension of array
            corner_square_height = int(frame.data.shape[1] * 0.2)  # 1/5th of y dimension of array

            square_1 = frame.data[0:corner_square_length, 0:corner_square_height]  # top left

            square_2 = frame.data[-corner_square_length:, 0:corner_square_height]  # top right

            square_3 = frame.data[0:corner_square_length, -corner_square_height:]  # bottom left

            square_4 = frame.data[-corner_square_length:, -corner_square_height:]  # bottom right

            dataset_noise.append(
                np.average(
                    [
                        np.std(square_1),
                        np.std(square_2),
                        np.std(square_3),
                        np.std(square_4),
                    ]
                )
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

            dataset_noise.append(
                np.average(
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
                if frame.ao_status == 1:
                    ao_stati.append(frame.ao_status)
                # find the average noise value
                self.avg_noise(dataset_noise, frame)

        with self.apm_step("Sending lists for storage"):
            self.quality_store_fried_parameter(datetimes=datetimes, values=fried_parameter_values)
            self.quality_store_light_level(datetimes=datetimes, values=light_level_values)
            self.quality_store_noise(datetimes=datetimes, values=dataset_noise)
            self.quality_store_ao_status(ao_statuses=ao_stati)
            self.quality_store_health_status(statuses=health_stati)
