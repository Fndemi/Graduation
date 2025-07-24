## Testing Example

Here we are creating our Testing env.
We install pandas in our Testing env.
We observe which packages are installed Testing.
We observe which packsages are installed in base
We can use python binary to execute the python in the context of conda
check what binary is being loaded.

```sh
conda create -n hello python 3.11.0 -y
conda activate
conda install -c conda-forge pandas
pip list
conda deactivate
pip list
conda activate Testing
python app.py
whereis python
whereis python3
pip install -r requirements.txt 
```