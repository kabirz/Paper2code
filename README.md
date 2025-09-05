## paper code

### set up enviroment

1. Clone this project


2. Install [nvidia aiqtoolkit](https://docs.nvidia.com/aiqtoolkit/latest/index.html)([repo](https://github.com/NVIDIA/NeMo-Agent-Toolkit))
```shell
cd <this_git_repo_root_path>
uv venv .venv -p python3.12
source .venv/bin/activate
git clone https://github.com/NVIDIA/NeMo-Agent-Toolkit aiqtoolkit --recursive
cd aiqtoolkit 
git lfs install
git lfs fetch
git lfs pull
uv pip install ".[langchain]"
```

3. Install this package

```shell
cd <this_git_repo_root_path>
uv pip install  -e .
```

### run
```shell
nat run --config_file paper2code/configs/config.yml --input "prompt"
```

### azure open ai

set enviroment variable `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`.

