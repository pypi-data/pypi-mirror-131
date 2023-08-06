import warnings
from pathlib import Path
from .pl_ileum_detection_resnet import IleumDetectionResnet
from .pl_googlenet import GoogleNet
from .pl_polyp_detection_resnet import PolypDetectionResnet
import torch

AVAILABLE_AI_MODELS = ["polyp", "ileum", "tool", "ileocaecalvalve", "appendix", "blurry", "body"]


def get_ckpt_path(ai_name: str, version: float, path_models: Path) -> Path:
    """Function selects folder which matches the label in the given folder and then\
        returns a Path object of the corresponding model version

    Args:
        ai_name (str): name of the ai
        version (float): version number (one decimal!)
        path_models (Path): Path object pointing to the base model folder

    Returns:
        Path: Path object pointing to the desired model
    """

    version = "{:.1f}".format(version)
    _path = path_models.joinpath(f"{ai_name}/{version}.ckpt")
    if not _path.exists():
        warnings.warn(f"Path {_path} does not exist!")
        print(_path)

    return _path


def load_model(model_name: str, version: float, _eval: bool, base_path_models: Path):
    """Function loads model for given name.

    Args:
        model_name (str): One of "polyp", "ileum", "tool", "ileocaecalvalve", "appendix"
        version (float): version number.
        eval (bool): If True, model is loaded in eval mode.
        base_path_models(Path): Points to directory containing folders named by models, containing checkpoints named by
            version numbers (e.g. '0.1.ckpt')

    Returns:
        [PL Model]: Model for given name.
    """
    assert model_name in AVAILABLE_AI_MODELS

    ckpt_path = get_ckpt_path(model_name, version, base_path_models)
    if model_name == "polyp":
        Model = PolypDetectionResnet
    if model_name == "ileum":
        Model = GoogleNet
    if model_name == "tool":
        Model = GoogleNet
    if model_name == "ileocaecalvalve":
        Model = GoogleNet
    if model_name == "appendix":
        Model = GoogleNet
    if model_name == "blurry":
        Model = GoogleNet
    if model_name == "body":
        Model = GoogleNet

    trained_model = Model.load_from_checkpoint(checkpoint_path=ckpt_path)

    if torch.cuda.is_available():
        trained_model.cuda(0)
    # trained_model.to(0)
    if _eval:
        trained_model.eval()
        trained_model.freeze()
    else: 
        trained_model.train()

    return trained_model
