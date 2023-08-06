from dkist_processing_common import ParsedL0InputTaskBase
from dkist_processing_common.tasks.mixin.metadata_store import MetadataStoreMixin
from dkist_processing_common.tasks.mixin.quality import QualityMixin


class SubmitQuality(ParsedL0InputTaskBase, QualityMixin, MetadataStoreMixin):
    def run(self):
        with self.apm_step("Building quality report"):
            report = self.quality_build_report()
        with self.apm_step("Submitting quality report"):
            self.metadata_store_add_quality_report(
                dataset_id=self.dataset_id, quality_report=report
            )
