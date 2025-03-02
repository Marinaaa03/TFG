PYTHON := python3

WS := web_scrapping.py
IKEA := web_scrapping_ikea.py
CONFORAMA := web_scrapping_conforama.py
APP := app.py
JSON := resultados.json

ws0: $(WS)
	$(PYTHON) $(WS)

ws1: $(IKEA)
	$(PYTHON) $(IKEA)

ws2: $(CONFORAMA)
	$(PYTHON) $(CONFORAMA)

web: $(APP)
	$(PYTHON) $(APP)

app:
	flask run --host=0.0.0.0 --port=5000

clean:
	rm -f $(JSON)
