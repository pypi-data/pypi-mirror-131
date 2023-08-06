#! /usr/bin/env python

import xml.etree.ElementTree as et
from os import path as p

d = p.dirname(p.abspath(__file__))
quran = p.join(d, "source/quran.xml")
terjemahan = p.join(d, "source/terjemahan.xml")
tafsir = p.join(d, "source/tafsir.xml")


class AlQuran():


    def __init__(self):
        self.quran = et.parse(quran)
        self.terjemahan = et.parse(terjemahan)
        self.tafsir = et.parse(tafsir)
    

    def Ayat(self, id_surat, id_ayat):
        surat = self.quran.getroot()
        surat = surat.find(f".//sura[@index='{id_surat}']")
        ayat = surat.find(f".//aya[@index='{id_ayat}']")
        ayat = ayat.get("text")
        jml_ayat = surat.findall("aya")
        jml_ayat = len(jml_ayat)
        return ayat, jml_ayat


    def Terjemahan(self, id_surat, id_ayat):
        terjemahan = self.terjemahan.getroot()
        terjemahan = terjemahan.find(f".//sura[@index='{id_surat}']")
        ayat = terjemahan.find(f".//aya[@index='{id_ayat}']")
        ayat = ayat.get("text")
        return ayat


    def Tafsir(self, id_surat, id_ayat):
        tafsir = self.tafsir.getroot()
        tafsir = tafsir.find(f".//sura[@index='{id_surat}']")
        ayat = tafsir.find(f".//aya[@index='{id_ayat}']")
        ayat = ayat.get("text")
        return ayat
