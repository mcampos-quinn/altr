% import config
% rebase('templates/base.tpl', title='Page Title')
<p> <b>Hello upload a file</b></p>

<label for="list_form">Choose an alt file type:</label>
<select class="" name="" form="list_form">
  Choose an alt file type:
  % for type,code in config.ALTERNATIVE_FILE_TYPES.items():
    <option value="{{ code }}">{{type}}</option>
  % end
</select>

<form action="/show_result" method="post" enctype="multipart/form-data" id="list_form">

  Select a text file list: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
</form>