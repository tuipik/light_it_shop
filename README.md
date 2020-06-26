# light_it_shop
***A simple system for managing orders.***

---
**Usage**

- Install docker and git on your machine

- Clone this repository via http `https://github.com/tuipik/light_it_shop.git`
or via ssh `git@github.com:tuipik/light_it_shop.git`

- In terminal open directory with source code of repo

- Build or pull docker image. In terminal: `make build` or `make pull`

- Start local server by `make run` command in Terminal

- Fill up database with testing data, superuser and users `make db`

    Logining as
     - superuser use login: `test@testemail.com`  password: `test_pass`
     - accounter use login: `accounter@a.com`  password: `test_pass`
     - cashier use login: `cashier@a.com`  password: `test_pass`
     - assistant use login: `assistant@a.com`  password: `test_pass`
 
- To start tests use command `make test`
---
**Endpoints:**


products list: `http://0.0.0.0:8000/api/v1/products/`

product detail: `http://0.0.0.0:8000/api/v1/products/1/`

orders list: `http://0.0.0.0:8000/api/v1/orders/`

order detail: `http://0.0.0.0:8000/api/v1/orders/1/`

order filtered list: `http://0.0.0.0:8000/api/v1/orders/?creation_date_after=YYYY-MM-DD&creation_date_before=YYYY-MM-DD`
- the command `make db` creates 10 orders. Each of them has different creation date
in period of last 10 days. To filter list of orders use last 10 dates instead of YYYY-MM-DD
    
bills list: `http://0.0.0.0:8000/api/v1/bills/`

bill detail: `http://0.0.0.0:8000/api/v1/bills/1/`

---
**Postman Collection:**

`https://www.postman.com/collections/f7bab853c7f89710b3e0`