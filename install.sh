cd $( dirname $0 )

printf '\n>> Installing the needed tools ...\n'
sudo apt -q -y install python3.7 python3-venv postgresql postgresql-contrib perl
# >/dev/null 2>&1  &>/dev/null ? python-psycopg2
printf '\n>> Setting up the Python virtual environment ...\n'
python3.7 -q -m venv ./.vegetadn-virtualenv
source ./.vegetadn-virtualenv/bin/activate
pip install -q -r ./requirements.txt

printf '\n>> Setting up the PostgreSQL service ...\n'
# sudo /etc/init.d/postgresql status
sudo service postgresql start
sudo service postgresql restart
sudo useradd vegetadn
sudo -u postgres createuser -g postgres -w -D -A vegetadn
sudo -u postgres createuser -g vegetadn -w -D -A "$(whoami)"
sudo -u postgres createdb -O vegetadn vegetadn
sudo /etc/init.d/postgresql reload
sudo -u vegetadn psql vegetadn < ./app/models/biosql_scheme.sql

# loading ncbi taxonomy
chmod +x ./app/models/load_ncbi_taxonomy.pl
printf '\n>> Would you like to load the taxonomy of the NCBI? This could take a while. [y/N]: '
read response
if [ "$response" = "y" ]
then
  perl -MCPAN -e 'install DBI'
  perl -MCPAN -e 'install DBD::Pg'
  ./app/models/load_ncbi_taxonomy.pl --dbname vegetadn --driver Pg --dbuser vegetadn --download true
fi
sudo -u vegetadn psql vegetadn < ./app/models/search_scheme.sql
python ./app/__init__.py

printf '\n>> DONE\n'