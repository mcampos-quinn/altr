% import config
% rebase('templates/base.tpl', title='Page Title')
<p> <b>Hello upload a file</b></p>

<label for="list_form">Choose an alt file type:</label>
<select class="" name="alt_type" form="list_form">
  Choose an alt file type:
  % for type in config.ALTERNATIVE_FILE_TYPES:
    <option value="{{ type }}">{{type}}</option>
  % end
</select>

<form action="/show_result" method="post" enctype="multipart/form-data" id="list_form">

  Select a text file list: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
</form>
