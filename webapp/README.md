Copy both of these files to /var/www/html/ on the Raspberry Pi to run on boot

sudo su
apt install apache2 -y
apt install php7.4 libapache2-mod-php7.4 -y
cd /opt
git clone https://github.com/DDeGonge/Shuffle-o-matic.git
mv Shuffle-o-matic/webapp/* /var/www/html
rm -rf  Shuffle-o-matic
chmod -R www-data. /var/www/html
ln -s /opt/Shuffle-o-matic/helpers/Card_Imgs /home/pi/pics

-- Install needed python modules
pip install pyserial opencv-python scipy picamera Pillow
apt install libatlas-base-dev libopencv-dev

--Enable the Raspberry Pi Camera Intrface
raspi-config
 3. Interface Options
 P1 Camera
 Yes


-- Run the ShuffleScript
python3 ShuffleScript.py