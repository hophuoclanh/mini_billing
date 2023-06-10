# mini_billing
- project_cs311 in SPRING2023
- In order to run this program, you need to first create mini_billing database in mysql server


# Manual

## Installation
```
pip install -r requirements.txt
```

## Create database
...

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
python .\tools\create_super_user_position.py --user_id <user_id> --role <role>
```

#### linux base

``` bash
python ./tools/create_super_user.py --user_name vpa141203 --email vpa141203@gmail.com --phone 0123456789 --address ttu-plaza --password 123456
python ./tools/create_super_user_position.py --user_id <user_id> --role <role>
```

## run program
```
python main.py
```
