% from bottle import  SimpleTemplate, template
% rebase('templates/base.tpl', title='Results')
<div class="container mt-3">
  <div class="row">
    <p class="fs-1 fw-bold">Here's the outcome of your request</p>
  </div>
  % if alts:
  <div class="row">
    % include('templates/alt_table.tpl',alts=alts)
    <div class="col-3">
      <p> Here's your zip file:
        <form class="form-control" action="/zip" method="get">
          <button type="submit" class="btn btn-primary" value="Get files">
            Get files
          </button>
        </form>
      </p>
    </div>
  </div>
  % end
</div>
