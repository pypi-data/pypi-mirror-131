"""Atlas templates module."""
import typing as t
from pathlib import Path

from fw_utils.files import fileglob

ATLAS_DIR = Path(__file__).parents[0] / "templates"

# Constant directory names expected.
P_MASK = "brain_extraction_probability_mask"
S_MASK = "brain_segmentation_template"
E_MASK = "extraction_registration_mask"
R_TEMPLATE = "t1_registration_template"
PRIOR = "Priors2"

ATLASES = {
    "mindboggle": {
        # Data root
        "root": "OASIS-30_Atropos_template",
        # Template file
        "template": "T_template0.nii.gz",
        # Input mask
        "mask": "T_template0_BrainCerebellumProbabilityMask.nii.gz",
        # List of files to use special (not Linear) interpolation
        "files": {
            # Binary values
            "T_template0_BrainCerebellumExtractionMask.nii.gz": "NearestNeighbor",
            "T_template0_BrainCerebellumMask.nii.gz": "NearestNeighbor",
            "T_template0_BrainCerebellumRegistrationMask.nii.gz": "NearestNeighbor",
            "T_template0_BrainCerebellumRegistrationMask.nii.gz": "NearestNeighbor",
            # Discrete values
            "T_template0_glm_4labelsJointFusion.nii.gz": "NearestNeighbor",
            "T_template0_glm_6labelsJointFusion.nii.gz": "NearestNeighbor",
        },
        "out": {
            "priors1.nii.gz": PRIOR,
            "priors2.nii.gz": PRIOR,
            "priors3.nii.gz": PRIOR,
            "priors4.nii.gz": PRIOR,
            "priors5.nii.gz": PRIOR,
            "priors6.nii.gz": PRIOR,
            "T_template0.nii.gz": S_MASK,
            "T_template0_BrainCerebellum.nii.gz": R_TEMPLATE,
            "T_template0_BrainCerebellumMask.nii.gz": E_MASK,
            "T_template0_BrainCerebellumProbabilityMask.nii.gz": P_MASK,
        },
    }
}


def get_atlas(name: str) -> t.Tuple[Path, t.Optional[Path], t.List[str], t.List[str]]:
    """Get template and optional mask for a given atlas name."""
    if name not in ATLASES:
        raise ValueError(f"No atlas '{name}' found.")
    atlas = ATLASES[name]
    atlas_path = ATLAS_DIR / atlas["root"]
    # Get template and mask for registration stage
    template = atlas_path / atlas["template"]
    mask = None
    if "mask" in atlas:
        mask = atlas_path / atlas["mask"]
    # Get all atlas files for transform stage
    a_files = []
    a_interpolations = []
    for f_path in fileglob(atlas_path, pattern="*.nii.gz", recurse=True):
        # Add an entry for filename and interpolation (defaults to Linear)
        a_files.append(str(f_path))
        a_interpolations.append(atlas["files"].get(f_path.name, "Linear"))

    return template, mask, a_files, a_interpolations


def atlas_out_dir_mapping(name: str) -> t.Dict[str, str]:
    """Get out mapping to build out zip folder structure.

    This function returns a dictionary of filename: <folder>/filename in order
    to make a zipfile that will be conformant with what ants-dbm-longitudinal
    expects.
    """
    atlas = ATLASES[name]
    if "out" not in atlas:
        return {}
    return {k: f"{v}/{k}" for k, v in atlas["out"].items()}
