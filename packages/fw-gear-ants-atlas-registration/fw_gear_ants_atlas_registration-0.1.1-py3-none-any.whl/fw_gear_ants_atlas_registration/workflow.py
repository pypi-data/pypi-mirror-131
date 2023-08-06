"""Handle antsRegistration nipype workflow."""
import logging as gen_log
import os
import typing as t
from pathlib import Path

from nipype import config, logging

cfg = dict(  # pragma: no cover
    execution={
        "stop_on_first_crash": True,
        "hash_method": "content",
        "remove_unnecessary_outputs": False,
        "crashfile_format": "txt",
        "crashdump_dir": "/flywheel/v0/output",
    },
)

config.update_config(cfg)
logging.update_logging(config)

import nipype.pipeline.engine as pipeline_engine
from nipype.interfaces.ants import ApplyTransforms, Registration
from nipype.interfaces.io import DataSink

log = gen_log.getLogger(__name__)


def registration_workflow(
    base_dir: Path,
    reg_node: pipeline_engine.Node,
    atlas_files: t.List[str],
    atlas_interpolations: t.List[str],
) -> pipeline_engine.Workflow:
    log.info("Setting up registration workflow")
    log.debug(f"Setting workflow base dir to {base_dir / 'work'}")

    reg_workflow = pipeline_engine.Workflow(
        name="ants_atlas_registration_workflow", base_dir=(base_dir / "work")
    )

    log.info("Creating MapNode over atlas files and interpolations")
    # ApplyTransform node that takes output from Registration
    # And maps over the specific atlas files and their interpolations
    transform_node = pipeline_engine.MapNode(
        ApplyTransforms(),
        name="transform_atlas",
        iterfield=["input_image", "interpolation"],
    )
    # Mapped atlas files with their corresponding interpolation
    transform_node.inputs.input_image = atlas_files
    transform_node.inputs.interpolation = atlas_interpolations
    # Fixed inputs
    transform_node.inputs.reference_image = reg_node.inputs.fixed_image[0]
    transform_node.inputs.dimension = reg_node.inputs.dimension
    transform_node.inputs.float = reg_node.inputs.float
    transform_node.inputs.num_threads = reg_node.inputs.num_threads
    transform_node.inputs.out_postfix = ""

    log.info(f"Creating DataSink node")
    sink = pipeline_engine.Node(DataSink(), name="sink")
    sink.inputs.base_directory = str(base_dir)

    log.info("Connecting nodes")

    try:  # pragma: no cover
        reg_workflow.connect(
            [
                (
                    reg_node,
                    sink,
                    [
                        ("warped_image", "output.@warped"),
                        ("composite_transform", "transforms"),
                    ],
                ),
                (
                    reg_node,
                    transform_node,
                    [
                        ("composite_transform", "transforms"),
                    ],
                ),
                (
                    transform_node,
                    sink,
                    [
                        # Create a new directory for output images
                        ("output_image", "output.transformed"),
                    ],
                ),
            ]
        )
    except Exception as exc:
        log.error("Unhandled exception", exc_info=True)
        raise RuntimeError(*exc.args) from exc

    return reg_workflow


def setup_registration(
    fixed_image: Path,
    fixed_mask: t.Optional[Path],
    moving_image: Path,
    moving_mask: t.Optional[Path],
    config: t.Dict,
) -> pipeline_engine.Node:
    """Set up nipype antsRegistration node.

    Args:
        fixed_image (Path): Image to which the moving image should be
            transformed.
        fixed_mask (Path): Mask image to which the moving image sh
        moving_image (Path): Image that will be transformed.
        config (Dict): Configuration dictionary.
    """
    reg_node = pipeline_engine.Node(Registration(), name="antsRegistration")
    # Image inputs
    reg_node.inputs.fixed_image = fixed_image
    if fixed_mask and moving_mask:
        reg_node.inputs.fixed_image_mask = fixed_mask
        reg_node.inputs.moving_image_mask = moving_mask
    reg_node.inputs.moving_image = moving_image

    for key, val in config.items():
        setattr(reg_node.inputs, key, val)

    return reg_node
