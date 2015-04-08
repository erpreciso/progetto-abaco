$(window).ready(function(){
	
	// pulsante per codice pagina
	$(document).on('click',"#btn_1",function(){
		alert($("section").html());
		
	});
	
	// scrive la form per inserire l'articolo
	if ((esiste_elemento("form") == true)&& (esiste_elemento(null,null,"contenuto") == false))
		{ scrivi_form_inserimento_articolo(null); }
	
	// all'inserire di una etichetta, aggiungi input per la successiva
	$(document).on('change', "input[name='nome_etichetta']", function(){
		if ($("#nome_etichetta input:last").val() != "")
			{
			$("#nome_etichetta input")
				.css("background-color","#AFAFAF");
			aggiungi_altra_input("#nome_etichetta", "nome_etichetta", "scrivi qui un'altra etichetta");
			};
		});
	
	// all'inserire di una fonte, aggiungi input per la successiva
	$(document).on('change', "input[name='nome_fonte']", function(){
		if ($("#nome_fonte input:last").val() != "")
			{
			$("#nome_fonte input")
				.css("background-color","#AFAFAF");
			aggiungi_altra_input("#nome_fonte", "nome_fonte", "scrivi qui un'altra fonte");
			aggiungi_altra_input("#link_fonte", "link_fonte", "metti il link per la nuova fonte");
			};
		});
	
	// evita il POST al premere di ENTER
	$("input, select").keypress(function(event) { return event.keyCode != 13; });
	
	// aggiunge azione al premere del tasto immagine
	$(document).on('click',"#tasto_inserisci_immagine",function(){
		if (inserisco_altra_input_immagine())
			{ scrivi_sezione_inserimento_immagine();}
		else 
			{ return; }
	});
	
	// aggiunge azione al premere del tasto modifica_contenuto
	$(document).on('click',"#modifica_contenuto",function(){
		var vecchio_contenuto = salva_contenuto();
		$("#contenuto").remove();
		scrivi_form_inserimento_articolo(vecchio_contenuto);
	});
});

function salva_contenuto(){
	vecchio_contenuto = new Object();
	vecchia_immagine_principale = new Object();
	vecchie_vetrine = new Array();
	
	vecchio_contenuto.titolo_contenuto = $("#titolo_contenuto").text();
	vecchio_contenuto.sottotitolo_contenuto = $("#sottotitolo_contenuto").text();
	vecchio_contenuto.autore_contenuto = $("#autore_contenuto a").text();
	vecchio_contenuto.corpo_contenuto = $("#corpo_contenuto").text();
	vecchio_contenuto.etichette = new Array();
	$("#nome_etichetta").children().each(function(){
			vecchio_contenuto.etichette.push($(this).text());
		});
	vecchio_contenuto.nomi_fonti = new Array();
	vecchio_contenuto.link_fonti = new Array();
	$("#fonti").children(".nome_fonte").each(function(){
			vecchio_contenuto.nomi_fonti.push($(this).text());
		});
	$("#fonti").children(".link_fonte").each(function(){
			vecchio_contenuto.link_fonti.push($(this).text());
		});
	vecchia_immagine_principale.src = $("#immagine_principale img").attr("src");
	vecchia_immagine_principale.href = $("#immagine_principale a").attr("href");

	//for (var i=0;i<$("#immagini_vetrina").children().length;i++)
	$("#immagini_vetrina").children().each(function(){
		vetrina = new Object();
		vetrina.src = $(this).children("a").children("img").attr("src");
		vetrina.href = $(this).children("a").attr("href");
		vecchie_vetrine.push(vetrina);
		});
	return [vecchio_contenuto, vecchia_immagine_principale, vecchie_vetrine];
};

function aggiungi_altra_input(
								id_div,
								nome_input,
								placeholder
								){
	var elm_inp_nome_etichetta = $(document.createElement("input"))
		.attr("name", nome_input)
		.attr("type", "text")
		.attr("placeholder", placeholder)
		.attr("size", "15");
	$(id_div).append(elm_inp_nome_etichetta);
};

