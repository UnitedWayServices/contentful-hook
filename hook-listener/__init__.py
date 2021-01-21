import logging
import azure.functions as func
import requests
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    getRequestHeaders = dict(req.headers)

    #check POST request is from Contentful
    if "x-contentful-webhook-name" in getRequestHeaders:
        
        #identifies specific build pipeline from devops
        body = {
            "definition": {
                "id": 7
            }
        }
        user_name = os.environ["USER"]
        user_token = os.environ["TOKEN"]
        url = "https://dev.azure.com/UnitedWayofCalgary/Annual%20Impact%20Report/_apis/build/builds?api-version=5.0"

        #initiate build via POST
        r = requests.post(url, auth=(user_name,user_token), json=body)
        if r.status_code == requests.codes.ok:
            return func.HttpResponse(
             "You have sucessfully received the Contentful webhook and queued the new build for deployment.",
             status_code=200
        )
        else:
            return func.HttpResponse(
             "Something went wrong. Please try again."
        )

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully, but only processes Contentful webhook requests.",
             status_code=200
        )