#!/bin/bash

cd $( dirname $0 )
printf 'Enter the password for the database. This will be internal.\n'
while true
do
  printf 'Password: ';read -s password;echo;
  printf 'Repeat the same password: ';read -s match_pass;echo;
  [ "$password" == "$match_pass" ] && break
  printf '\nThe password does not match. Try again.\n';
done
echo "$password">./password;chmod 600 ./password;

printf '\n>> Installing the needed tools ...\n'
sudo apt -qq -y install python3.7 python3-venv postgresql-11 postgresql-contrib perl

printf '\n>> Setting up the PostgreSQL service ...\n'
sudo service postgresql start
sudo service postgresql restart

printf '\n>> Creating the user "vegetadn" ...\n'
sudo useradd vegetadn
yes "$password" | sudo passwd vegetadn
sudo -u postgres createuser --superuser vegetadn
echo "ALTER USER vegetadn WITH PASSWORD '$password' ;" | sudo -u postgres psql
# sudo /etc/init.d/postgresql reload

printf '\n>> Loading the database schema ...\n'
sudo -u vegetadn createdb vegetadn
sudo -u vegetadn psql vegetadn < ./app/models/biosql_scheme.sql
sudo -u vegetadn psql vegetadn < ./app/models/search_scheme.sql

printf '\n>> Would you like to load the taxonomy of the NCBI? This could take a while. [y/N]: '
read response
if [ "$response" = "y" ]
then
  yes '' | perl -MCPAN -e 'install DBI'
  yes '' | perl -MCPAN -e 'install DBD::Pg'
  sudo chmod +x ./app/models/load_ncbi_taxonomy.pl
  yes '' | ./app/models/load_ncbi_taxonomy.pl --dbname vegetadn --driver Pg --dbuser vegetadn --download true
fi

printf '\n>> Setting up the Python virtual environment ...\n'
python3.7 -q -m venv ./.venv
source ./.venv/bin/activate
pip install -q -r ./requirements.txt
python ./config.py

printf '\n>> DONE\n'
