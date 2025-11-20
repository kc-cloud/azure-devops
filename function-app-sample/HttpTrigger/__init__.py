import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Sample HTTP trigger Azure Function.
    Accepts GET and POST requests with an optional 'name' parameter.
    """
    logging.info('Python HTTP trigger function processed a request.')

    # Try to get 'name' from query parameters
    name = req.params.get('name')

    # If not in query params, try to get from request body
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    # Return response based on whether name was provided
    if name:
        return func.HttpResponse(
            json.dumps({
                "message": f"Hello, {name}! This HTTP triggered function executed successfully.",
                "status": "success"
            }),
            mimetype="application/json",
            status_code=200
        )
    else:
        return func.HttpResponse(
            json.dumps({
                "message": "Please pass a name on the query string or in the request body",
                "status": "error"
            }),
            mimetype="application/json",
            status_code=400
        )
