import pathlib
import re
import shutil
import string
import zipfile

import requests
import rs_utils

def process_list_file(filepath):
    return_msg = False
    resource_ids = []
    with open(filepath,'r') as f:
        for line in f:
            resource_ids.append(line)
    try:
        tmp = []
        for _id in resource_ids:
            tmp.append(int(_id))
        return_msg = tmp
    except:
        pass

    return return_msg

def get_alt_data(resource,alt_type,requester):
    alt_ref=None
    requester.rs_api_function = "get_alternative_files"
    requester.parameters = requester.format_params({"resource":resource,"type":alt_type})
    requester.make_query()
    response = requester.post_query()
    if response:
        alt_ref = response[0]['ref']
        file_extension = response[0]['file_extension']
        name = response[0]['name']

    return alt_ref,file_extension,name


def get_alt_url(resource,alt_ref,requester):
    alt_url = None
    requester.rs_api_function = "get_resource_path"
    requester.parameters = requester.format_params({
        "ref":resource,
        "alternative":alt_ref,
        "getfilepath":0
        })
    requester.make_query()
    response = requester.post_query()
    print(response)
    if response:
        alt_url = response

    return alt_url

def get_orig_filename(resource, requester):
    orig_filename = None
    requester.rs_api_function = "get_resource_field_data"
    requester.parameters = requester.format_params({
        "resource":resource
        })
    requester.make_query()
    response = requester.post_query()
    if response:
        resource_data = response
        orig_filename = rs_utils.filter_field_data_list(resource_data,"originalfilename")

    return orig_filename

def get_alts(alt_type,resource_ids):
    # this should get passed a list of resource ids from process_file()
    requester = rs_utils.RSpaceRequest()
    alts = {}
    for resource in resource_ids:
        alts[resource] = {"url":""}
        alts[resource]['orig_filename'] = get_orig_filename(resource, requester)
        alt_ref,file_extension,name = get_alt_data(resource,alt_type,requester)
        if alt_ref:
            alts[resource]['file_extension'] = file_extension
            alts[resource]['name'] = name
            alt_url = get_alt_url(resource,alt_ref,requester)
            alts[resource]['url'] = alt_url

    return alts

def make_zip(alts):
    print(alts)
    work_dir = pathlib.Path('temp/working_files')
    work_dir.mkdir(parents=True, exist_ok=True)
    print(work_dir)
    for alt,details in alts.items():
        alts[alt]['downloaded'] = False
        with requests.get(details['url'],stream=True) as r:
            if alts[alt]['orig_filename']:
                fn = alts[alt]['orig_filename']
                path = pathlib.Path(fn)
                stem = str(path.stem)
                name = re.sub(r"["+string.punctuation+string.whitespace+"]",'_',alts[alt]['name'])
                alt_name = f"{stem}_{name}.{alts[alt]['file_extension']}"
                temp_path = work_dir / path.with_name(alt_name)
            with open(str(temp_path),'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            if pathlib.Path(temp_path).exists:
                alts[alt]['downloaded'] = True

    zip_file = zipfile.ZipFile("temp/alternative_files.zip", "w")
    alt_files =  pathlib.Path(work_dir).glob('*.*')
    for file in alt_files:
        print(file)
        zip_file.write(file, compress_type=zipfile.ZIP_DEFLATED)

    shutil.rmtree(work_dir, ignore_errors=True)
    print(alts)
    return alts
