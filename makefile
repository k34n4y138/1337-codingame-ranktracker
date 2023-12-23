# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: zmoumen <zmoumen@student.1337.ma>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/23 14:46:51 by zmoumen           #+#    #+#              #
#    Updated: 2023/12/23 14:58:03 by zmoumen          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #



ENVFOLDER = .venv
ENVPYTHON = $(ENVFOLDER)/bin/python3

GLOBALPYTHON = /usr/bin/python3

all: run

$(ENVFOLDER):
	@ ($(GLOBALPYTHON) -m venv $(ENVFOLDER)) || (echo "you don't have python3-venv installed"; exit 1;")
	$(ENVPYTHON) -m pip install --upgrade pip
	$(ENVPYTHON) -m pip install -r requirements.txt


run: $(ENVFOLDER)
	$(ENVPYTHON) rankscrap.py

freeze:
	@if [ ! -d $(ENVFOLDER) ]; then;echo "can't run freeze without virtual env";exit 1;fi
	$(ENVPYTHON) -m pip freeze > requirements.txt

clean:
	rm -rf $(ENVFOLDER)

rm-datafiles:
	rm -rf ranking-*.txt