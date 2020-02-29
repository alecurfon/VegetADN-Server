cd $( dirname $0 )

printf '\n>> Installing the needed tools ...\n'
sudo apt -qq -y install python3.7 python3-venv postgresql postgresql-contrib perl
printf '\n>> Setting up the Python virtual environment ...\n'
python3.7 -q -m venv ./.venv
source ./.venv/bin/activate
pip install -q -r ./requirements.txt

printf '\n>> Setting up the PostgreSQL service ...\n'
sudo service postgresql start
sudo service postgresql restart
sudo useradd vegetadn
sudo -u postgres createuser -g postgres -w -D -A "$(whoami)"
sudo -u postgres createuser -g "$(whoami)" -w -D -A vegetadn
createdb vegetadn
sudo /etc/init.d/postgresql reload

printf '\n>> Setting up the PostgreSQL scheme ...\n'
psql vegetadn < ./app/models/biosql_scheme.sql
chmod +x ./app/models/load_ncbi_taxonomy.pl
printf '\n>> Would you like to load the taxonomy of the NCBI? This could take a while. [y/N]: '
read response
if [ "$response" = "y" ]
then
  perl -MCPAN -e 'install DBI'
  perl -MCPAN -e 'install DBD::Pg'
  ./app/models/load_ncbi_taxonomy.pl --dbname vegetadn --driver Pg --dbuser vegetadn --download true
fi
psql vegetadn < ./app/models/search_scheme.sql
python ./config.py

printf '\n>> DONE\n'
