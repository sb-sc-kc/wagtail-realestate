from django.contrib.auth import get_user_model

def run(*args):
    username = args[0]
    email = args[1]
    password = args[2]
    print(args)
    mystr = "from django.contrib.auth import get_user_model;\
    CustomUser = get_user_model();\
    CustomUser.objects.create_superuser(\
    '{username:s}', '{email:s}', '{password:s}')".format(username=username,
                                                email=email,
                                                password=password)
    print(mystr)
    CustomUser = get_user_model()
    CustomUser.objects.create_superuser(username, email, password)
    
    # c.run('echo "{:s}" | {manage:s} shell'.format(mystr, manage=MANAGE))
