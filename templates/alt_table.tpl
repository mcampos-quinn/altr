<table class="table table-striped">
  <thead>
    <tr>
      <th scope="col">Original Resource</th>
      <th scope="col">Alternative file downloaded?</th>
      <th scope="col">Note</th>
      <th scope="col">Alternative file url</th>
    </tr>
  </thead>
  <tbody>
    % for k,v in results['alts'].items():
      <tr>
        <th scope="row">{{ results['alts'][k]['orig_filename'] }}</th>
        <td>{{results['alts'][k]['downloaded']}}</td>
        <td>{{results['alts'][k]['note']}}<td>
        % if v['requested']:
          <td>{{results['alts'][k]['url']}}<td>
        % elif results['alts'][k]['url'] not in ("",None):
          <td><a href="{{results['alts'][k]['url']}}">Direct link</a><td>
        % else:
          <td></td>
        % end
      </tr>
    % end
 </tbody>
</table>
