<table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">Original Resource</th>
      <th scope="col">Alternative file downloaded?</th>
      <th scope="col">Alternative file url</th>
    </tr>
  </thead>
  <tbody>
    % for k,v in results['alts'].items():
      <tr>
        <th scope="row">{{ results['alts'][k]['orig_filename'] }}</th>
        <td>{{results['alts'][k]['downloaded']}}</td>
        <td>{{results['alts'][k]['url']}}<td>
      </tr>
    % end
 </tbody>
</table>
