cd $( dirname $0 )
sudo chmod +x ./app/models/load_ncbi_taxonomy.pl

printf '\n>> Installing the needed tools ...\n'
sudo apt -qq -y install python3.7 python3-venv postgresql postgresql-contrib perl

printf '\n>> Setting up the PostgreSQL service ...\n'
sudo service postgresql start
sudo service postgresql restart
printf '\n>> Setting up the system user "vegetadn" ...\n'
sudo useradd vegetadn
sudo passwd vegetadn
sudo -u postgres createuser --superuser vegetadn

printf '\n>> Log in as "vegetadn" ...\n'
# sudo /etc/init.d/postgresql reload

printf '\n>> Setting up the PostgreSQL scheme ...\n'
sudo -u vegetadn createdb vegetadn
sudo -u vegetadn psql vegetadn < ./app/models/biosql_scheme.sql

printf '\n>> Would you like to load the taxonomy of the NCBI? This could take a while. [y/N]: '
read response
if [ "$response" = "y" ]
then
  perl -MCPAN -e 'install DBI'
  perl -MCPAN -e 'install DBD::Pg'
  ./app/models/load_ncbi_taxonomy.pl --dbname vegetadn --driver Pg --dbuser vegetadn --download true
fi

sudo -u vegetadn psql vegetadn < ./app/models/search_scheme.sql

printf '\n>> Setting up the Python virtual environment ...\n'
sudo -u vegetadn python3.7 -q -m venv ./.venv
sudo -u vegetadn source ./.venv/bin/activate
sudo -u vegetadn pip install -q -r ./requirements.txt
sudo -u vegetadn python ./config.py

printf '\n>> DONE\n'
