echo >> Installing the needed tools ...
sudo apt install virtualenv pip postgresql postgresql-contrib perl
# sudo apt-get install python-psycopg2
echo >> Setting up the Python virtual environment ...
virtualenv --python=python3.7 $0/.vegetadn-virtualenv
source $0/.vegetadn-virtualenv/bin/activate
pip install -r $0/requirements.txt

echo >> Setting up the PostgreSQL service ...
# sudo /etc/init.d/postgresql status
sudo service postgresql start
sudo service postgresql restart
sudo -u postgres createuser -D -A -P vegetadn
sudo -u postgres createdb -O vegetadn vegetadn
sudo /etc/init.d/postgresql reload
psql vegetadn < $0/app/models/biosql_scheme.sql
python $0/app/models/user_account.py

# loading ncbi taxonomy
chmod +x ./db/load_ncbi_taxonomy.pl
echo >> Would you like to load the taxonomy of the NCBI? This could take a while. [y/N]:
read response
if [ "$response" = "y" ]
then
  perl -MCPAN -e 'install DBI'
  perl -MCPAN -e 'install DBD::Pg'
  ./db/load_ncbi_taxonomy.pl --dbname vegetadn --driver Pg --dbuser vegetadn --download true
fi
psql vegetadn < $0/app/models/search_scheme.sql
