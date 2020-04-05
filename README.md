## Reps API
 A serverless api that returns a short summary of campaign contributions to elected representatives in the House and Senate.

### Getting Started
**Test on AWS (already deployed)**
I deployed this to a dev environment in AWS.  You can interact with the API with this [Swagger UI](https://editor.swagger.io/?_ga=2.143766844.829039718.1585956943-1736463195.1585956943) here.

**Test Locally**
Assumes you have `npm`, `conda`, and `git` already installed
1. Install serverless framework: `npm install -g serverless`
2. Clone this repo.
3. Install serverless plugins: `npm install`
4. Build python environment (for local use only): `conda env create -f environment.yml`
5. Make a .env file in the project root containing `GOOGLE_API_KEY=[your api key]`
6. Run unit tests: `coverage run -m unittest discover -sv tests`
7. View coverage report (or html version): `coverage report` or `coverage html`
  - html coverage report will be in ./htmlcov
8. Run api tests on local server (an AWS Gateway emulator): `python api_test_local.py`
  - This will just make calls to local endpoints using the set of test params in `/mocks`
  - These are not all supposed to return 200.  Some will return 400 or 500.


**Test with Travis**
A Travis file is included that will "build" the serverless app and run unit tests.
1. Clone this repo and push a copy to your Github account.
2. Link your repo to your [TravisCI account](https://travis-ci.com/)
3. Enter a Google API Key in Travis by going to Options >> Settings  from the project page:
  - `GOOGLE_API_KEY: [key val]`
3. Trigger a build by pushing a commit or manually from within Travis.


**Deploy to AWS with Seed**
I deployed this project using a serverless CI/CD platform, called Seed.  You can
do the same, but it would involve creating a free Seed account and using (or creating)
a set of AWS IAM credentials (Access ID and Secret Key).  In the interest of time I created a
User with AdministratorAccess.

1. After completing the steps from **Test Locally** above...
2. Create a copy of the project repo in your Github account.
3. Create a [Seed account](https://seed.run/) and link to your Github (like with any CI/CD)
4. Click "Add an App" and follow the 3 steps to link the Github repo to Seed.
  - this includes selecting the repo, adding your AWS IAM credentials, and accepting all other defaults.
5. Enter your Google API Key and Insert a Post-Deploy process
  - from the project dashboard, goto Dev in Pipeline Panel >> Settings >> Env Vars:
  - `GOOGLE_API_KEY: [key val]`
  - in the same settings screen goto Enable Post-Deploy. Insert the following, one per line:
    - echo "Running API tests"
    - python api_test.py
7. Trigger a deployment by pushing a commit or manually from within Seed
  - Seed will run the unit tests, and then deploy to AWS
  - this will deploy the application to a dev environment
  - after deployment Seed will run the Post-Deployment API test we provided
