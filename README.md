# SEVIR-Assignment-5
DAMG 7245 - Big Data Systems &amp; IA Assignment 5 

Open Codelabs document [Here](https://codelabs-preview.appspot.com/?file_id=1zbc6fNJV5Msqiwyye3LPGtQclWHoE3v9ggmCOBst-d8#0):rocket:

### Live Demo Screen recording 🎥

[![Weather Nowcasting System using SEVIR NOAA dataset](https://res.cloudinary.com/marcomontalbano/image/upload/v1649982532/video_to_markdown/images/youtube--LDiy4YRJmp8-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=LDiy4YRJmp8 "Weather Nowcasting System using SEVIR NOAA dataset")

## Deliverables

1.  Limiting API Invocations from User
2.  Build and deploy NER and Summarization APIs
3.  Build a LIVE admin dashboard

## Tutorial Tryout and BERT API Repos

[Serverless-Question-Answering-API](https://github.com/kshitijzutshi/Serverless-Question-Answering-API)

[BERT-Summary-API](https://github.com/kshitijzutshi/BERT-Summary-API)

[BERT-NER-API](https://github.com/kshitijzutshi/BERT-NER-API)

## Requirements

* Python 3.X
* AWS Lambda, API Gateway, Elastic Container Registry
* Serverless framework
* fastapi==0.75.0, geopy, h5py==3.6.0, imageio, matplotlib, numpy, opencv_python==4.5.5.64, pandas, plotly, requests, starlette==0.17.1, tensorflow
* uvicorn
* gunicorn
* email-validator, PyJWT, python-decouple
* Pytorch, Transformers

## Project Setup 

### Create a custom docker image

Before we can create our docker we need to create a requirements.txt file with all the dependencies we want to install in our docker.

We are going to use a lighter Pytorch Version and the transformers library.

```
https://download.pytorch.org/whl/cpu/torch-1.5.0%2Bcpu-cp38-cp38-linux_x86_64.whl
transformers==3.4.0
```

To containerize our Lambda Function, we create a dockerfile in the same directory and copy the following content.
```
FROM public.ecr.aws/lambda/python:3.8

# Copy function code and models into our /var/task
COPY ./* ${LAMBDA_TASK_ROOT}/

# install our dependencies
RUN python3 -m pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "handler.handler" ]

```

Additionally we can add a .dockerignore file to exclude files from your container image.

```
README.md
*.pyc
*.pyo
*.pyd
__pycache__
.pytest_cache
serverless.yaml
get_model.py
```

### To build our custom docker image we run.

```
docker build -t bert-lambda .
```

### Test our function locally

AWS also released the Lambda Runtime Interface Emulator that enables us to perform local testing of the container image and check that it will run when deployed to Lambda.

We can start our docker by running.

```
docker run -p 8080:8080 bert-lambda
```

Afterwards, in a separate terminal, we can then locally invoke the function using curl or a REST-Client. Following example for Bert Q&A API

```
curl --request POST \
  --url http://localhost:8080/2015-03-31/functions/function/invocations \
  --header 'Content-Type: application/json' \
  --data '{"body":"{\"context\":\"We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models (Peters et al., 2018a; Radford et al., 2018), BERT is designed to pretrain deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be finetuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial taskspecific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).\",\n\"question\":\"What is the GLUE score for Bert?\"\n}"}'

# {"statusCode": 200, "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": true}, "body": "{\"answer\": \"80 . 5 %\"}"}%

```

### Deploy a custom docker image to ECR

Since we now have a local docker image we can deploy this to ECR. Therefore we need to create an ECR repository with the name bert-lambda.

```
aws ecr create-repository --repository-name bert-lambda > /dev/null
```

To be able to push our images we need to login to ECR. We are using the aws CLI v2.x. Therefore we need to define some environment variables to make deploying easier.

```
aws_region=eu-east-1
aws_account_id=<AWS ID>

aws ecr get-login-password \
    --region $aws_region \
| docker login \
    --username AWS \
    --password-stdin $aws_account_id.dkr.ecr.$aws_region.amazonaws.com
```

Next we need to tag / rename our previously created image to an ECR format. The format for this is {AccountID}.dkr.ecr.{region}.amazonaws.com/{repository-name}

### Tag docker image

```
docker tag bert-lambda $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/bert-lambda

```

To check if it worked we can run docker images and should see an image with our tag as name

Finally, we push the image to ECR Registry.

### Push Image to ECR

```
 docker push $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/bert-lambda
```

## Project folder structure

```bash
│   .dockerignore
│   .env
│   .gitignore
│   airflow_new.py
│   LICENSE
│   main.py
│   new.csv
│   package-lock.json
│   project_structure
│   README.md
│   requirements.txt
│   streamlit_new.py
│
└───app
    │   model.py
    │
    └───auth
            jwt_bearer.py
            jwt_handler.py
```

### Team Contributions

| Team Member     | NUID      | Work Done                                 | Percentage(%) contribution |
|-----------------|-----------|-------------------------------------------|----------------------------|
| Kshitij Zutshi  | 001021288 | BERT APIs                                 | 33.33333%                  |
| Priyanka Shinde | 001524484 | Streamlit, User Auth, GCP dashboard       | 33.33333%                  |
| Dwithika Shetty | 002114630 | Airflow deployment, Streamlit integration | 33.33333%                  |
|                 |           |                                           |                            |



**“WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK”**
