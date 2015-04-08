# coding: utf-8
# copyright Stefano Merlo
# [progetto-abaco] website

import webapp2
import jinja2
import random
import string
import json
import os
import unicodedata
from google.appengine.ext import ndb, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from time import localtime, strftime, sleep
from oggetti import *

# funzioni

def generatore_id_casuale(
			size = 6,
			chars = string.ascii_uppercase + string.digits
			):
	return ''.join(random.choice(chars) for x in range(size))

def converti_unicode_in_ascii(testo):
	res = ''
	nkfd_form = unicodedata.normalize('NFKD', unicode(testo))
	q = u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
	res = ''.join(e for e in q if e.isalnum())
	return res

def questo_istante():
	"""restituisce data e ora in questo istante, formato 'yyyy-mm-dd HH-MM-SS'"""
	return strftime("%Y-%m-%d %H:%M:%S", localtime())

def tutti_titoli_ascii_contenuto():
	"""restituisce la lista dei titoli ascii contenuto presenti nel datastore, altrimenti None"""
	l = Contenuto.query()
	if l:
		res = []
		for p in l:
			res.append(p.titolo_ascii_contenuto)
		return res
	return None

def tutte_etichette():
	"""restituisce la lista delle etichette presenti nel datastore in forma di dizionario {etichetta,etichetta formattata}, altrimenti None"""
	l = Etichetta.query()
	if l:
		res = {"ascii": [], "text": []}
		for e in l:
			if e.nome_ascii_etichetta not in res["ascii"]:
				res["ascii"].append(e.nome_ascii_etichetta)
				res["text"].append(e.nome_etichetta)
		return res
	return None

def oggetto_articolo(id_articolo):
	"""restituisce un oggetto articolo corrispondente al id inserito"""
	return ndb.Query(Articolo).filter('id_articolo = ', id_articolo).get()

def estrai_ultimo_contenuto(oggetto_articolo):
	"""restituisce il contenuto più recente figlio dell'articolo"""
	q = ndb.Query(Contenuto).ancestor(oggetto_articolo.key()).order("data_contenuto")
	if q.get() == None:
		return None
	else:
		return q.get()

def url_immagine(oggetto_immagine, dimensione=None):
	"""restituisce url dell'immagine della dimensione specificata, numero o 'max'"""
	
	if dimensione == 'max':
		dimensione_pixel = 1600
	else:
		dimensione_pixel = dimensione
	
	if oggetto_immagine and oggetto_immagine.blob_immagine:
		
		return images.get_serving_url(oggetto_immagine.blob_immagine, size=dimensione_pixel)
	return None

def immagine_principale_del_contenuto(oggetto_contenuto):
	"""restituisce l'immagine principale del contenuto, oppure None"""
	q = ImmaginePrincipale.query(ancestor=articolo_del_contenuto(oggetto_contenuto).key)
	if q.get() == None:
		return None
	else:
		res = []
		for p in q:
			res.append(p)
		#assert len(res) == 1
		return res[0]
		
def immagini_vetrina_del_contenuto(oggetto_contenuto):
	"""restituisce la lista delle immagini vetrina del contenuto, oppure None"""
	q = ImmagineVetrina.query(ancestor=articolo_del_contenuto(oggetto_contenuto).key)
	if q.get() == None:
		return None
	else:
		res = []
		for p in q:
			res.append(p)
		return res

def articolo_del_contenuto(oggetto_contenuto):
	"""dell'oggetto contenuto passato, ricava l'articolo madre"""
	return oggetto_contenuto.key.parent().get()

def stati_contenuto_per_contenuto(objContenuto):
	q = StatoContenuto.query(StatoContenuto.titolo_ascii_contenuto == objContenuto.titolo_ascii_contenuto)
	if q.get():
		res = []
		for r in q:
			res.append([r.stato_contenuto, r.stato_ascii_contenuto])
		return res
	else:
		return None

