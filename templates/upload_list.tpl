% import config
% rebase('templates/base.tpl', title='Upload list')
<div class="container mt-3">
  <div class="row">
    <div class="col">
      <p>Upload a plain text file that includes a list of resource IDs for which you want to download cropped/alternative files.</p>
      <p>Instructions:
        <ul>
          <li>when you make your cropped selections in RS, make sure that they are marked with the correct type (e.g. "web crop")</li>
          <li>put all the resources with crops you want into a collection in resourcespace</li>
          <li>from "Actions" choose "Download metadata CSV"</li>
          <li>open the csv and copy the resource IDs from the first column, then paste them into a plain text file</li>
          <li>there should be one ID per line, and that's it (no other text, etc.)</li>
          <li>upload the file here and select the correct type ("web crop" or whatever)</li>
          <li>your files will get wrapped in a zip file that you can then download</li>
        </ul>
      </p>
    </div>
  </div>
  <div class="row g-3">
    <div class="col-3">
      <label for="list_form" class="form-label">Choose an alt file type:</label>
      <select class="form-select" name="alt_type" form="list_form">
        Choose an alt file type:
        % for type in config.ALTERNATIVE_FILE_TYPES:
          <option value="{{ type }}">{{type}}</option>
        % end
      </select>

      <form action="/show_result" method="post" enctype="multipart/form-data" id="list_form">
        <label for="upload" class="form-label"></label>
        <input class="form-control" type="file" name="upload" />
        <input class="btn btn-primary mt-3" type="submit" value="Start upload" />
      </form>
    </div>
  </div>
</div>
