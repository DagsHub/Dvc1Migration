import argparse
import logging
import os
import yaml


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

    # Change stage path to future stage path (dvc.yaml file location)
    stage.path = os.path.join(os.getcwd(), "dvc.yaml")
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


def is_dvc_stage_file(file_path):
    if os.path.splitext(file)[1].lower() != ".dvc" and os.path.basename(file_path).lower() != "dvcfile":
        return False

    with open(file_path, "r") as dvc_file:
        dvc_yaml = yaml.safe_load(dvc_file)
        return dvc_yaml.get("cmd") is not None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--single-stage', nargs=2, metavar=('dvc file', 'stage name'), )

    args = parser.parse_args()
    repo = _get_repo()
    if args.single_stage:
        path, name = args.single_stage
        migrate(repo, path, name)
    else:
        for file in [os.path.join(dir_path, file) for dir_path, _, files in os.walk(".") for file in files]:
            if not is_dvc_stage_file(file):
                continue
            stage_name = os.path.splitext(os.path.basename(file))[0]
            migrate(repo, file, stage_name)

