build:
	@docker build -t tuipik/light_it_shop:tagname .
pull:
	@docker pull tuipik/light_it_shop:tagname
run:
	@docker-compose up
db:
	@docker-compose run app sh -c "python manage.py fill_up_db"
test:
	@docker-compose run app sh -c "python manage.py test -v 2 && flake8"