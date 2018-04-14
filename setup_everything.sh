sudo rm prehab/db.sqlite3
sudo rm prehab_app/migrations/* -rf
python manage.py makemigrations prehab_app
python manage.py migrate prehab_app
python manage.py loaddata prehab/fixtures/*