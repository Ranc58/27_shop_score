# Shop Score Page
Script for create site with call-center today orders handling stats.\
Site displayed:
1) Conditions with waiting time of unprocessed requests.
2) Counts of unhandled requests.
3) Counts of handled requests.
Stats have 3 conditions:

**waiting time more than 30 minutes**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**waitng time more than 7 minutes**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
**waiting time less then 7 minutes**     
![Statuses](https://pp.userapi.com/c639522/v639522446/32c4d/iP3b6CIp6BY.jpg?raw=true "Statuses")
Information refresh every 10 minutes.\
Site is closed from indexing by search engines.\
Site maked for displays from 320px to FullHD.\
Working example: [call-center-score.herokuapp.com](https://call-center-score.herokuapp.com/)
# How to install
1. Recomended use venv or virtualenv for better isolation.\
Venv setup example: \
`python3 -m venv myenv`\
`source myenv/bin/activate`
2. Install requirements:\
`pip3 install -r requirements.txt` (alternatively try add `sudo` before command)

# How to launch
   - Run server `gunicorn server:app`
   - Open on browser `http://127.0.0.1:8000`

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
