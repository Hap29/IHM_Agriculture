(function($){

  //ENTOURAGE DU CHAMP DE TEXTE AVEC UNE BALISE div QUI CONTIENT LA JAUGE
  $('input.compteur').wrap('<div class="compteur" />').each(function(){

    //INITIALISATION DES VARIABLES
    var element_input = $(this); //CHAMP DE TEXTE AVEC UN POINTEUR
    var element_div = element_input.parent(); //VARIABLE DE LA BALISE div
    //RECUPERATION DE LA VALEUR MINIMUM DE LA JAUGE
    var min = element_input.data('min');
    //RECUPERATION DE LA VALEUR MAXIMUM DE LA JAUGE
    var max = element_input.data('max');
    //RECUPERATION DE LA  COULEUR DE LA JAUGE
    var color = element_input.data('color') ? element_input.data('color') : "#91c2ff" ;
    //RECUPERATION DE LA TAILLE DE LA JAUGE
    var taille = element_input.data('taille') ? element_input.data('taille') : 100 ;
    //RECUPERATION DE LA VALEUR PAR DEFAUT ET TRANSFORMATION EN POURCENTAGE
    var ratio = ( element_input.val() - min ) / ( max - min );

    //MISE EN FORME DE LA BALISE div ET DU TEXTE
    element_div.width(taille*2)
               .height(taille*2);
    element_input.width(taille)
                 .css("font-size",(taille/100*40)+"px")
                 .css("top",(taille/100*70)+"px")
                 .css("left",(taille/100*50)+"px");

    //ECRITURE/DESSIN DE LA JAUGE CIRCULAIRE A L'AIDE DU D'UN ESPACE DE DESSIN (canevas)
    dessin_jauge(element_div , taille , 1 , "#fff" , true , true);
    
    //ECRITURE/DESSIN DE LA JAUGE CIRCULAIRE
    var contexte = dessin_jauge(element_div , taille , ratio , color , false , true);

  });

})(jQuery); 