function formatta_data(date) {
    var mm = date.getMonth() + 1;
    var dd = date.getDate();
    var yyyy = date.getFullYear();
    mm = (mm < 10) ? '0' + mm : mm;
    dd = (dd < 10) ? '0' + dd : dd;
    var hh = date.getHours();
    var min = date.getMinutes();
    var ss = date.getSeconds();
    hh = (hh < 10) ? '0' + hh : hh;
    min = (min < 10) ? '0' + min : min;
    ss = (ss < 10) ? '0' + ss : ss;
    return yyyy + "-" + mm + "-" + dd + " " + hh + ":" + min + ":" + ss;
};


function scrivi_sezione_inserimento_immagine(){
	var dove_appendere = $("#inserimento_immagine");
	// categoria (lista)
	var elm_div_categoria_immagine = $(document.createElement("div"))
		.attr("id", "categoria_immagine");
	var elm_sel_categoria_immagine = $(document.createElement("select"))
		.attr("name", "categoria_immagine");
	$(elm_sel_categoria_immagine)
				.append($("<option>")
					.attr("value", "principale")
					.text("Immagine principale")
					)
				.append($("<option>")
					.attr("value", "vetrina")
					.text("Immagine vetrina")
					);
	// caricatore
	var elm_div_nome_caricatore_immagine = $(document.createElement("div"))
		.attr("class", "nome_caricatore_immagine");
	var elm_inp_nome_caricatore_immagine = $(document.createElement("input"))
		.attr("name", "nome_caricatore_immagine")
		.attr("type", "text")
		.attr("required", "required")
		.attr("placeholder", "chi sta caricando l'immagine?");
	// data
	// tipo (lista)
	var elm_div_tipo_immagine = $(document.createElement("div"))
		.attr("id", "tipo_immagine");
	var elm_sel_tipo_immagine = $(document.createElement("select"))
		.attr("name", "tipo_immagine");
	$.getJSON("/liste/liste.json", function(data) {
		for (var i=0;i<data.tipo_immagine.length;i++)
			{ 
			$(elm_sel_tipo_immagine)
				.append($("<option>")
					.attr("value", data.tipo_immagine[i].ascii)
					.text(data.tipo_immagine[i].text)
					);
			}
	});
	// fonte_nome
	var elm_div_nome_fonte_immagine = $(document.createElement("div"))
		.attr("id", "nome_fonte_immagine");
	var elm_inp_nome_fonte_immagine = $(document.createElement("input"))
		.attr("name", "nome_fonte_immagine")
		.attr("type", "text")
		.attr("size", "15")
		.attr("placeholder", "da dove viene l'immagine?");
	// fonte_link
	var elm_div_link_fonte_immagine = $(document.createElement("div"))
		.attr("id", "link_fonte_immagine");
	var elm_inp_link_fonte_immagine = $(document.createElement("input"))
		.attr("name", "link_fonte_immagine")
		.attr("type", "text")
		.attr("size", "25")
		.attr("placeholder", "metti il link, se necessario");
	// descrizione immagine
	var elm_div_descrizione_immagine = $(document.createElement("div"))
		.attr("id", "descrizione_immagine");
	var elm_inp_descrizione_immagine = $(document.createElement("input"))
		.attr("name", "descrizione_immagine")
		.attr("type", "text")
		.attr("size", "25")
		.attr("placeholder", "descrivi l'immagine");
	// blob immagine
	var elm_div_blob_immagine = $(document.createElement("div"))
		.attr("id", "blob_immagine");
	var elm_inp_blob_immagine = $(document.createElement("input"))
		.attr("name", "blob_immagine")
		.attr("type", "file")
		.attr("placeholder", "dove trovo il file immagine?");
		
	if (esiste_elemento(null,null,"sezione_caricamento_immagini") == false)
		{ var elm_div_sezione_caricamento_immagini = $(document.createElement("div"))
		.attr("id", "sezione_caricamento_immagini");
		dove_appendere.before(elm_div_sezione_caricamento_immagini);
		}
	else
		{ elm_div_sezione_caricamento_immagini = $("#sezione_caricamento_immagini");}
	elm_div_sezione_caricamento_immagini
			.append(elm_div_categoria_immagine.append(elm_sel_categoria_immagine))
			.append(elm_div_nome_caricatore_immagine.append(elm_inp_nome_caricatore_immagine))
			.append(elm_div_tipo_immagine.append(elm_sel_tipo_immagine))
			.append(elm_div_nome_fonte_immagine.append(elm_inp_nome_fonte_immagine))
			.append(elm_div_link_fonte_immagine.append(elm_inp_link_fonte_immagine))
			.append(elm_div_descrizione_immagine.append(elm_inp_descrizione_immagine))
			.append(elm_div_blob_immagine.append(elm_inp_blob_immagine));
};


