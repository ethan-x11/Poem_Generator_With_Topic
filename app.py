import requests
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
import json
import os

# Get the API key from .env file
api_key = os.getenv("API_KEY")

def get_data(query):
    url = f'https://llamastudio.dev/api/{api_key}'
    data = {'input':query}
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

@app.get("/get_poem/")
def get_poem(query: str):
    output = get_data(query)
    # Log the query and output in log.json
    log_data = {
        "query": query,
        "output": output
    }

    logging.basicConfig(filename='log.json', level=logging.INFO)
    logging.info(json.dumps(log_data))
    logging.info("\n")

    # Return the PDF file as a response
    return output

#make get request that will take query parameter and return the output
@app.get("/get_poem_pdf/")
def get_poem(query: str):
    output = get_data(query)
    # Log the query and output in log.json
    log_data = {
        "query": query,
        "output": output
    }

    logging.basicConfig(filename='log.json', level=logging.INFO)
    logging.info(json.dumps(log_data))
    
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

    # Return the PDF file as a response
    return FileResponse(pdf_file, filename=f'{query}.pdf', media_type="application/pdf")

if __name__ == "__main__":
    uvicorn.run(app)
    
    # query = input('Enter a word or two to make poem with: ')
    # print("<Wait for Output>")
    # #print two line break
    # print("\n")
    # print(get_data(query))
    