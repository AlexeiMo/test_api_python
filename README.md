**Run commands in terminal IDE**
1. Install python3
2. python3 -m venv env (create env)
3. cd env\Scripts (go to env activation folder)
4. activate.bat (activate env)
5. pip install -r requirements.txt (install dependencies from requirements.txt file)
6. cd test (go to test folder into the project)
7. pytest --alluredir=allure-results (run onliner tests)
8. allure generate allure-results --clean -o allure-report (generate allure report)
