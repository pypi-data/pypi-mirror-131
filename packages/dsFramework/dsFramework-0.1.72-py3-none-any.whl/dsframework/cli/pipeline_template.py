import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

from dsframework.base.pipeline.pipeline import ZIDS_Pipeline

from .preprocessor.preprocess import generatedProjectNamePreprocess
from .postprocessor.postprocess import generatedProjectNamePostprocess
from .predictors.predictor import generatedProjectNamePredictor
from .forcers.forcer import generatedProjectNameForcer
from .artifacts.shared_artifacts import generatedProjectNameSharedArtifacts

class generatedClass(ZIDS_Pipeline):

    def __init__(self):
        super().__init__()

    def get_artifacts(self):
        return generatedProjectNameSharedArtifacts()

    def build_pipeline(self):
        # Define preprocessor - Automatically added to the pipeline
        self.preprocessor = generatedProjectNamePreprocess(artifacts=self.artifacts)

        # Define and add predictor to the pipeline
        self.predictor = generatedProjectNamePredictor()
        self.add_component(self.predictor)

        # Define and add forcer to the pipeline
        self.forcer = generatedProjectNameForcer()
        self.add_component(self.forcer)

        # Define postprocessor - Automatically added to the pipeline
        self.postprocessor = generatedProjectNamePostprocess(artifacts=self.artifacts)

    def preprocess(self, **kwargs):
        return self.preprocessor(**kwargs)

    def postprocess(self, predictables):
        return self.postprocessor(predictables)
