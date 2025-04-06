# Receipt Predictor

Flask take home assignment that predicts receipt counts for each month of 2022

## Run

1. Clone the repository
2. Build the docker image with:
```
docker build -t receipt-predictor .
```
3. Run the docker container
```
docker run -p 5001:5000 receipt-predictor
```
I used port 5001 because 5000 wasn't working for me

4. Go to this link on google

http://localhost:5001

the last number should be the port number you ran the docker container with