def fonti_contenuto_per_contenuto(objContenuto):
	q = FonteContenuto.query(FonteContenuto.titolo_ascii_contenuto == objContenuto.titolo_ascii_contenuto)
	if q.get():
		res = []
		for r in q:
			res.append([r.nome_fonte, r.nome_ascii_fonte, r.link_fonte])
		return res
	else:
		return None

def contenuti_per_fonte(strAsciiFonte):
	q = FonteContenuto.query(FonteContenuto.nome_ascii_fonte == strAsciiFonte)
	if q.get():
		res = []
		for r in q:
			res.append(r.titolo_ascii_contenuto)
		return res
	else:
		return None

def contenuti_per_stato(strAsciiStato):
	q = StatoContenuto.query(StatoContenuto.stato_ascii_contenuto == strAsciiStato)
	if q.get():
		res = []
		for r in q:
			res.append(r.titolo_ascii_contenuto)
		return res
	else:
		return None

def contenuti_per_etichetta(strAsciiEtichetta):
	q = Etichetta.query(Etichetta.nome_ascii_etichetta == strAsciiEtichetta)
	if q.get():
		res = []
		for r in q:
			if r.titolo_ascii_contenuto not in res:
				res.append(r.titolo_ascii_contenuto)
		return res
	else:
		return None

def etichette_contenuto_per_contenuto(objContenuto):
	q = Etichetta.query(Etichetta.titolo_ascii_contenuto == objContenuto.titolo_ascii_contenuto)
	if q.get():
		res = []
		for r in q:
			res.append([r.nome_etichetta, r.nome_ascii_etichetta])
		return res
	else:
		return None

def estrai_contenuti(
						quanti = 1,
						criterio = None,
						valore = "",
					):
	if criterio == "recenti" or criterio == None:
		q = Contenuto.query().order(-Contenuto.data_contenuto)
	elif criterio == "articolo":
		assert quanti == 1
		q = Contenuto.query(Contenuto.titolo_ascii_contenuto == valore)
	elif criterio == "autore":
		q = Contenuto.query(Contenuto.autore_ascii_contenuto == valore)
	elif criterio == "fonte":
		q = Contenuto.query(Contenuto.titolo_ascii_contenuto.IN(contenuti_per_fonte(valore)))
	elif criterio == "stato":
		q = Contenuto.query(Contenuto.titolo_ascii_contenuto.IN(contenuti_per_stato(valore)))
	elif criterio == "etichetta":
		q = Contenuto.query(Contenuto.titolo_ascii_contenuto.IN(contenuti_per_etichetta(valore)))
	else:
		raise Exception("indica almeno un criterio di estrazione contenuti. attuale == " + criterio)
	if q.get():
		oggetti = q.fetch(quanti)
		stati = {}
		fonti = {}
		etichette = {}
		miniature = {}
		vetrine = {}
		for r in oggetti:
			stati[r.titolo_ascii_contenuto] = stati_contenuto_per_contenuto(r)
			fonti[r.titolo_ascii_contenuto] = fonti_contenuto_per_contenuto(r)
			etichette[r.titolo_ascii_contenuto] = etichette_contenuto_per_contenuto(r)
			if immagine_principale_del_contenuto(r):
				miniature[r.titolo_ascii_contenuto] = [
					url_immagine(immagine_principale_del_contenuto(r), 100),
					immagine_principale_del_contenuto(r).key.urlsafe(),
					]
			if immagini_vetrina_del_contenuto(r):
				vetrine[r.titolo_ascii_contenuto] = [[url_immagine(v, 100), v.key.urlsafe()] for v in immagini_vetrina_del_contenuto(r)]
		return {
					"oggetti_contenuto": oggetti,
					"stati_oggetti_contenuto": stati,
					"fonti_oggetti_contenuto": fonti,
					"etichette_oggetti_contenuto": etichette,
					"miniature_immagine_principale": miniature,
					"vetrine_oggetti_contenuto": vetrine,
				}
	else:
		return None

