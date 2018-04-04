# PreHab Backend
[![Coverage Status](https://coveralls.io/repos/github/cubicon-feup/prehab-backend/badge.svg?branch=master)](https://coveralls.io/github/cubicon-feup/prehab-backend?branch=master)
[![Build Status](https://travis-ci.org/cubicon-feup/prehab-backend.svg?branch=master)](https://travis-ci.org/cubicon-feup/prehab-backend)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/be081261e0084083ad03f6d1ef13e6fd)](https://www.codacy.com/app/Cubicon/prehab-backend?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cubicon-feup/prehab-backend&amp;utm_campaign=Badge_Grade)

Now with CI on Travis and CD on Jenkins

### Migrate Database
`python manage.py makemigrations prehab_app`

`python manage.py migrate prehab_app`

### Sync Database with information (Only if needed)
`python manage.py loaddata prehab/fixtures/*`

### Run Unit Tests
`coverage run manage.py test prehab_app`

### Get Coverage Report in HTML
`coverage html`
