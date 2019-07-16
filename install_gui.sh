if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi
sudo apt update -y
conda env create -f=environment.yml
conda activate ht
sudo apt-get install python-dev
sudo apt-get install libjpeg-dev
sudo apt-get install libtiff-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl-dev tk-dev python-tk
pip install -r requirements.txt
clear
echo "All is done :) Now type:"
echo "python manage.py runserver"
