-- Install myapp--
>cd folder
>d:\python38\python.exe -m venv py38_env
>.\py38_env\Script\activate
(env) >pip install -e .
(env) >python -m pip install -r requirements.txt

--Version---
chromedriver.exe utk chrome Ver 91
geckodriver Ver 29
python Ver 3.8
selenium Ver 3 up

-- Install server IIS --
# https://pypi.org/project/wfastcgi/
# https://docs.microsoft.com/en-us/visualstudio/python/configure-web-apps-for-iis-windows?view=vs-2019
\venv\scrip>wfastcgi-enable  (dgn administrator)

-- Copy Firefox profile (bila menggunakan Firefox) -- (Sy gunakan Chrome)
setting headless=False di MainScript agar browser jalan
localhost:1993/{module}/startdriver  # (lihat di routes.py di module)
url: about:support
Buka folder Profile Folder (cth: C:\Users\Syahpril\AppData\Local\Temp\rust_mozprofile8888)
# ingat yg tanpa add-ons
copy folder (rust_mozprofile8888) ke path ini, dan rename dgn nama firefox_profile

-- MANUAL run server --
--- (venv) >set FLASK_ENV=development  (optional)
=============================
(env) >set FLASK_APP=myapp
(env) >flask run --host=localhost --port=1993
# result: * Running on http://localhost:1993/
-atau-
(env) >flask run
# result: * Running on http://127.0.0.1:5000/

-- Petunjuk Debug dan Development
ada di file PetunjukDebug-Dev.txt
