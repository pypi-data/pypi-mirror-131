# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marcelle']

package_data = \
{'': ['*']}

install_requires = \
['filetype>=1.0.8,<2.0.0',
 'keras2onnx>=1.7.0,<2.0.0',
 'numpy>=1.21.4,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'tensorflow>=2.7.0,<3.0.0',
 'tensorflowjs>=3.11.0,<4.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'marcelle',
    'version': '0.0.5',
    'description': 'Python package for interacting with Marcelle',
    'long_description': '# Marcelle - Python Package\n\nA python package for interacting with a Marcelle backend from python.\n\n> See: [http://marcelle.dev](http://marcelle.dev)\n\n## Status ⚠️\n\nMarcelle is still experimental and is currently under active development. Breaking changes are expected.\n\n## Installing\n\n```shell\npip install .\n```\n\n## Basic Usage\n\n### Keras Callback\n\n```py\nfrom marcelle import MarcelleCallback\n\nmrc_callback = KerasCallback(\n    backend_root="http://localhost:3030",\n    disk_save_formats=["h5", "tfjs"],\n    remote_save_format="tfjs",\n    model_checkpoint_freq=None,\n    base_log_dir="marcelle-logs",\n    run_params={},\n)\n\nmodel.fit(\n  # ...\n  callbacks = [\n    mrc_callback,\n    # other callbacks\n  ]\n)\n```\n\n### Writer (for custom training loops)\n\n```py\nfrom marcelle import Writer\n\nwriter = Writer(\n    backend_root="http://localhost:3030",\n    disk_save_formats=["h5", "tfjs"],\n    remote_save_format="tfjs",\n    base_log_dir="marcelle-logs",\n    source="keras",\n)\n\nwriter.create_run(model, params, loss.name)\nwriter.train_begin(epochs)\n\nfor epoch in range(epochs):\n  # ...\n  logs = {\n    "loss": 1.3,\n    "accuracy": 0.7,\n    "val_loss": 2.3,\n    "val_accuracy": 0.52,\n  }\n  assets = ["path/to/asset1.wav", "path/to/asset2.wav"]\n  self.writer.save_epoch(epoch, logs=logs, save_checkpoint=True, assets=assets)\n\nwriter.train_end(save_checkpoint=True)\n```\n\n### Batch upload\n\nUseful when training was done offline or connection to server failed during the training.\n\n```py\nfrom glob import glob\nimport os\nfrom marcelle import MarcelleRemote, MarcelleUploader\n\n\nif __name__ == "__main__":\n    LOG_DIR = "marcelle-logs"\n    uploader = MarcelleUploader(\n        MarcelleRemote(\n            backend_root="http://localhost:3030",\n            save_format="tfjs",\n            source="keras",\n        )\n    )\n    runs = [d for d in glob(os.path.join(LOG_DIR, "*")) if os.path.isdir(d)]\n    for run in runs:\n        uploader.upload(run)\n\n```\n\n## ✍️ Authors\n\n- [@JulesFrancoise](https://github.com/JulesFrancoise/)\n- [@bcaramiaux](https://github.com/bcaramiaux/)\n',
    'author': 'Jules Françoise',
    'author_email': 'me@julesfrancoise.com',
    'maintainer': 'Jules Françoise',
    'maintainer_email': 'me@julesfrancoise.com',
    'url': 'https://marcelle.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
