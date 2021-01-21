kioskBackend

Run Django Server
`python manage.py runserver`

install restframework by running: 
`pip install djangorestframework`

install django channels by running:
`pip install -U channels`

To create a super admin for models:
`python manage.py createsuperuser`

Everytime you make change to models(database table),run following commands:
`python manage.py makemigrations`
`python manage.py migrate`

Everytime you pull, run this:
`python manage.py migrate`

Install requests: 
`pip install requests`

Please run following commands to install cors request middleware:
`pip install django-cors-headers`