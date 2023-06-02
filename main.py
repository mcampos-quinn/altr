from fastapi import FastAPI
from fastapi.responses import FileResponse


#https://fastapi.tiangolo.com/advanced/custom-response/?h=fileresponse#fileresponse
@app.get("/get_alts/{type}/file_ids.txt")
async def main():
     # download the text file of rs ids and the alt file type (tbd, maybe set in url?)
     # query rs for each alt
     # download alts to temp folder
     # zip them and return to user's browser
     # clear temp folder
    return FileResponse(some_file_path)
