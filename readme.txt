Фласк
set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
export FLASK_APP=webapp && export FLASK_ENV=development && flask run
set FLASK_APP=webapp && flask shell
pip freeze > requirements.txt


Миграции
set FLASK_APP=webapp && FLASK db init
move webdb.db webdb.db.old
set FLASK_APP && flask db migrate -m "add new table commet comments"
flask db upgrade
move webdb.db.old webdb.db
flask db stamp de08b25fb416
