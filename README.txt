########################
### koristeni paketi ###
########################

Za popis paketa koristenih u projektu pokrenuti:
python -m pip freeze > requirements-pip-freeze.txt

ili

navesti ih u requirements.in (vec su navedeni) pa pokrenuti pip-compile (za tu komandu treba paket: pip install pip-tools)

ne trebamo koristiti venv, pyinstaller sve sto koristimo upakira u exe
#python -m venv gdvenv
#.\gdvenv\Scripts\Activate.ps1
#pip install <paketi_iz_requirements.in>

pripremiti requirements.in file sa dependencijima:
pandas
xlrd
XlsxWriter
pyinstaller

i pokrenuti pip-compile da ti ostane popis dependenciya za ubuduce u requirements.txt

pip freeze izbaci malo vise paketa pa su i oni zabiljezeni (u requirements-pip-freeze.txt)


###############
### app.exe ###
###############

Za generirati Windows exe file instalirati:
pip install pyinstaller

navigirati se u root dir projekta i pokrenuti:
pyinstaller.exe --onefile --icon=img/logo.ico gui/app.py

app.exe ce se generirati u dist/ direktoriju
