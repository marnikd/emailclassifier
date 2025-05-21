from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
import joblib
import logging
from typing import Optional
from starlette.requests import Request


# logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# initialise API
app = FastAPI(title="Email Classifier API")

# load model
try:
    model = joblib.load("pipple_model.pkl")
    logging.info("Model succesvol geladen.")
except Exception as e:
    logging.error(f"Fout bij het laden van het model: {e}")
    raise

# class mapping
CLASS_MAP = {
    1: "World",
    2: "Sports",
    3: "Business",
    4: "Sci-Tech"
}

# classes request / response
class EmailRequestData(BaseModel):
    EmailID: str = Field(..., min_length=1, max_length=100)
    TitleDescription: str = Field(..., min_length=1, max_length=1000)

class EmailRequest(BaseModel):
    EmailRequestData: EmailRequestData

class EmailResponseData(BaseModel):
    EmailId: str
    ReturnCode: int
    EmailClass: int
    EmailClassDescrip: str
    ErrorMessage: Optional[str] = None
    class Config:
        exclude_none = True 

class EmailResponse(BaseModel):
    EmailResponseData: EmailResponseData



@app.post("/classify", response_model=EmailResponse, response_model_exclude_none=True)
def classify_email(request: EmailRequest):
    try:
        email_id = request.EmailRequestData.EmailID
        content = request.EmailRequestData.TitleDescription

        logging.info(f"Ontvangen verzoek voor EmailID: {email_id}")

        # predict
        prediction = model.predict([content])[0]
        label = CLASS_MAP.get(prediction, "Unknown")

        return EmailResponse(
            EmailResponseData=EmailResponseData(
                EmailId=email_id[:10],
                ReturnCode=0,
                EmailClass=prediction,
                EmailClassDescrip=label
            )
        )

    except Exception as e:
        logging.error(f"Fout bij classificatie: {e}")
        # raise HTTPException(status_code=500)
        data = EmailResponseData(
            EmailId=email_id[:10],
            ReturnCode=1,
            EmailClass=0,
            EmailClassDescrip="",
            ErrorMessage= f'{e}'
        )

        return JSONResponse(
            status_code=500,
            content={"EmailResponseData": data.model_dump()}
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validatiefout: {exc}")

    # try to get emailID for tracing
    try:
        body = await request.json()
        email_id = body.get("EmailRequestData", {}).get("EmailID", "Unknown")
        email_id = email_id[:10]
    except Exception as e:
        email_id = "Unknown"

    data = EmailResponseData(
        EmailId=email_id,
        ReturnCode= 1,
        EmailClass= 0,
        EmailClassDescrip="",
        ErrorMessage=f"Validatiefout: {exc}"
    )
    return JSONResponse(
        status_code=422,
        content={"EmailResponseData": data.model_dump()}
    )


