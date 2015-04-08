# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

class Articolo(ndb.Model):		
	#id_articolo = ndb.StringProperty()
	pass			

class Contenuto(ndb.Model):
	data_contenuto = ndb.StringProperty()
	autore_contenuto = ndb.StringProperty()
	autore_ascii_contenuto = ndb.StringProperty()
	titolo_contenuto = ndb.StringProperty()
	titolo_ascii_contenuto = ndb.StringProperty()
	sottotitolo_contenuto = ndb.StringProperty()
	corpo_contenuto = ndb.TextProperty()
	lingua_contenuto = ndb.StringProperty()

class StatoContenuto(ndb.Model):
	titolo_ascii_contenuto = ndb.StringProperty()
	stato_contenuto = ndb.StringProperty()
	stato_ascii_contenuto = ndb.StringProperty()

class FonteContenuto(ndb.Model):
	titolo_ascii_contenuto = ndb.StringProperty()
	nome_fonte = ndb.StringProperty()
	nome_ascii_fonte = ndb.StringProperty()
	link_fonte = ndb.StringProperty()

class Immagine(ndb.Model):
	data_immagine = ndb.StringProperty()
	tipo_immagine = ndb.StringProperty()
	nome_caricatore_immagine = ndb.StringProperty()
	nome_ascii_caricatore_immagine = ndb.StringProperty()
	nome_fonte_immagine = ndb.StringProperty()
	nome_ascii_fonte_immagine = ndb.StringProperty()
	link_fonte_immagine = ndb.StringProperty()
	descrizione_immagine = ndb.TextProperty()
	blob_immagine = ndb.BlobKeyProperty()

class ImmaginePrincipale(Immagine):
	pass

class ImmagineVetrina(Immagine):
	pass

class Etichetta(ndb.Model):
	titolo_ascii_contenuto = ndb.StringProperty()
	nome_etichetta = ndb.StringProperty()
	nome_ascii_etichetta = ndb.StringProperty()

