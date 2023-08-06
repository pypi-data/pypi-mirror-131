printf '\n#### Downloading torch...\n'
wget -q --show-progress https://download.pytorch.org/whl/cu111/torch-1.9.1%2Bcu111-cp38-cp38-linux_x86_64.whl
printf '\n#### Installing torch...\n'
pip install torch*.whl
rm torch*.whl

printf '\n#### Downloading torchvision...\n'
wget -q --show-progress https://download.pytorch.org/whl/cu111/torchvision-0.10.1%2Bcu111-cp38-cp38-linux_x86_64.whl
printf '\n#### Installing torchvision...\n'
pip install torchvision*.whl
rm torchvision*.whl

printf '\n#### Downloading pytorch3d...\n'
wget -q --show-progress https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py38_cu111_pyt191/pytorch3d-0.6.0-cp38-cp38-linux_x86_64.whl
printf '\n#### Installing pytorch3d...\n'
pip install pytorch3d*.whl
rm pytorch3d*.whl

printf '\n#### Downloading torch-geometric auxiliary libraries...\n'
wget -q --show-progress https://data.pyg.org/whl/torch-1.9.0%2Bcu111/torch_sparse-0.6.12-cp38-cp38-linux_x86_64.whl
wget -q --show-progress https://data.pyg.org/whl/torch-1.9.0%2Bcu111/torch_scatter-2.0.9-cp38-cp38-linux_x86_64.whl
wget -q --show-progress https://data.pyg.org/whl/torch-1.9.0%2Bcu111/torch_cluster-1.5.9-cp38-cp38-linux_x86_64.whl
wget -q --show-progress https://data.pyg.org/whl/torch-1.9.0%2Bcu111/torch_spline_conv-1.2.1-cp38-cp38-linux_x86_64.whl
printf '\n#### Installing torch-geometric auxiliary libraries...\n'
pip install torch_sparse*.whl
pip install torch_scatter*.whl
pip install torch_cluster*.whl
pip install torch_spline_conv*.whl
rm torch_sparse*.whl
rm torch_scatter*.whl
rm torch_cluster*.whl
rm torch_spline_conv*.whl
