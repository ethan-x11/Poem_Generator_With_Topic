import requests
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from logtail import LogtailHandler
from fastapi.responses import FileResponse, HTMLResponse
from reportlab.pdfgen import canvas
import json
import os
import sys

# Get the API key from .env file
api_key = os.getenv("API_KEY")

logtail_handler = LogtailHandler(source_token="p2EZUv5XBwvq6bhnJauaCRFa")

logger.remove(0)

logger.add(
    sys.stderr,
    format="{time:MMMM D, YYYY > HH:mm:ss!UTC} | {level} | {message} | {extra}",
    level="TRACE",
    backtrace=False,
    diagnose=False,
)

logger.add(
    logtail_handler,
    format="{message}",
    level="INFO",
    backtrace=False,
    diagnose=False,
)

logger.add("log.json")

logger.info("App started")

def get_data(query):
    url = f"https://llamastudio.dev/api/clqcch9ka0001jv08u8wzzx94"
    data = {"input": query}
    response = requests.post(url, json=data)
    return response.json()


## make api using fastapi
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to the PoemGeneratorWithTopic API! Use get_poem route to generate a poem and get_poem_pdf route to generate a PDF of the poem(Pass query as a parameter)."
    }


@app.get("/get_poem/")
def get_poem(query: str):
    output = get_data(query)
    # Log the query and output in log.json
    # log_data = {"query": query, "output": output}
    # logger.info(json.dumps(log_data))
    # Convert the output data to proper HTML format
    try:
        html_output = "<div>"
        lines = output.split("\n")
        for line in lines:
            html_output += f"<p>{line}</p>"
        html_output += "</div>"
        log_data = {"query": query, "output": output}
        logger.info(json.dumps(log_data))
    except:
        html_output = "<div><p>Sorry, there was an error in generating the poem.</p></div>"
        log_data = {"query": query, "output": output}
        logger.error(json.dumps(log_data))

    # Return the HTML as a response
    return HTMLResponse(content=html_output, media_type="text/html")
    # Return the PDF file as a response
    return output


# make get request that will take query parameter and return the output
@app.get("/get_poem_pdf/")
def get_poem(query: str):
    output = get_data(query)
    # Log the query and output in log.json
    # log_data = {"query": query, "output": output}
    # logger.info(json.dumps(log_data))

    try:
        # Create a PDF file
        pdf_file = "./output.pdf"
        c = canvas.Canvas(pdf_file)
        c.setFont("Helvetica", 12)  # Set the font and size
        lines = output.split("\n")  # Split the output into lines
        y = 750  # Initial y-coordinate for drawing text
        for line in lines:
            c.drawString(100, y, line)  # Write each line to the PDF
            y -= 20  # Decrease the y-coordinate for the next line
        c.save()
        log_data = {"query": query, "output": output}
        logger.info(json.dumps(log_data))
    except:
        html_output = "<div><p>Sorry, there was an error in generating the poem.</p></div>"
        log_data = {"query": query, "output": output}
        logger.error(json.dumps(log_data))

    # Return the PDF file as a response
    return FileResponse(pdf_file, filename=f"{query}.pdf", media_type="application/pdf")


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0")
    uvicorn.run(app, port = 8000)

    # query = input('Enter a word or two to make poem with: ')
    # print("<Wait for Output>")
    # #print two line break
    # print("\n")
    # print(get_data(query))
