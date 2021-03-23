function dessin_jauge(element_div , taille , ratio , color , ombre , contexte){

  if(contexte===true){
  
    var circle = $('<canvas width="'+(taille*2)+'px" height="'+(taille*2)+'px" />');
    element_div.append(circle);
    //CONFIGURATION DU PLAN DE TRAVAIL EN 2 DIMENSIONS 
    var ctx = circle[0].getContext('2d');

  }else{
    ctx = contexte;
  }
  // DEBUT DU DESSIN
  ctx.beginPath();
  //DESSIN D'UN CERCLE
  ctx.arc(taille,taille,(taille/100*85), -1/2*Math.PI , ratio*2*Math.PI-1/2*Math.PI);
  //TAILLE D'UN BORD
  ctx.lineWidth = (taille/100*20);
  //COULEUR DU BORD
  ctx.strokeStyle = color;

  if(ombre){

    //POSITION DE L'OMBRE
    ctx.shadowOffsetX = (taille/100*1.5);
    //TAILLE DE L'OMBRE
    ctx.shadowBlur = (taille/100*8);
    //COULEUR DE l'OMBRE
    ctx.shadowColor='rgba(0,0,0,0.5)';

  }

  //FIN DU DESSIN
  ctx.stroke();

  return ctx;

}