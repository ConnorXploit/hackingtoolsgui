sudo apt update
conda env create -f=environment.yml
conda activate ht
sudo apt-get install python-dev -y
sudo apt-get install libjpeg-dev -y
sudo apt-get install libtiff-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl-dev tk-dev python-tk -y
conda install -c conda-forge dlib
pip install -r requirements.txt
echo "All is done :) Now type:"
echo "python manage.py runserver"