class GestoreHTML(webapp2.RequestHandler):
	template_dir = os.path.join(os.path.dirname(__file__), 'pagine')
	jinja_env = jinja2.Environment(
		loader = jinja2.FileSystemLoader(template_dir),
		autoescape = True,
		trim_blocks = True,
		#lstrip_blocks = True,
		)
	def scrivi(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def leggi(self,param):
		return self.request.get(param)
		
	def render_str(self, template, **params):
		return self.jinja_env.get_template(template).render(params)
		
	def render(self, template, **kw):
		self.scrivi(self.render_str(template, **kw))
	
	def servi_pagina(self, template, **kw):
		self.scrivi(self.render_str(template,**kw))

class PaginaContenuti(GestoreHTML):
	def get(self, criterio, valore):
		if criterio == "articolo":
			if valore == "":
				nuovo_articolo = True
				contenuto = None
			else:
				contenuto = estrai_contenuti(
									criterio = criterio,
									quanti = 1,
									valore = valore,
									)
				nuovo_articolo = False
			self.scrivi_articolo(nuovo_articolo, contenuto)
		else:
			self.scrivi_tops(criterio, valore)
		
	def scrivi_tops(self, criterio, valore = None):
		contenuti = estrai_contenuti(
						criterio = criterio,
						quanti = 10,
						valore = valore,
						)
		self.servi_pagina("tops.html",
						stile = "/statici/stili/tops.css",
						js = "/statici/funzioni_js/tops.js",
						contenuti = contenuti,
						etichette = tutte_etichette(),
						)
	
	def scrivi_articolo(self,
			nuovo_articolo,
			contenuto = None,
			):
		json_data = open("liste/liste.json").read()
		data = json.loads(json_data)
		self.servi_pagina("articolo.html",
							stile = "/statici/stili/articolo.css",
							js = "/statici/funzioni_js/articolo.js",
							contenuto = contenuto,
							nuovo_articolo = nuovo_articolo,
							upload_url = blobstore.create_upload_url('/upload'),
							etichette = tutte_etichette(),
							)

#class PaginaJsonPubblicazione(GestoreHTML):
	#def get(self, nome_pubblicazione):
		#pubb = estrai_pubblicazione(nome_pubblicazione)
		#outp = crea_json(pubb)
		#self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
		#self.scrivi(json.dumps(outp))

class PaginaChiSono(GestoreHTML):
	def get(self):
		in_costruzione = '<h1 style="color:red;font-family:monospace;">Pagina in costruzione</h1>'
		self.scrivi(in_costruzione)

class CaricaInserimento(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		adesso = questo_istante()
		titolo_contenuto = self.request.get("titolo_contenuto")
		titolo_ascii_contenuto = converti_unicode_in_ascii(titolo_contenuto)
		autore_contenuto = self.request.get("autore_contenuto")
		lista = tutti_titoli_ascii_contenuto()	# controllo se l'id è univoco
		if lista:
			while titolo_ascii_contenuto in lista:
				titolo_ascii_contenuto = titolo_ascii_contenuto + '-' + generatore_id_casuale()
		
		nomi_etichetta = self.request.get_all("nome_etichetta")
		for k in range(len(nomi_etichetta)):
			if nomi_etichetta[k] != "":
				etichetta = Etichetta()
				etichetta.titolo_ascii_contenuto = titolo_ascii_contenuto
				etichetta.nome_etichetta = nomi_etichetta[k]
				etichetta.nome_ascii_etichetta = converti_unicode_in_ascii(nomi_etichetta[k])
				etichetta.put()
		
		nomi_fonte = self.request.get_all("nome_fonte")
		links_fonte = self.request.get_all("link_fonte")
		for k in range(len(nomi_fonte)):
			if nomi_fonte[k] != "":
				fonte = FonteContenuto()
				fonte.titolo_ascii_contenuto = titolo_ascii_contenuto
				fonte.nome_fonte = nomi_fonte[k]
				fonte.nome_ascii_fonte = converti_unicode_in_ascii(nomi_fonte[k])
				fonte.link_fonte = links_fonte[k]
				fonte.put()
		
		stati_contenuto = self.request.get_all("stato_contenuto[]")
		for k in range(len(stati_contenuto)):
			stato = StatoContenuto()
			stato.titolo_ascii_contenuto = titolo_ascii_contenuto
			stato.stato_contenuto = stati_contenuto[k]
			stato.stato_ascii_contenuto = converti_unicode_in_ascii(stati_contenuto[k])
			stato.put()

		articolo = Articolo(
			).put()
		
		contenuto = Contenuto(
			parent = articolo,
			data_contenuto = adesso,
			autore_contenuto = autore_contenuto,
			autore_ascii_contenuto = converti_unicode_in_ascii(autore_contenuto),
			titolo_contenuto = titolo_contenuto,
			titolo_ascii_contenuto = titolo_ascii_contenuto,
			sottotitolo_contenuto = self.request.get("sottotitolo_contenuto"),
			corpo_contenuto = self.request.get("corpo_contenuto"),
			lingua_contenuto = "Italiano",
			).put()
		
		# sezione IMMAGINI
		categoria_immagine = self.request.get_all("categoria_immagine")
		tipo_immagine = self.request.get_all("tipo_immagine")
		nome_caricatore_immagine = self.request.get_all("nome_caricatore_immagine")
		nome_fonte_immagine = self.request.get_all("nome_fonte_immagine")
		link_fonte_immagine = self.request.get_all("link_fonte_immagine")
		descrizione_immagine = self.request.get_all("descrizione_immagine")
		blob_immagine = self.get_uploads("blob_immagine")
		
		numero_immagini = len(tipo_immagine)
		for k in range(numero_immagini):
			if categoria_immagine[k] == "principale":
				immagine = ImmaginePrincipale(parent = articolo)
			elif categoria_immagine[k] == "vetrina":
				immagine = ImmagineVetrina(parent = articolo)
			immagine.data_immagine = adesso
			immagine.tipo_immagine = tipo_immagine[k]
			immagine.nome_caricatore_immagine = nome_caricatore_immagine[k]
			immagine.nome_ascii_caricatore_immagine = converti_unicode_in_ascii(immagine.nome_caricatore_immagine)
			immagine.nome_fonte_immagine = nome_fonte_immagine[k]
			immagine.nome_ascii_fonte_immagine = converti_unicode_in_ascii(immagine.nome_fonte_immagine)
			if blob_immagine[k]:
				immagine.blob_immagine = blob_immagine[k].key()
			else:
				immagine.blob_immagine = None
			
			immagine.put()
		
		sleep(1)
		self.redirect('/')
		
class SingolaImmagine(GestoreHTML):
	def scrivi_singola_immagine(self,immagine,chiave):
		self.render("singola_immagine.html",
					immagine = immagine,
					chiave = chiave,
					blob = url_immagine(immagine, 500),
					)
		
	def get(self,chiave):
		immagine = revision = ndb.Key(urlsafe=chiave).get()
		self.scrivi_singola_immagine(immagine,chiave)
		
			
	def post(self,chiave):
		db.delete(chiave)
		sleep(1)
		self.redirect("/")
	
class CancellaDatastore(GestoreHTML):
	def get(self):
		ndb.delete_multi(Contenuto.query())
		sleep(1)
		self.redirect('/')

app = webapp2.WSGIApplication([
								('/visualizza/' + r'((?:[a-zA-Z0-9_-]+)*)', SingolaImmagine),
								('/chisono', PaginaChiSono),
								('/upload', CaricaInserimento),
								('/cancella', CancellaDatastore),
								(r'/([a-z]+)*/*([0-9a-zA-Z+#]*)', PaginaContenuti),
								], debug= True)

