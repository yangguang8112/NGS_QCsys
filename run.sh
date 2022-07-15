# superset
#export FLASK_APP=superset
#superset run -p 8088 --with-threads --reload --debugger

# GC_pct = '38.39(N)'

# flaskr
export FLASK_APP=flaskr
export FLASK_ENV=development
# flask init-db
flask run -h 0.0.0.0 -p 6868
