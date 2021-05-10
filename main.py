# -*- coding: utf-8 -*-
# utilizzo delle funzioni da lettoreDataset
import lettoreDataset


#   restituisce una lista con malattie e sintomi
listaMalattie = lettoreDataset.acquisisciDataset('dataset/data.json')
#   visualizza in output le malattie
lettoreDataset.visualizzaMalattie(listaMalattie)

