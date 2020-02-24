cd $( dirname $0 )

echo >> Installing the needed tools ...
sudo apt -y install virtualenv postgresql postgresql-contrib perl
# sudo apt-get install python-psycopg2
echo >> Setting up the Python virtual environment ...
virtualenv --python=python3.7 ../.vegetadn-virtualenv
source ../.vegetadn-virtualenv/bin/activate
pip install -r ./requirements.txt

echo >> Setting up the PostgreSQL service ...
# sudo /etc/init.d/postgresql status
sudo service postgresql start
sudo service postgresql restart
sudo -u postgres createuser -D -A -P vegetadn
sudo -u postgres createdb -O vegetadn vegetadn
sudo /etc/init.d/postgresql reload
psql vegetadn < ./app/models/biosql_scheme.sql
python ./app/models/user_account.py

# loading ncbi taxonomy
chmod +x ./app/models/load_ncbi_taxonomy.pl
echo >> Would you like to load the taxonomy of the NCBI? This could take a while. [y/N]:
read response
if [ "$response" = "y" ]
then
  perl -MCPAN -e 'install DBI'
  perl -MCPAN -e 'install DBD::Pg'
  ./app/models/load_ncbi_taxonomy.pl --dbname vegetadn --driver Pg --dbuser vegetadn --download true
fi
psql vegetadn < ./app/models/search_scheme.sql

echo >> DONE
