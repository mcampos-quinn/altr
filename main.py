import os
import pathlib

from bottle import Bottle, route, run, template, request, static_file

import utils

app = application = Bottle()

@app.route('/altr')
def upload_list():

    return template('templates/upload_list')

@app.route('/zip', method='GET')
def get_zip():

    return static_file('alternative_files.zip', root='temp')

@app.route('/show_result', method='POST')
def show_result():
    upload = request.files.get('upload')
    # print(upload)
    alt_type = request.forms.get('alt_type')
    # print(alt_type)
    resource_ids = None
    results = None
    filepath = None
    save_path = 'temp/'
    # print(save_path)
    try:
        filename = upload.filename
        upload.save(save_path,overwrite=True)
        filepath = os.path.join(save_path,filename)
        # print(filepath)
    except:
        return template('templates/show_result', result=None, msg="You didn't upload a file?")

    if os.path.isfile(filepath):
        resource_ids = utils.process_list_file(filepath)
        # print(resource_ids)
        results = utils.get_alts(alt_type,resource_ids)
        # print(results)
        results = utils.make_zip(results)

    if not resource_ids:
        return template('templates/show_result', results=None, msg="Sorry there was a problem with your list file")


    return template('templates/show_result', results=results, msg="")

# FOR DEV ONLY! FOR PRODUCTION COMMENT THIS LINE
app.run(host='localhost', port=8080, debug=True,reloader=True)
