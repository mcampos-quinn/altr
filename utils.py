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
    alt_ref = file_extension = name = None
    requester.rs_api_function = "get_alternative_files"
    requester.parameters = requester.format_params({"resource":resource,"type":alt_type})
    requester.make_query()
    response = requester.post_query()
    # print(response)
    if response:
        alt_ref = response[0]['ref']
        file_extension = response[0]['file_extension']
        name = response[0]['name']
        result = [{'ref':alt_ref,"ext":file_extension,"name":name,"requested":True}]
    else:
        requester.parameters = requester.format_params({"resource":resource})
        requester.make_query()
        response = requester.post_query()
        # print(response)
        if response and len(response) > 1:
            result = []
            for item in response:
                # print(item)
                alt_ref = item['ref']
                file_extension = item['file_extension']
                name = item['name']
                result.append({'ref':alt_ref,"ext":file_extension,"name":name,"requested":False})
        elif response and len(response) == 1:
            alt_ref = response[0]['ref']
            file_extension = response[0]['file_extension']
            name = response[0]['name']
            result = [{'ref':alt_ref,"ext":file_extension,"name":name,"requested":False}]
        else:
            result = None

    # print(result)
    return result

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
    # print(response)
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
    results = {}
    # if there are alts of a type other than what's requested we need to pop the
    # original dict from the results bc the different types get their own keys/entries
    # and the originals are listed here
    to_pop = []
    results['alts'] = {}
    for resource in resource_ids:
        results['alts'][resource] = {"url":"","downloaded":False,"note":"","requested":False}
        results['alts'][resource]['orig_filename'] = get_orig_filename(resource, requester)
        # alt_ref,file_extension,name = get_alt_data(resource,alt_type,requester)
        alt_data = get_alt_data(resource,alt_type,requester)
        # print(alt_data)
        if alt_data and any([x['requested'] == True for x in alt_data]):
            for item in alt_data:
                if item['requested'] == True:
                    alt_url = get_alt_url(resource,item['ref'],requester)
                    results['alts'][resource]['url'] = alt_url
                    results['alts'][resource]['file_extension'] = item['ext']
                    results['alts'][resource]['name'] = item['name']
                    results['alts'][resource]['note'] = ""
                    results['alts'][resource]['requested'] = True
                    break
        elif alt_data != None:
            counter = 1
            to_pop.append(resource)
            for item in alt_data:
                alt_url = get_alt_url(resource,item['ref'],requester)
                # give each non-requested alt type its own dict based on the original
                results['alts'][str(resource)+" "+str(counter)] = {"downloaded":False}
                results['alts'][str(resource)+" "+str(counter)]['url'] = alt_url
                results['alts'][str(resource)+" "+str(counter)]['file_extension'] = item['ext']
                results['alts'][str(resource)+" "+str(counter)]['name'] = item['name']
                results['alts'][str(resource)+" "+str(counter)]['orig_filename'] = results['alts'][resource]['orig_filename']
                results['alts'][str(resource)+" "+str(counter)]['requested'] = False
                results['alts'][str(resource)+" "+str(counter)]['note'] = f"This is not the alternative file type you requested ({alt_type}) but you can click on the URL here to download it anyway."
                counter += 1
        else:
            results['alts'][resource]['url'] = \
            results['alts'][resource]['name'] = \
            results['alts'][resource]['file_extension'] = None
    if to_pop != []:
        # now if there are any extraneous resource listings, remove them from
        # the results
        try:
            for resource in to_pop:
                results['alts'].pop(resource)
        except:
            pass
    # print(results)
    return results

def make_zip(results):
    # print(results)
    results['zipfile']=False
    # print(results)
    work_dir = pathlib.Path('temp/working_files')
    work_dir.mkdir(parents=True, exist_ok=True)
    for alt,details in results['alts'].items():
        if details['url'] in ('',False,None):
            continue
        if details['requested'] == True:
            with requests.get(details['url'],stream=True) as r:
                if results['alts'][alt]['orig_filename']:
                    fn = results['alts'][alt]['orig_filename']
                    path = pathlib.Path(fn)
                    stem = str(path.stem)
                    name = re.sub(r"["+string.punctuation+string.whitespace+"]",'_',results['alts'][alt]['name'])
                    alt_name = f"{stem}_{name}.{results['alts'][alt]['file_extension']}"
                    temp_path = work_dir / path.with_name(alt_name)
                with open(str(temp_path),'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                if pathlib.Path(temp_path).exists:
                    results['alts'][alt]['downloaded'] = True

    alt_files = [x for x in pathlib.Path(work_dir).glob('*.*')]
    if alt_files != []:
        with zipfile.ZipFile("temp/alternative_files.zip", "w") as zip_file:
            for file in alt_files:
                if file.is_file():
                    zip_file.write(file, compress_type=zipfile.ZIP_DEFLATED,arcname=file.name)
        results['zipfile'] = True
    shutil.rmtree(work_dir, ignore_errors=True)
    # print(alts)
    return results
