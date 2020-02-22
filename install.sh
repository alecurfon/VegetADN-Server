sudo apt install virtualenv pip postgresql postgresql-contrib perl
# sudo apt-get install python-psycopg2
virtualenv --python=python3.7 $0/.vegetadn-virtualenv
source $0/.vegetadn-virtualenv/bin/activate
pip install -r $0/requirements.txt

# sudo /etc/init.d/postgresql status
sudo service postgresql start
sudo service postgresql restart
sudo -u postgres createuser -D -A -P vegetadn 
sudo -u postgres createdb -O vegetadn vegetadn
sudo /etc/init.d/postgresql reload
psql biosqldb < $0/app/models/biosql_scheme.sql
psql biosqldb < $0/app/models/search_scheme.sql
python $0/install.py
# construir estructura de usuarios

# loading ncbi taxonomy
chmod +x ./db/load_ncbi_taxonomy.pl
perl -MCPAN -e 'install DBI'
perl -MCPAN -e 'install DBD::Pg'
./db/load_ncbi_taxonomy.pl --dbname vegetadn --driver Pg --dbuser vegetadn --download true
