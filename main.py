import pathlib

from bottle import route, run, template, request

import utils

@route('/altr')
def upload_list():

    return template('templates/upload_list')

@route('/show_result', method='POST')
def show_result():
    upload = request.files.get('upload')
    file_ids = None
    filepath = pathlib.Path('temp'+upload.filename)
    if filepath.exists():
        upload.save(filepath)
        file_ids = utils.process_file(filepath)
    else:
        return template('templates/show_result', result=None, msg="You didn't upload a file?")
    if not file_ids:
        return template('templates/show_result', result=None, msg="Sorry there was a problem with your list file")
    else:
        utils.get_alts(file_ids)

    return template('templates/show_result', result=filepath, msg="Success")

run(host='localhost', port=8080, debug=True,reloader=True)
