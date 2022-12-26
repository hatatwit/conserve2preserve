# conserve2preserve
A web app is a GoodGuide-like that acts as a guide to all things that are good for you and good for the environment. Users can scan barcodes or browse by name to find products in a variety of categories, including food, drinks, health and beauty aids, pet food, body care and more. Each item is rated on a scale of 0 to 100 based on its ingredients, environmental impact and company ethics.

## Installation

```bash
$ git clone https://github.com/hatatwit/conserve2preserve.git
$ cd conserve2preserve
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver

```

## Demo
https://user-images.githubusercontent.com/53331354/169591089-0d1046d2-15ea-4eaf-a9fe-c74361c8db8b.mp4

## Database Relationships
![alt text](https://github.com/hatatwit/conserve2preserve/blob/master/static/image/data-relationships.png?raw=true)

## Build with
Web technologies: HTML, CSS, Bootstrap, Python, Django 

APIs:
* UPC Lookup API - Search barcode and find product information.
* Logo API - Get any company’s branding data.
* Recycling API - Find nearby recycling spots by ZIP code

Database: SQlite

## License

[MIT](https://choosealicense.com/licenses/mit/)

