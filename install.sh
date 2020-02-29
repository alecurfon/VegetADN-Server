cd $( dirname $0 )

printf '\n>> Installing the needed tools ...\n'
sudo apt -qq -y install python3.7 python3-venv postgresql postgresql-contrib perl

printf '\n>> Setting up the PostgreSQL service ...\n'
sudo service postgresql start
sudo service postgresql restart
printf '\n>> Setting up the system user "vegetadn" ...\n'
sudo useradd vegetadn
sudo yes vegetadn | passwd vegetadn
sudo -u postgres createuser --superuser vegetadn
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
  sudo chmod +x ./app/models/load_ncbi_taxonomy.pl
  ./app/models/load_ncbi_taxonomy.pl --dbname vegetadn --driver Pg --dbuser vegetadn --download true
fi

sudo -u vegetadn psql vegetadn < ./app/models/search_scheme.sql

printf '\n>> Setting up the Python virtual environment ...\n'
python3.7 -q -m venv ./.venv
source ./.venv/bin/activate
pip install -q -r ./requirements.txt
python ./config.py

printf '\n>> DONE\n'
