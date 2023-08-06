"""Parse and validation config.json."""
import json
import logging
import typing as t
from json.decoder import JSONDecodeError
from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext

from .atlas import get_atlas

log = logging.getLogger(__name__)


# Single-valued config/input options
SINGLE_VALUES = [
    "dimension",
    "interpolation",
    "interpolation_parameters",
    "collapse_output_transforms",
    "initialize_transforms_per_stage",
    "float",
    "output_transform_prefix",
    "output_warped_image",
    "output_inverse_warped_image",
    "winsorize_upper_quantile",
    "winsorize_lower_quantile",
    "num_threads",
    "args",
]

# Multi-valued config/input options, all must match # of stages.
STAGE_VALUES = [
    "metric",
    "metric_weight",
    "radius_or_number_of_bins",
    "sampling_strategy",
    "sampling_percentage",
    "use_estimate_learning_rate_once",
    "use_histogram_matching",
    "transforms",
    "transform_parameters",
    "restrict_deformation",
    "number_of_iterations",
    "smoothing_sigmas",
    "sigma_units",
    "shrink_factors",
    "convergence_threshold",
    "convergence_window_size",
]

TUPLEIZE_VALUES = ["transform_parameters"]


def parse_config(
    gear_context: GearToolkitContext,
) -> t.Tuple[
    t.Dict,
    Path,
    t.Optional[Path],
    Path,
    t.Optional[Path],
    str,
    t.List[str],
    t.List[str],
]:
    """Parse and validate antsRegistration config values and inputs.

    Returns:
        tuple:
            dict: Validated input values for antsRegistration node.
            Path: Fixed image
            Optional[Path]: Optional fixed image mask
            Path: Moving image
            Optional[Path]: Optional moving image mask
    """
    # Build config dict of inputs to pass to Registration interface.
    config = dict()
    raw_config = gear_context.config_json["config"]

    # Pop and save non-antsRegistration values
    atlas = raw_config.pop("atlas")
    debug = raw_config.pop("debug")

    # Propagate debug to 'verbose' in antsRegistration
    config["verbose"] = debug
    # Needed for ApplyTransform stage
    config["write_composite_transform"] = True
    try:
        transforms = json.loads(raw_config["transforms"])
        num_stages = len(transforms)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Could not decode config value transforms with value"
        ) from exc
    log.info(f"Using {num_stages} stages: {transforms}")

    for k, v in raw_config.items():
        if v is None:
            continue
        if k in STAGE_VALUES:
            val = parse_stage_val(k, v)
            if len(val) != num_stages:
                raise ValueError(
                    f"Stage-dependent parameter {k} with {len(val)} values "
                    f"did not match number of stages {num_stages}. Exiting"
                )
            config[k] = val
        elif k in SINGLE_VALUES:
            config[k] = v
        else:
            # Shouldn't happen in gear, but leaving in case this is
            # pip-installed.
            raise ValueError(f"Unknown parameter {k}")
        if k in TUPLEIZE_VALUES:
            config[k] = tupleize(config[k])

    fixed_image = gear_context.get_input_path("fixed_image")
    fixed_image = Path(fixed_image)
    fixed_mask = gear_context.get_input_path("fixed_image_mask")
    if fixed_mask:
        fixed_mask = Path(fixed_mask)

    moving_image, moving_mask, atlas_paths, atlas_interpolations = get_atlas(atlas)
    log.info(
        f"Loaded atlas {atlas} with template: {moving_image}, " f"mask: {moving_mask}"
    )
    return (
        config,
        fixed_image,
        fixed_mask,
        moving_image,
        moving_mask,
        atlas,
        atlas_paths,
        atlas_interpolations,
    )


param = t.List[t.Union[t.List[t.Union[str, float, int]], str, float, int]]


def parse_stage_val(param: str, raw: str) -> param:
    """Parse multi-valued stage value which is not supported in FW config.

    i.e. `metric` could have multiple metrics at each stage where the expected
    input would be something like ['Mattes',['CC','MI'], being the Mattes
    metric at the first stage and a summed weighting of the CC and MI metrics
    in the second stage.

    In FW config, we would represent this as ["Mattes","CC,MI"].

    Args:
        raw (str): FW config value

    Returns:
        (List with each element either a list of values or a value.  Where
        value is a string, float, or int): Nipype
        compatible input.
    """
    try:
        val = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Could not decode config value{param} with value {raw}"
        ) from exc
    nipyp_compat = list()
    for stage in val:
        if isinstance(stage, str):
            try:
                parsed_val = int(stage)
            except ValueError:
                try:
                    parsed_val = float(stage)
                except ValueError:
                    parsed_val = stage
            nipyp_compat.append(parsed_val)
        else:
            nipyp_compat.append(stage)

    return nipyp_compat


def tupleize(vals: t.List) -> t.List:
    return [tuple(val) if hasattr(val, "__iter__") else (val,) for val in vals]
