sudo apt update
sudo apt install wget -y
sudo apt install tar -y
sudo apt install cmake -y

function package_exists() {
    return dpkg -l "$1" &> /dev/null
}

# Install cmake
# if ! package_exists dpkg -l "cmake" &> /dev/null ; then
#     wget http://www.cmake.org/files/v2.8/cmake-2.8.3.tar.gz
#     tar xzf cmake-2.8.3.tar.gz
#     cd cmake-2.8.3
#     ./configure --prefix=/opt/cmake
#     sudo make
#     sudo make install
#     cd ..
#     sudo rm -r cmake-2.8.3
#     rm cmake-2.8.3.tar.gz
# fi

pip install hackingtools -U