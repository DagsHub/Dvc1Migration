import argparse
import logging
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _get_repo():
    from dvc.repo import Repo

    return Repo()


def migrate(dvc, path, name):
    from dvc.dvcfile import SingleStageFile, PipelineFile

    dvcfile = SingleStageFile(dvc, path)
    stage = dvcfile.stage
    stage.name = name
    p_file = PipelineFile(dvc, "dvc.yaml")

    # using internal APIs, there are checks on `dump()`.
    p_file._dump_pipeline_file(stage)
    p_file._dump_lockfile(stage)
    logger.info("'{}' has been added to 'dvc.yaml' and 'dvc.lock'.")

    os.rename(dvcfile.path, dvcfile.path + ".bak")
    logger.info("'{0}' has been renamed to '{0}.bak'.".format(dvcfile.path))
    logger.info(
        "Delete it after carefully reviewing"
        " 'dvc.lock' and 'dvc.yaml' or use it to rollback."
    )


def rollback(dvc, path, name):
    from dvc.utils.stage import dump_stage_file
    from dvc.dvcfile import PipelineFile

    dvcfile = PipelineFile(dvc, "dvc.yaml")
    stage = dvcfile.stages[name]
    dump_stage_file(path, stage.dumpd())
    
    # don't have an API for removing entry.
    logger.warning(
        "Please remove entries regarding '{name}' from 'dvc.yaml' and 'dvc.lock'.".format(
            name=name
        )
    )


if __name__ == "__main__":
    ### Usage: ./migrator.py <dot-dvc-file> <stage_name>
    ###        ./migrator.py featurize.dvc featurize
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rollback", action="store_true")
    parser.add_argument(
        "path", help="Path to dvcfile (to output in terms of rollback)"
    )
    parser.add_argument(
        "name", help="Name of stage to output (to use in terms of rollback)"
    )

    args = parser.parse_args()
    repo = _get_repo()
    if args.rollback:
        rollback(repo, args.path, args.name)
    else:
        migrate(repo, args.path, args.name)
