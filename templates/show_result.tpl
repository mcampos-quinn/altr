% from bottle import  SimpleTemplate, template
% rebase('templates/base.tpl', title='Results')
<div class="container mt-3">
  <div class="row">
    <p class="fs-1 fw-bold">Here's the outcome of your request</p>
  </div>
  % if results:
  <div class="row">
    % include('templates/alt_table.tpl',results=results)
    <div class="col-3">
      % if results["zipfile"] != False:
        <p> Here's your zip file:
          <form class="form-control" action="/zip" method="get">
            <button type="submit" class="btn btn-primary" value="Get files">
              Get files
            </button>
          </form>
        </p>
      % end
    </div>
  </div>
  % else:
  <div class="row">
    <p>Sorry, there were no alternative files for the images you selected :(</p>
  </div>
  <div class="row">
    <p>{{ msg }}</p>
  </div>
  % end
</div>
