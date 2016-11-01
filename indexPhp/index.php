<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>My Python ERP</title>
  </head>
  <body>
    <h1>Welcome to my Python ERP !</h1>
    <div id="block-form">
      <h3>Ajouter un client</h3>
        <form action="127.0.0.1:5000/addUser" id="my-form" name="myform" method="POST">
            <label for="enterpriseName" placeholder="Entrez le nom de l'entreprise">Entreprise :</label>
            <input type="text" name="enterpriseName">
            <br>
            <label for="contactName" placeholder="Entrez le nom de l'entreprise">Nom complet du contact :</label>
            <input type="text" name="contactName">
            <br>
            <label for="select">Etat :</label>
            <select name="select">
              <option value="prospect">Prospect</option>
              <option value="ongoingProject">Projet en cours</option>
              <option value="projectFinished">Projet terminé</option>
              <option value="partner">Partenaire</option>
            </select>
            <br>
            <br>
            <input type="button" id="btn-submit" name="btn" value="Valider">
        </form>
    </div>
  </body>
  <style>
      #block-form
      {
        margin-top: 100px;
        width: 100%
      }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  <script type="text/javascript">
      document.getElementById("btn-submit").addEventListener("click", function(){
          console.log('form post');
          // document.forms['myform'].submit();


          $.ajax({
              url: 'http://127.0.0.1:5000/addUser',
              dataType: 'json',
              type: 'post',
              contentType: 'application/json',
              data: $("form").serializeArray(),
              headers: {
                'Access-Control-Allow-Origin' : 'http://localhost:8888/',
              },
              success: function( data, textStatus, jQxhr ){
                  $('#response pre').html( JSON.stringify( data ) );
              },
              error: function(jqXhr, textStatus, errorThrown ){
                  console.log( errorThrown );
              }
          });
      });


  </script>
</html>
