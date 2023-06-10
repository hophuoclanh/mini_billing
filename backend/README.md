# Mini Billing Application
- SPRING2023 - CS311 Final Project

# Manual

## Installation
### Instal Dependencies and Library
```
pip install -r requirements.txt
```

## Create mini billing database 
- connect to mysql server
```
mysql -u <user-name> -p 
```
- run the script create_mini_billing_db.sql to create mini_billing database in your mysql server

```
source create_mini_billling_db.sql
```

## .env file
- base on the .env.template file, create your own .env file

### Create Jwt Secret

``` bash
openssl rand -hex 32
```

## Create Superuser

- First, create a super user
```
python .\tools\create_super_user.py --user_name <your-user-name> --email <your-email> --phone <your-phone> --address <your-address> --password <your-password>
```

- Then, paste the user_id obtaining after running the above command in the below script (the role can be either casher, manager or admin)

```
python .\tools\create_super_user_position.py --user_id <user_id> --role <role>

```
#### sample in window
``` bash
python .\tools\create_super_user.py --user_name hothienlac --email hothienlac@gmail.com --phone 0987654321 --address qwe.rty --password 123
```
```
python .\tools\create_super_user_position.py --user_id <user_id> --role <role>
```

#### linux base

``` bash
python ./tools/create_super_user.py --user_name vpa141203 --email vpa141203@gmail.com --phone 0123456789 --address ttu-plaza --password 123456
```

```
python ./tools/create_super_user_position.py --user_id <user_id> --role <role>
```

## run program
```
python main.py
```
