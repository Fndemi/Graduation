```sh
conda install -c conda-forge ipykernal
conda deactivate
conda remove -n Testing --all -y
conda create -n Testing python=3.10.0 ipykernel -y
conda activate Testing
```
