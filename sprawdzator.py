import requests

class Request():
	'''
	Klasa odpowiadająca za zbieranie danych ze strony.
	'''
	def __init__(self):
		'''
		Deklaruję zmienną dla klasy.
		'''
		self.url = r'https://w43.sfgame.net/req.php?req=0-0tj74j71185Hw1m62ubgJq2WZrleqd11eVcOhgU3DzaEOXqGLGDq63ao04CbIPRzhL1rq99IAO9ineYK2wY_5j6SyW5VrYH-svJQ==&rnd=0.08269227&c=278'
	
	def get_data(self) -> list:
		'''
		Metoda do pobrania danych ze strony i zesplittowania na pojedyncze elementy.
		Zwraca listę.
		'''
		r = requests.get(self.url)
		response = str(r.content.decode('utf-8'))
		return response

class FormatData():
	'''
	Klasa do obrabiania danych.
	'''

	def __extract_nicks(self, response: list) -> list:
		'''
		Metoda do wyciągania nicków.
		Zwraca listę nicków.
		'''
		nicks = response.split('&othergroupmember.s:')[1]
		nicks = nicks.split('&othergrouprank:')[0]
		nicks = nicks.split(',')
		return nicks

	def __extract_levels(self, nicks: list, response: list) -> list:
		'''
		Metoda do wyciągania leveli.
		Zwraca listę leveli.
		'''
		response = response.split('/')
		players_count = 64 + len(nicks)
		levels = response[64:players_count]
		return levels

	def __format_levels(self, levels: list) -> list:
		'''
		Metoda formatująca levele.
		Zwraca listę z levelami w formacie liczbowym.
		'''
		for counter in range(len(levels)):
			if len(levels[counter]) == 4:
				levels[counter] = int(levels[counter][1:])
			else:
				levels[counter] = int(levels[counter])
		return levels

	def __consolidate_data(self, nicks: list, levels: list) -> dict:
		'''
		Metoda do konsolidacji nicków z levelami.
		'''
		return dict(zip(nicks, levels))


	def format(self, response: list) -> dict:
		'''
		Główna metoda klasy. 
		Zwraca skonsolidowany słownik nicków i leveli.
		'''
		nicks = self.extract_nicks(response)
		levels = self.extract_levels(nicks, response)
		levels = self.format_levels(levels)
		output =  self.consolidate_data(nicks, levels)
		return output
	
if __name__ == "__main__":
	
	formatter = FormatData()
	requestor = Request()

	print(formatter.format(requestor.get_data()))
