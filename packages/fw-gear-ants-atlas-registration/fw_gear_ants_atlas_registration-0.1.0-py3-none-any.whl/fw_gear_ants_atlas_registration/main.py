"""Main module."""

import logging
import shutil
import zipfile
from pathlib import Path

from fw_utils.files import fileglob

from .atlas import atlas_out_dir_mapping
from .workflow import registration_workflow, setup_registration

log = logging.getLogger(__name__)


def run(
    fixed_image,
    fixed_mask,
    moving_image,
    moving_mask,
    config,
    atlas_name,
    atlas_paths,
    atlas_interpolations,
    out_dir,
) -> int:
    """Run workflow and prepare outputs."""
    reg_node = setup_registration(
        fixed_image, fixed_mask, moving_image, moving_mask, config
    )
    reg_workflow = registration_workflow(
        Path("/flywheel/v0"), reg_node, atlas_paths, atlas_interpolations
    )
    reg_workflow.run()
    zip_outputs(atlas_name, out_dir)

    return 0


def zip_outputs(name: str, out_dir: Path):
    out_map = atlas_out_dir_mapping(name)
    transformed_dir = out_dir / "transformed"
    out_file = out_dir / f"{name}.zip"
    with zipfile.ZipFile(out_file, "w") as z_file:
        for file_ in fileglob(transformed_dir, pattern="*.nii.gz", recurse=True):
            f_name = file_.name
            name = out_map[f_name] if f_name in out_map else f_name
            z_file.write(file_, arcname=name)
    shutil.rmtree(transformed_dir)
