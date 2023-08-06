import tempfile

import requests
import pathlib
import zipfile

from baseten_scaffolding.definitions.custom import CustomScaffoldDefinition
from baseten_scaffolding.definitions.sklearn import SKLearnScaffoldDefinition

DEFAULT_SKLEARN_REQUIREMENTS_FILE = tempfile.NamedTemporaryFile()
DEFAULT_SKLEARN_REQUIREMENTS_FILE.write(b"scikit-learn==0.22.2\njoblib==0.13.0")
DEFAULT_SKLEARN_REQUIREMENTS_FILE.seek(0)

a_presigned_url = 'https://baseten-user-models-dev.s3.amazonaws.com/organizations/gpqvbql/models/7d223f76-22a8-4a88-824e-dfc40cca04b4/model.zip?AWSAccessKeyId=AKIA4FWSEGGQQBKMVOB5&Signature=NOezKYr%2FGlOF3LsoovCrfRjG3yk%3D&Expires=1632331907'

model_request = requests.get(a_presigned_url)


# from sklearn.ensemble import RandomForestClassifier
# rfc = RandomForestClassifier()
#
# # def migrate_a_sklearn_model(s3_key: str, model_type: str):
# scaffold = SKLearnScaffoldDefinition(
#     rfc,
#     requirements_file=DEFAULT_SKLEARN_REQUIREMENTS_FILE.name,
#     model_type='Linear Model',
# )
#
# with open(pathlib.Path(scaffold.scaffold_model_dir, scaffold.model_filename), 'wb') as f:
#     f.write(model_request.content)

EMBEDDING_REQUIREMENTS_FILE = tempfile.NamedTemporaryFile()
EMBEDDING_REQUIREMENTS_FILE.write(b"tensorflow-hub==0.10.0\ntensorflow==2.4.0\nscikit-learn==0.23.2")
EMBEDDING_REQUIREMENTS_FILE.seek(0)

request_data = tempfile.NamedTemporaryFile(suffix='zip')
request_data.write(model_request.content)
zf = zipfile.ZipFile(request_data)

import pathlib

model_files = []
for model_file in zf.namelist():
    local_name = pathlib.Path(model_file).name
    model_files.append(local_name)
    with open(local_name, 'wb') as f:
        f.write(zf.read(model_file))



custom_scaffold = CustomScaffoldDefinition(
    None,
    requirements_file=EMBEDDING_REQUIREMENTS_FILE.name,
    model_files=model_files,
    model_class='MyEmbeddingModel'
)
custom_scaffold.docker_build_string


# with open(pathlib.Path(xxx.scaffold_model_dir, xxx.model_filename), 'wb') as f:
#     f.write(model_request.content)

# backend/oracles/model_deployer/services.py:def _presigned_s3_key(s3_key
