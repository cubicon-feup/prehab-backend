# PreHab Backend
[![Coverage Status](https://coveralls.io/repos/github/cubicon-feup/prehab-backend/badge.svg?branch=master)](https://coveralls.io/github/cubicon-feup/prehab-backend?branch=master)
[![Build Status](https://travis-ci.org/cubicon-feup/prehab-backend.svg?branch=master)](https://travis-ci.org/cubicon-feup/prehab-backend)

Now with CI/CD on jenkins

### Migrate Database
`python manage.py makemigrations prehab_app`
`python manage.py migrate prehab_app`

### Sync Database with information (Only if needed)
`python manage.py loaddata prehab_app/fixtures/*`

### Run Unit Tests
`python manage.py test`