function scrivi_form_inserimento_articolo(vecchio_contenuto){
	elm_form = $("form")
		.attr("enctype", "multipart/form-data")
		.attr("method", "POST");
	// crea le singole sezioni
	// titolo
	var elm_div_titolo_contenuto = $(document.createElement("div"))
		.attr("id", "titolo_contenuto");
	var elm_inp_titolo_contenuto = $(document.createElement("input"))
		.attr("name", "titolo_contenuto")
		.attr("type", "text")
		.attr("required", "required")
		.attr("placeholder", "che titolo gli vuoi dare?")
		.attr("maxlength", 300);
	
	// sottotitolo
	var elm_div_sottotitolo_contenuto = $(document.createElement("div"))
		.attr("id", "sottotitolo_contenuto");
	var elm_inp_sottotitolo_contenuto = $(document.createElement("input"))
		.attr("name", "sottotitolo_contenuto")
		.attr("type", "text")
		//.attr("value", sottotitolo_contenuto)
		.attr("placeholder", "che sottotitolo gli vuoi dare?")
		.attr("maxlength", 300);
	// info
	var elm_div_info_1 = $(document.createElement("div"))
		.attr("class", "info");
	// data
	var elm_div_data_contenuto = $(document.createElement("div"))
		.attr("id", "data_contenuto")
		.text(formatta_data(new Date(jQuery.now())));
		// non serve creare l'input in quanto la data è inserita automaticamente
	// autore
	var elm_div_autore_contenuto = $(document.createElement("div"))
		.attr("id", "autore_contenuto");
	var elm_inp_autore_contenuto = $(document.createElement("input"))
		.attr("name", "autore_contenuto")
		.attr("type", "text")
		.attr("placeholder", "chi sta scrivendo?")
		.attr("size", "15");
	// etichette
	var elm_div_nome_etichetta = $(document.createElement("div"))
		.attr("id", "nome_etichetta")
		.text("Etichette: ");
	var elm_inp_nome_etichetta = $(document.createElement("input"))
		.attr("name", "nome_etichetta")
		.attr("type", "text")
		.attr("placeholder", "scrivi qui l'etichetta")
		.attr("size", "15");
	// corpo
	var elm_div_corpo_contenuto = $(document.createElement("div"))
		.attr("id", "corpo_contenuto");
	var elm_inp_corpo_contenuto = $(document.createElement("textarea"))
		.attr("name", "corpo_contenuto")
		.attr("rows", 8)
	// info
	var elm_div_info_2 = $(document.createElement("div"))
		.attr("class", "info");
	// fonte_nome
	var elm_div_nome_fonte = $(document.createElement("div"))
		.attr("id", "nome_fonte");
	var elm_inp_nome_fonte = $(document.createElement("input"))
		.attr("name", "nome_fonte")
		.attr("type", "text")
		.attr("size", "15")
		.attr("placeholder", "da dove viene questo?");
	// fonte_link
	var elm_div_link_fonte = $(document.createElement("div"))
		.attr("id", "link_fonte");
	var elm_inp_link_fonte = $(document.createElement("input"))
		.attr("name", "link_fonte")
		.attr("type", "text")
		.attr("size", "25")
		.attr("placeholder", "metti il link, se necessario");
	// stato contenuto
	var elm_div_stato_contenuto = $(document.createElement("div"))
		.attr("id", "stato_contenuto");
	var elm_sel_stato_contenuto = $(document.createElement("select"))
		.attr("multiple", "multiple")
		.attr("name", "stato_contenuto[]");
	$.getJSON("/liste/liste.json", function(data) {
		for (var i=0;i<data.stato_del_contenuto.length;i++)
			{ 
			$(elm_sel_stato_contenuto)
				.append($("<option>")
					.attr("value", data.stato_del_contenuto[i].ascii)
					.text(data.stato_del_contenuto[i].text)
					);
			}
	});
	// blocco inserimento immagine
	var elm_div_tasto_immagine = $(document.createElement("div"))
		.attr("id", "inserimento_immagine");
	var elm_btn_tasto_immagine = $(document.createElement("button"))
		.attr("type", "button")
		.attr("id", "tasto_inserisci_immagine")
		.text("Inserisci un'immagine");
	// tasto submit
	var elm_div_submit = $(document.createElement("div"))
		.attr("id", "submit");
	var elm_inp_submit = $(document.createElement("input"))
		.attr("type", "submit")
		.attr("value", "Pubblica");

	elm_form
	.append(elm_div_titolo_contenuto.append(elm_inp_titolo_contenuto))
	.append(elm_div_sottotitolo_contenuto.append(elm_inp_sottotitolo_contenuto))
	.append(elm_div_info_1
		.append(elm_div_data_contenuto)
		.append(elm_div_autore_contenuto.append(elm_inp_autore_contenuto))
		)
	.append(elm_div_nome_etichetta.append(elm_inp_nome_etichetta))
	.append(elm_div_corpo_contenuto.append(elm_inp_corpo_contenuto))
	.append(elm_div_info_2
		.append(elm_div_nome_fonte.append(elm_inp_nome_fonte))
		.append(elm_div_link_fonte.append(elm_inp_link_fonte))
		)
	.append(elm_div_stato_contenuto.append(elm_sel_stato_contenuto))
	.append(elm_div_tasto_immagine.append(elm_btn_tasto_immagine))
	.append(elm_div_submit.append(elm_inp_submit))
	;
	
	if (vecchio_contenuto != null)
		{
		elm_inp_titolo_contenuto.attr("value", vecchio_contenuto[0].titolo_contenuto);
		elm_inp_sottotitolo_contenuto.attr("value", vecchio_contenuto[0].sottotitolo_contenuto);
		elm_inp_autore_contenuto.attr("value", vecchio_contenuto[0].autore_contenuto);
		elm_inp_corpo_contenuto.text(vecchio_contenuto[0].corpo_contenuto);
		for (var i=0;i<vecchio_contenuto[0].etichette.length;i++)
			{
			elm_div_nome_etichetta.append($(document.createElement("input"))
				.attr("name", "nome_etichetta")
				.attr("type", "text")
				.attr("value", vecchio_contenuto[0].etichette[i]));
			}
		for (var i=0;i<vecchio_contenuto[0].nomi_fonti.length;i++)
			{
			elm_div_info_2.append($(document.createElement("input"))
				.attr("name", "nome_fonte")
				.attr("type", "text")
				.attr("value", vecchio_contenuto[0].nomi_fonti[i]));
			elm_div_info_2.append($(document.createElement("input"))
				.attr("name", "link_fonte")
				.attr("type", "text")
				.attr("value", vecchio_contenuto[0].link_fonti[i]));
			}
		if (vecchio_contenuto[1] != null)
			{
			elm_form.append($(document.createElement("div"))
				.attr("id", "immagine_principale").append($(document.createElement("a")).attr("href", vecchio_contenuto[1].href).append($(document.createElement("img")).attr("src", vecchio_contenuto[1].src))));
			}
		if (vecchio_contenuto[2] != null)
			{
			var vetrina = $(document.createElement("div")).attr("id", "immagini_vetrina");
			for (var i=0;i<vecchio_contenuto[2].length;i++){
				vetrina.append($(document.createElement("div"))
				.attr("class", "vetrina").append($(document.createElement("a")).attr("href", vecchio_contenuto[2][i].href).append($(document.createElement("img")).attr("src", vecchio_contenuto[2][i].src))));
			};
			elm_form.append(vetrina);
			}
		
		}
};

function esiste_elemento(
		tag_elemento,
        classe_elemento,
		id_elemento
		){
	if (id_elemento)
		{ return $("#" + id_elemento).length > 0; }
    else if (classe_elemento)
        { return $("." + classe_elemento).length > 0; }
        
	else if (tag_elemento)
		{ return $(tag_elemento).length > 0; }
	else
		{ return false; }
};

function inserisco_altra_input_immagine(){
	if (esiste_elemento(null,null,"sezione_caricamento_immagini") == false)
		{ return true; }
	var ultima_input = $("#sezione_caricamento_immagini .nome_caricatore_immagine:last input");
	if (ultima_input.val() == "" || ultima_input.val() == undefined)
		{ return false; }
	else
		{ return true; }
};
