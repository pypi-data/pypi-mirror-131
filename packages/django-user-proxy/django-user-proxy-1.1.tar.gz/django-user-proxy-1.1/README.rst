==================
DjangoAuthProxyApp
==================

AuthProxyApp is a Django app containing a single User Proxy model, which is shared between multiple
Django instances.

The purpose of this Proxy model is to access a single shared "Users" database between Django
applications, with no explicit foreign relations.

It currently operates with a modified User implementation featuring a UUID as a PK, you can easily
implement this by creating your own AbstractUser implementation, and storing all users and permissions
in a single "Users" database.

Quick start
-----------

1. Add "auth_proxy" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'auth_proxy',
    ]

2. Run ``python manage.py migrate`` to create the auth_proxy model.

3. If you wish to use the included Middlewares, include them::

    MIDDLEWARE_CLASSES = (
        ...
        'auth_proxy.middleware.GenerateUserProxy',
        'auth_proxy.middleware.AddUserProxyToRequest'
    )

GenerateUserProxy will create the UserProxy on user login, and AddUserProxyToRequest will add the
UserProxy to the request, where it can be obtained like this: request.user_proxy.

TODO
----

- REST endpoints to manage UserProxy instances
- Erase UserProxy instances when Users are deleted

BUILDING
--------

Run ``python -m build``