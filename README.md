# Receipt Predictor

Flask take home assignment that predicts receipt counts for each month of 2022

# Project layout

model.ipynb is the jupyter notebook for developing the model (model.ipynb)\
app.py is the flask app for the webserver\
templates/index.html is the website layout\

## Run

1. Clone the repository with
```
git clone https://github.com/pattybruh/fetch-receipt-th.git
```
2. Build the docker image with:
```
docker build -t receipt-predictor .
```
3. Run the docker container
```
docker run -p 5001:5000 receipt-predictor
```
I used port 5001 because 5000 wasn't working for me but make sure the number after is 5000

4. Go to this link on google

http://localhost:5001

the number at the end should be the port number you ran the image with
