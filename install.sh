cd $( dirname $0 )

printf '\n>> Installing the needed tools ...\n'
sudo apt -qq -y install python3.7 python3-venv postgresql postgresql-contrib perl >/dev/null 2>&1
printf '\n>> Setting up the Python virtual environment ...\n'
python3.7 -q -m venv ./.venv
source ./.venv/bin/activate
pip install -q -r ./requirements.txt

printf '\n>> Setting up the PostgreSQL service ...\n'
sudo service postgresql start >/dev/null 2>&1
sudo service postgresql restart >/dev/null 2>&1
sudo useradd vegetadn
sudo -u postgres createuser -g postgres -w -D -A vegetadn
sudo -u postgres createuser -g vegetadn -w -D -A "$(whoami)"
sudo -u postgres createdb -O vegetadn vegetadn
sudo /etc/init.d/postgresql reload >/dev/null 2>&1

printf '\n>> Setting up the PostgreSQL scheme ...\n'
sudo -u vegetadn psql vegetadn < ./app/models/biosql_scheme.sql >/dev/null 2>&1
chmod +x ./app/models/load_ncbi_taxonomy.pl
printf '\n>> Would you like to load the taxonomy of the NCBI? This could take a while. [y/N]: '
read response
if [ "$response" = "y" ]
then
  perl -MCPAN -e 'install DBI'
  perl -MCPAN -e 'install DBD::Pg'
  ./app/models/load_ncbi_taxonomy.pl --dbname vegetadn --driver Pg --dbuser vegetadn --download true
fi
sudo -u vegetadn psql vegetadn < ./app/models/search_scheme.sql >/dev/null 2>&1
python ./config.py

printf '\n>> DONE\n'
