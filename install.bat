@echo off
cls

echo [*] Upgrading pip
python -m pip install -U pip

echo [*] Installing Django
python -m pip install Django==1.10.2

echo [*] Installing PyBBM Forum
python -m pip install pybbm

echo [*] Installing Pillow
python -m pip install Pillow

echo [*] Installing rest of the necessary files
python -m pip install Markdown
python -m pip install BBcode
python -m pip install pytz
python -m pip install postmarkup
python -m pip install django-annoying
python -m pip install django-pure-pagination
python -m pip install sorl-thumbnail
python -m pip install unidecode
python -m pip install django-simple-captcha
python -m pip install pinax-theme-bootstrap<6.0
python -m pip install django-bootstrap-form
python -m pip install django-user-accounts

echo [+] Done
