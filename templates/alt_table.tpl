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
      % if 'requested' in v:
      <tr>
        <th scope="row">{{ results['alts'][k]['orig_filename'] }}</th>
        <td>{{results['alts'][k]['downloaded']}}</td>
        <td>{{results['alts'][k]['note']}}<td>
        % if v['requested']:
        <td>{{results['alts'][k]['url']}}<td>
        % else:
        <td><a href="{{results['alts'][k]['url']}}">Direct link</a><td>
        % end
      </tr>
      % end
    % end
 </tbody>
</table>
