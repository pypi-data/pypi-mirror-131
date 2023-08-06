echo '#### Downloading torch...'
wget -q --show-progress https://download.pytorch.org/whl/cu111/torch-1.9.1%2Bcu111-cp38-cp38-linux_x86_64.whl
echo '#### Installing torch...'
pip install torch*.whl
rm torch*.whl

echo '#### Downloading pytorch3d...'
wget -q --show-progress https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py38_cu111_pyt191/pytorch3d-0.6.0-cp38-cp38-linux_x86_64.whl
echo '#### Installing pytorch3d...'
pip install pytorch3d*.whl
rm pytorch3d*.whl

echo '#### Downloading torch-geometric auxiliary libraries...'
wget -q --show-progress https://data.pyg.org/whl/torch-1.9.0%2Bcu111/torch_sparse-0.6.12-cp38-cp38-linux_x86_64.whl
wget -q --show-progress https://data.pyg.org/whl/torch-1.9.0%2Bcu111/torch_scatter-2.0.9-cp38-cp38-linux_x86_64.whl
wget -q --show-progress https://data.pyg.org/whl/torch-1.9.0%2Bcu111/torch_cluster-1.5.9-cp38-cp38-linux_x86_64.whl
wget -q --show-progress https://data.pyg.org/whl/torch-1.9.0%2Bcu111/torch_spline_conv-1.2.1-cp38-cp38-linux_x86_64.whl
echo '#### Installing torch-geometric auxiliary libraries...'
pip install torch_sparse*.whl
pip install torch_scatter*.whl
pip install torch_cluster*.whl
pip install torch_spline_conv*.whl
rm torch_sparse*.whl
rm torch_scatter*.whl
rm torch_cluster*.whl
rm torch_spline_conv*.whl
