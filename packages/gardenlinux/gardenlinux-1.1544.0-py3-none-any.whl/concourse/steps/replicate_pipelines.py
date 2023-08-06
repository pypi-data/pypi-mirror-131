import logging

import ci.log
import concourse.replicator

ci.log.configure_default_logging()
logger = logging.getLogger(__name__)


## it may seem pointless to wrap replicate-pipelines - however, this will at least help
## linters to detect errors that would be missed if the call were inlined in mako
def replicate_pipelines(
    cfg_set,
    job_mapping,
    pipelines_not_to_delete: list,
):
    # prevent own replication pipeline from being removed
    def filter_own_pipeline(pipeline_name: str):
        return pipeline_name in pipelines_not_to_delete

    result = concourse.replicator.replicate_pipelines(
        cfg_set=cfg_set,
        job_mapping=job_mapping,
        unpause_pipelines=False,
        unpause_new_pipelines=True,
        expose_pipelines=True,
        remove_pipelines_filter=filter_own_pipeline,
    )
    return result
