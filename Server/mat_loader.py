# !/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
""" Loads different Menus from ETH and UZH and stores them in MongoDB"""
import json
from html.parser import HTMLParser
import json
import requests
from html2json import collect

itet = """
<ul class="nice-menu nice-menu-down nice-menu-menu-studiumsunterlagen-itet nice-menus-processed sf-js-enabled" id="nice-menu-2">
<li class="menu-660 menuparent  menu-path-studium-unterlagen first odd"><a href="/studium/unterlagen" title="">Basisjahr</a>

<ul style="display: none; visibility: hidden;">
<li class="menu-659 menu-path-studium-unterlagen-23 first odd "><a href="/studium/unterlagen/23" title="">Analysis I &amp; II</a></li>
<li class="menu-661 menu-path-studium-unterlagen-24  even "><a href="/studium/unterlagen/24" title="">Netzw. &amp; Schaltungen I &amp; II</a></li>
<li class="menu-752 menu-path-studium-unterlagen-86  odd "><a href="/studium/unterlagen/86" title="">Informatik I &amp; II</a></li>
<li class="menu-747 menu-path-studium-unterlagen-84  even "><a href="/studium/unterlagen/84" title="">Digitaltechnik</a></li>
<li class="menu-750 menu-path-studium-unterlagen-85  odd "><a href="/studium/unterlagen/85" title="">Lineare Algebra</a></li>
<li class="menu-746 menu-path-studium-unterlagen-83  even "><a href="/studium/unterlagen/83" title="">Technische Mechanik</a></li>
<li class="menu-753 menu-path-studium-unterlagen-87  odd "><a href="/studium/unterlagen/87" title="">Komplexe Analysis</a></li>
<li class="menu-754 menu-path-studium-unterlagen-88  even last"><a href="/studium/unterlagen/88" title="">Physik I</a></li>

</ul></li>
<li class="menu-748 menuparent  menu-path-studium-unterlagen  even"><a href="/studium/unterlagen" title="">3. Semester</a><ul style="display: none; visibility: hidden;"><li class="menu-861 menu-path-studium-unterlagen-93 first odd "><a href="/studium/unterlagen/93" title="">Analysis III</a></li>
<li class="menu-858 menu-path-studium-unterlagen-90  even "><a href="/studium/unterlagen/90" title="">Diskrete Mathematik</a></li>
<li class="menu-863 menu-path-studium-unterlagen-95  odd "><a href="/studium/unterlagen/95" title="">Felder &amp; Komponenten I</a></li>
<li class="menu-1505 menu-path-studium-unterlagen-171  even "><a href="/studium/unterlagen/171" title="">Halbleiter-Schaltungstechnik</a></li>
<li class="menu-859 menu-path-studium-unterlagen-91  odd "><a href="/studium/unterlagen/91" title="">Physik II</a></li>
<li class="menu-860 menu-path-studium-unterlagen-92  even "><a href="/studium/unterlagen/92" title="">Signal- &amp; Systemtheorie I</a></li>
<li class="menu-862 menu-path-studium-unterlagen-94  odd last"><a href="/studium/unterlagen/94" title="">Technische Informatik I</a></li>
</ul></li>
<li class="menu-864 menuparent  menu-path-studium-unterlagen  odd"><a href="/studium/unterlagen" title="">4. Semester</a><ul style="display: none; visibility: hidden;"><li class="menu-1506 menu-path-studium-unterlagen-172 first odd "><a href="/studium/unterlagen/172" title="">Elektromagnetische Felder &amp; Wellen</a></li>
<li class="menu-869 menu-path-studium-unterlagen-101  even "><a href="/studium/unterlagen/101" title="">Felder &amp; Komponenten II</a></li>
<li class="menu-870 menu-path-studium-unterlagen-102  odd "><a href="/studium/unterlagen/102" title="">Halbleiterbauelemente</a></li>
<li class="menu-865 menu-path-studium-unterlagen-97  even "><a href="/studium/unterlagen/97" title="">Numerische Methoden</a></li>
<li class="menu-868 menu-path-studium-unterlagen-100  odd "><a href="/studium/unterlagen/100" title="">Signal- &amp; Systemtheorie II</a></li>
<li class="menu-867 menu-path-studium-unterlagen-99  even "><a href="/studium/unterlagen/99" title="">Technische Informatik II</a></li>
<li class="menu-866 menu-path-studium-unterlagen-98  odd last"><a href="/studium/unterlagen/98" title="" class="active">Wahrscheinl.-Th &amp; Statistik</a></li>
</ul></li>
<li class="menu-871 menuparent  menu-path-studium-unterlagen  even"><a href="/studium/unterlagen" title="">5. Semester</a><ul style="display: none; visibility: hidden;"><li class="menu-1508 menu-path-studium-unterlagen-174 first odd "><a href="/studium/unterlagen/174" title="">Advanced Waves</a></li>
<li class="menu-892 menu-path-studium-unterlagen-125  even "><a href="/studium/unterlagen/125" title="">Analog Integrated Circuits</a></li>
<li class="menu-888 menu-path-studium-unterlagen-121  odd "><a href="/studium/unterlagen/121" title="">Biosensors &amp; Bioelectronics</a></li>
<li class="menu-874 menu-path-studium-unterlagen-106  odd "><a href="/studium/unterlagen/106" title="">Communication Electronics</a></li>
<li class="menu-876 menu-path-studium-unterlagen-108  even "><a href="/studium/unterlagen/108" title="">Diskrete Ereignissysteme</a></li>
<li class="menu-878 menu-path-studium-unterlagen-110  odd "><a href="/studium/unterlagen/110" title="">Einführung in die Biomed. Technik I</a></li>
<li class="menu-882 menu-path-studium-unterlagen-114  even "><a href="/studium/unterlagen/114" title="">Elektrische Energiesysteme</a></li>
<li class="menu-1507 menu-path-studium-unterlagen-173  odd "><a href="/studium/unterlagen/173" title="">High-Speed Signal Propagation</a></li>
<li class="menu-873 menu-path-studium-unterlagen-105  even "><a href="/studium/unterlagen/105" title="">Kommunikationssysteme</a></li>
<li class="menu-881 menu-path-studium-unterlagen-113  odd "><a href="/studium/unterlagen/113" title="">Leistungselektronik</a></li>
<li class="menu-875 menu-path-studium-unterlagen-107  even "><a href="/studium/unterlagen/107" title="">Leitungen &amp; Filter</a></li>
<li class="menu-880 menu-path-studium-unterlagen-112  odd "><a href="/studium/unterlagen/112" title="">Microsystems Technology</a></li>
<li class="menu-877 menu-path-studium-unterlagen-109  even "><a href="/studium/unterlagen/109" title="">Regelsysteme</a></li>
<li class="menu-879 menu-path-studium-unterlagen-111  odd "><a href="/studium/unterlagen/111" title="">Solid State Electronics</a></li>
<li class="menu-872 menu-path-studium-unterlagen-104  even last"><a href="/studium/unterlagen/104" title="">Zeitdiskr. &amp; statist. Signalverarbeitung</a></li>
</ul></li>
<li class="menu-883 menuparent  menu-path-studium-unterlagen  odd"><a href="/studium/unterlagen" title="">6. Semester</a><ul style="display: none; visibility: hidden;"><li class="menu-1968 menu-path-studium-unterlagen-160 first odd "><a href="/studium/unterlagen/160" title="">Advanced Electromagnetic Waves</a></li>
<li class="menu-884 menu-path-studium-unterlagen-117  even "><a href="/studium/unterlagen/117" title="">Antennas &amp; Propagations</a></li>
<li class="menu-890 menu-path-studium-unterlagen-123  odd "><a href="/studium/unterlagen/123" title="">Communication &amp; Detection Theory</a></li>
<li class="menu-885 menu-path-studium-unterlagen-118  even "><a href="/studium/unterlagen/118" title="">Communication Networks</a></li>
<li class="menu-889 menu-path-studium-unterlagen-122  odd "><a href="/studium/unterlagen/122" title="">Einführung in die Biomed. Technik II</a></li>
<li class="menu-891 menu-path-studium-unterlagen-124  even "><a href="/studium/unterlagen/124" title="">Eingebettete Systeme</a></li>
<li class="menu-897 menu-path-studium-unterlagen-130  odd "><a href="/studium/unterlagen/130" title="">Elektrische Antriebssysteme I</a></li>
<li class="menu-895 menu-path-studium-unterlagen-128  even "><a href="/studium/unterlagen/128" title="">Hochspannungstechnik</a></li>
<li class="menu-896 menu-path-studium-unterlagen-129  odd "><a href="/studium/unterlagen/129" title="">Mechatronik</a></li>
<li class="menu-3590 menu-path-taxonomy-term-215  even "><a href="/study-materials/neural-systems" title="">Neural Systems</a></li>
<li class="menu-1969 menu-path-studium-unterlagen-225  odd "><a href="/studium/unterlagen/225" title="">Optics and Photonics</a></li>
<li class="menu-886 menu-path-studium-unterlagen-119  even "><a href="/studium/unterlagen/119" title="">Optoelectronics &amp; Optical Communications</a></li>
<li class="menu-4566 menu-path-studium-unterlagen-230  odd "><a href="/studium/unterlagen/230" title="">Power Semiconductors</a></li>
<li class="menu-894 menu-path-studium-unterlagen-127  even "><a href="/studium/unterlagen/127" title="">Quantenelektronik</a></li>
<li class="menu-893 menu-path-studium-unterlagen-126  odd "><a href="/studium/unterlagen/126" title="">Regelsysteme II</a></li>
<li class="menu-887 menu-path-studium-unterlagen-120  even last"><a href="/studium/unterlagen/120" title="">VLSI I: von Architektur zu hochintegrierter Schaltung &amp; FPGA</a></li>
</ul></li>
<li class="menu-900 menuparent  menu-path-studium-unterlagen active-trail  even last"><a href="/studium/unterlagen" title="">Master</a><ul style="display: none; visibility: hidden;"><li class="menu-902 menu-path-studium-unterlagen-66 first odd "><a href="/studium/unterlagen/66" title="">Biomedical Engineering</a></li>
<li class="menu-901 menu-path-studium-unterlagen-132  even "><a href="/studium/unterlagen/132" title="">Electrical Engineering &amp; Information Technology</a></li>
<li class="menu-903 menu-path-studium-unterlagen-68  odd "><a href="/studium/unterlagen/68" title="">Energy Science and Technology</a></li>
<li class="menu-904 menu-path-studium-unterlagen-67  even "><a href="/studium/unterlagen/67" title="">Micro and Nanosystems</a></li>
<li class="menu-905 menu-path-studium-unterlagen-65  odd last"><a href="/studium/unterlagen/65" title="">Robotics, Systems and Control</a></li>
</ul></li>
</ul>
"""

mavt = """

<li class="menu-638 menuparent  menu-path-studium-unterlagen first odd"><a href="/studium/unterlagen" title="">Basisjahr</a>
<ul style="display: none; visibility: hidden;"><li class="menu-637 menu-path-studium-unterlagen-10 first odd "><a href="/studium/unterlagen/10" title="">Analysis I &amp; II</a></li>

<li class="menu-639 menu-path-studium-unterlagen-11  even "><a href="/studium/unterlagen/11" title="">Mechanik I &amp; II</a></li>
<li class="menu-640 menu-path-studium-unterlagen-13  odd "><a href="/studium/unterlagen/13" title="">Lineare Algebra I &amp; II</a></li>
<li class="menu-641 menu-path-studium-unterlagen-14  even "><a href="/studium/unterlagen/14" title="">Werkstoffe &amp; Fertigung I &amp; II</a></li>
<li class="menu-642 menu-path-studium-unterlagen-15  odd "><a href="/studium/unterlagen/15" title="">Chemie</a></li>
<li class="menu-645 menu-path-studium-unterlagen-18  even "><a href="/studium/unterlagen/18" title="">CAD</a></li>
<li class="menu-643 menu-path-studium-unterlagen-16  odd "><a href="/studium/unterlagen/16" title="">Informatik I</a></li>
<li class="menu-644 menu-path-studium-unterlagen-17  even last"><a href="/studium/unterlagen/17" title="">Maschinenelemente &amp; IP</a></li>
</ul></li>
<li class="menu-646 menuparent  menu-path-studium-unterlagen  even"><a href="/studium/unterlagen" title="">3. Semester</a><ul style="display: none; visibility: hidden;"><li class="menu-647 menu-path-studium-unterlagen-20 first odd "><a href="/studium/unterlagen/20" title="">Analysis III</a></li>
<li class="menu-648 menu-path-studium-unterlagen-21  even "><a href="/studium/unterlagen/21" title="">Mechanik III</a></li>
<li class="menu-691 menu-path-studium-unterlagen-29  odd "><a href="/studium/unterlagen/29" title="">Dimensionieren I</a></li>
<li class="menu-687 menu-path-studium-unterlagen-25  even "><a href="/studium/unterlagen/25" title="">Physik I &amp; II (MAVT)</a></li>
<li class="menu-689 menu-path-studium-unterlagen-27  odd "><a href="/studium/unterlagen/27" title="">Regelungstechnik I</a></li>
<li class="menu-688 menu-path-studium-unterlagen-26  even last"><a href="/studium/unterlagen/26" title="">Thermodynamik I</a></li>
</ul></li>
<li class="menu-692 menuparent  menu-path-studium-unterlagen  odd"><a href="/studium/unterlagen" title="">4. Semester</a><ul style="display: none; visibility: hidden;"><li class="menu-690 menu-path-studium-unterlagen-28 first odd "><a href="/studium/unterlagen/28" title="">Elektrotechnik I</a></li>
<li class="menu-693 menu-path-studium-unterlagen-31  even "><a href="/studium/unterlagen/31" title="">Fluiddynamik I</a></li>
<li class="menu-695 menu-path-studium-unterlagen-25  odd "><a href="/studium/unterlagen/25" title="">Physik I &amp; II (MAVT)</a></li>
<li class="menu-694 menu-path-studium-unterlagen-32  even "><a href="/studium/unterlagen/32" title="">Thermodynamik II</a></li>
<li class="menu-696 menuparent  menu-path-studium-unterlagen  odd last"><a href="/studium/unterlagen" title="">Wahlfächer</a><ul style="display: none; visibility: hidden;"><li class="menu-3649 menu-path-studium-unterlagen-224 first odd "><a href="/studium/unterlagen/224" title="">Computational Methods for Engineering I</a></li>
<li class="menu-698 menu-path-studium-unterlagen-35  even "><a href="/studium/unterlagen/35" title="">Dimensionieren II</a></li>
<li class="menu-700 menu-path-studium-unterlagen-37  odd "><a href="/studium/unterlagen/37" title="">Fertigungstechnik</a></li>
<li class="menu-697 menu-path-studium-unterlagen-34  even "><a href="/studium/unterlagen/34" title="">Introduction to Chemical Engineering</a></li>
<li class="menu-703 menu-path-studium-unterlagen-40  odd "><a href="/studium/unterlagen/40" title="">Introduction to Quantum Mechanics</a></li>
<li class="menu-704 menu-path-studium-unterlagen-41  even last"><a href="/studium/unterlagen/41" title="">Regelungstechnik II</a></li>
</ul></li>
</ul></li>
<li class="menu-705 menuparent  menu-path-studium-unterlagen active-trail  even"><a href="/studium/unterlagen" title="">5. Semester</a><ul style="display: none; visibility: hidden;"><li class="menu-706 menu-path-studium-unterlagen-44 first odd "><a href="/studium/unterlagen/44" title="">Fluiddynamik II</a></li>
<li class="menu-707 menu-path-studium-unterlagen-45  even "><a href="/studium/unterlagen/45" title="">Thermodynamik III</a></li>
<li class="menu-708 menuparent  menu-path-studium-unterlagen  odd"><a href="/studium/unterlagen" title="">Wahlfächer</a><ul style="display: none; visibility: hidden;"><li class="menu-714 menu-path-studium-unterlagen-52 first odd "><a href="/studium/unterlagen/52" title="">Einführung in die Verfahrenstechnik</a></li>
<li class="menu-699 menu-path-studium-unterlagen-36  even "><a href="/studium/unterlagen/36" title="">Elektrotechnik II</a></li>
<li class="menu-713 menu-path-studium-unterlagen-51  odd "><a href="/studium/unterlagen/51" title="">Managerial Economics</a></li>
<li class="menu-709 menu-path-studium-unterlagen-47  even "><a href="/studium/unterlagen/47" title="">Signals &amp; Systems</a></li>
<li class="menu-711 menu-path-studium-unterlagen-49  odd "><a href="/studium/unterlagen/49" title="">Stochastik</a></li>
<li class="menu-712 menu-path-studium-unterlagen-50  even "><a href="/studium/unterlagen/50" title="">Stofftransport</a></li>
<li class="menu-710 menu-path-studium-unterlagen-48  odd "><a href="/studium/unterlagen/48" title="">Systemmodellierung</a></li>
<li class="menu-3648 menu-path-studium-unterlagen-223  even "><a href="/studium/unterlagen/223" title="">Computational Methods for Engineering II</a></li>
<li class="menu-3888 menu-path-studium-unterlagen-228  odd last"><a href="/studium/unterlagen/228" title="">Leichtbau</a></li>
</ul></li>
<li class="menu-743 menuparent  menu-path-studium-unterlagen active-trail  even last"><a href="/studium/unterlagen" title="">Laborpraktika</a><ul style="display: none; visibility: hidden;"><li class="menu-745 menu-path-studium-unterlagen-60 first odd "><a href="/studium/unterlagen/60" title="">Nicht Physik-Praktika</a></li>
<li class="menu-744 menu-path-studium-unterlagen-59  even last"><a href="/studium/unterlagen/59" title="">Physikpraktika</a></li>
</ul></li>
</ul></li>
<li class="menu-728 menuparent  menu-path-studium-unterlagen  odd"><a href="/studium/unterlagen" title="">Fokus</a><ul style="display: none; visibility: hidden;"><li class="menu-736 menu-path-samivethzch-studium-unterlagen-71 first odd "><a href="https://www.amiv.ethz.ch/studium/unterlagen/71" title="">Biomedical Engineering</a></li>
<li class="menu-737 menu-path-samivethzch-studium-unterlagen-72  even "><a href="https://www.amiv.ethz.ch/studium/unterlagen/72" title="">Energy, Flows &amp; Processes</a></li>
<li class="menu-738 menu-path-samivethzch-studium-unterlagen-73  odd "><a href="https://www.amiv.ethz.ch/studium/unterlagen/73" title="">Management, Technology, and Economics</a></li>
<li class="menu-739 menu-path-samivethzch-studium-unterlagen-75  even "><a href="https://www.amiv.ethz.ch/studium/unterlagen/75" title="">Manufacturing Science</a></li>
<li class="menu-740 menu-path-samivethzch-studium-unterlagen-76  odd "><a href="https://www.amiv.ethz.ch/studium/unterlagen/76" title="">Mechatronics</a></li>
<li class="menu-741 menu-path-samivethzch-studium-unterlagen-77  even "><a href="https://www.amiv.ethz.ch/studium/unterlagen/77" title="">Microsystems and Nanotechnology</a></li>
<li class="menu-742 menu-path-samivethzch-studium-unterlagen-78  odd last"><a href="https://www.amiv.ethz.ch/studium/unterlagen/78" title="">Structure Mechanics</a></li>
</ul></li>
<li class="menu-727 menuparent  menu-path-studium-unterlagen  even last"><a href="/studium/unterlagen" title="">Master</a><ul style="display: none; visibility: hidden;"><li class="menu-732 menu-path-samivethzch-studium-unterlagen-66 first odd "><a href="https://www.amiv.ethz.ch/studium/unterlagen/66" title="">Biomedical Engineering</a></li>
<li class="menu-734 menu-path-samivethzch-studium-unterlagen-68  even "><a href="https://www.amiv.ethz.ch/studium/unterlagen/68" title="">Energy Science and Technology</a></li>
<li class="menu-729 menu-path-samivethzch-studium-unterlagen-63  odd "><a href="https://www.amiv.ethz.ch/studium/unterlagen/63" title="">Mechanical Engineering</a></li>
<li class="menu-733 menu-path-samivethzch-studium-unterlagen-67  even "><a href="https://www.amiv.ethz.ch/studium/unterlagen/67" title="">Micro and Nanosystems</a></li>
<li class="menu-735 menu-path-samivethzch-studium-unterlagen-69  odd "><a href="https://www.amiv.ethz.ch/studium/unterlagen/69" title="">Nuclear Engineering</a></li>
<li class="menu-730 menu-path-samivethzch-studium-unterlagen-64  even "><a href="https://www.amiv.ethz.ch/studium/unterlagen/64" title="">Process Engineering</a></li>
<li class="menu-731 menu-path-samivethzch-studium-unterlagen-65  odd last"><a href="https://www.amiv.ethz.ch/studium/unterlagen/65" title="">Robotics, Systems and Control</a></li>
</ul></li>
"""


class UlHtmlParser(HTMLParser):
    """ Simple HTML Parser that parses the content of the RSS Feed obtained from UZH API """

    def setDep(self, dep):
        self.dep = dep

    def clearState(self):
        self.semesters = {}
        self.currentTag = ""
        self.inUl = False
        self.inSemester = False
        self.currentSemester = []
        self.currFach = {};
        self.fachList =[]

    def getAll(self):
        self.fachList.append(self.currFach)
        return self.fachList

    def printAll(self):
        for fach in self.fachList:
            print(fach)

    def handle_starttag(self, tag, attrs):

        if (tag == "ul"):
            self.inUl = True
            for attName, attValue in attrs:
                if(attName == "class" and "nice-menu" in attValue):
                    self.inUl = True
                    self.inSemester = False
                    return
            self.inSemester = True
        if(tag=="li" and self.inSemester):

            if(self.currFach is not None):
                self.fachList.append(self.currFach)

            self.currFach = {}

        if(tag == "a" and self.inSemester):

            self.currFach["sem"] = self.currentSemester
            self.currFach["dep"] = self.dep
            for attName, attValue in attrs:
                if(attName == "href"):
                    print(attValue)
                    self.currFach["id"] = attValue.split("/")[-1]



    def handle_endtag(self, tag):
        if (tag == "ul"):
            if(self.inSemester == True):
                self.inSemester = False
            else:
             self.inUl = False

        elif (tag == "td"):
            self.tdCounter = self.tdCounter + 1

    def handle_data(self, data):

        if (self.trimData(data) == ""):
            return
        if(self.inUl):
            if(not self.inSemester):
                self.currentSemester = self.mapSemester(data)
            else:
                self.currFach["name"] = self.trimData(data)
                print(self.trimData(data))


    def trimData(self, data):
        return data.replace("\n","").strip();

    def mapSemester(self, string):
        f = self.trimData(string)
        if(f == "Basisjahr"):
            return ["1","2"]
        else:
            arr = [];
            for i in range(1,5):
                if(str(i) in f):
                    arr.append(str(i))
            if(len(arr) != 0):
                return arr;
            else:
                return ["5+"];

class GrabDocsParser(HTMLParser):
    """ Simple HTML Parser that parses the content of the RSS Feed obtained from UZH API """

    def clearState(self):
        self.fileEntry = {'links':[]}

        self.inTable = False
        self.inTr = False
        self.foundCaption = False
        self.currTable = "";
        self.tables = {}
        self.inCaption = False
        self.inBody = False
        self.inTitle = False
        self.inEntity = False

        self.inAuthor = False
        self.inA = False
        self.currLink = ""
        self.inFiles = False

    def handle_starttag(self, tag, attrs):
        if(tag == "table"):
            print("in table")
            self.inTable  = True

        if(tag=="caption"):
            self.inCaption = True

            self.foundCaption = True
        if(tag == "tbody"):
            self.inBody = True

        if(tag == "tr"):
            self.inTr = True

        if(tag == "td") :
            if("title" in str(attrs)):
                self.inTitle = True
            if("entity-id-2" in str(attrs)):
                self.inEntity = True
                return
            if ("entity-id-1" in str(attrs)):
                self.inFiles = True
                return

            if ("entity-id-3" in str(attrs)):
                #Year
                return
            if("entity-id" in str(attrs)):
                self.inAuthor = True

        if(tag == "a"):
            self.inA = True
            for e,v in attrs:
                if(e == 'href' and "legacy" in v):
                    self.currLink = v
        """  if (tag == "a" and self.inSemester):
            self.currFach["sem"] = self.currentSemester
            self.currFach["dep"] = self.dep
            for attName, attValue in attrs:
                if (attName == "href"):
                    print(attValue)
                    self.currFach["id"] = attValue.split("/")[-1]"""

    def handle_endtag(self, tag):

        if(tag == "tr"):
            self.inTr = False
            self.tables[self.currTable].append(self.fileEntry)
            self.fileEntry = {'links': []}
            print(self.tables)

        if(tag == "tbody"):
            self.inBody = False
        if(tag=="caption"):
            self.inCaption = False

        if(tag == "table"):
            print("end table")
            self.inTable  = False

        if (tag == "td"):
            self.inTitle = False
            self.inEntity =False
            self.inAuthor = False
            self.inFiles = False
        if(tag == "a"):
            self.inA = False
    def handle_data(self, data):


        if(self.currTable != ""):
            if(self.currTable not in self.tables):
                self.tables[self.currTable] = []
            self.currTableObj =  self.tables[self.currTable]

        if(self.inCaption):
            self.currTable = self.trimData(data)
            print(data)
            print(self.tables)
        dat = self.trimData(data);
        if(self.inTitle):
            print("in Title:" + str(self.trimData(data)))
            self.fileEntry['title'] = dat
        if(self.inEntity):
            print("in Entity:" + str(self.trimData(data)))
            self.fileEntry['year'] = dat
        if(self.inAuthor):
            print("in Author:" + str(self.trimData(data)))
            self.fileEntry['author'] = dat
        if(self.inFiles and self.inA):
            print("in Files:" + str(self.trimData(data)))
            print(self.currLink)
            self.fileEntry['links'].append((dat ,self.currLink))
            print(self.fileEntry)


    def trimData(self, data):
        return data.replace("\n", "").strip()

    def mapSemester(self, string):
        f = self.trimData(string)
        if (f == "Basisjahr"):
            return ["1", "2"]
        else:
            arr = [];
            for i in range(1, 5):
                if (str(i) in f):
                    arr.append(str(i))
            if (len(arr) != 0):
                return arr;
            else:
                return ["5+"];


def grabUrl(path):

    headers = {
        'User-Agent': 'PostmanRuntime/7.17.1',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    cookies = {'has_js':'1; SSESSa81176e9c9c8a1c8cb0fb5cc0d030a97=4V2WXqEcN0d3AogmBZ1yME0JN4qXseHtMYNt7euMBp4'}
    req = requests.get(
        url=path,
        params=None, headers=headers, cookies=cookies)

    parser = GrabDocsParser()
    parser.clearState()
    parser.feed(req.text)
    print("-------------------")
    return parser.tables


if __name__ == '__main__':

    masters = ["Biomedical Engineering", "Information Techn", "Energy Science", "Micro and", "Robotics", "Mechanical Engineering", "Micro and Nano", "Nuclear Engineering", "Process Engineering"]


    parser = UlHtmlParser()
    parser.setDep("mavt")
    parser.clearState()
    parser.feed(mavt)
    parser.printAll()
    for fach in parser.getAll():
        if(fach == {}):
            continue
        print(fach)
        print("going to grab url")
        url = "https://legacy.amiv.ethz.ch/studium/unterlagen/" + str(fach["id"])
        print(url)

        vlsg = fach['name']
        tables = grabUrl(url)
        for entry in tables:

            list = []
            for element in tables[entry]:
                if ('title' in element):
                    print(element)
                    list.append(element)
            tables[entry] = list
        tables['info'] = fach

        tables['master'] = False
        for m in masters:
            if m in vlsg:
                print("found master: " + str(vlsg))
                tables['master'] = True

        filename = "mavt-" + vlsg
        with open('res/' + filename + ".json", 'w') as outfile:
            text = json.dumps(tables, sort_keys=True, indent=4)
            outfile.write(text)









def getEntries():
    list = []
    #for conn in connDefs:
    #    for entry in getEntriesForConn(conn):
    #        list.append(entry)


def getEntriesForConn(connectionInfo):
    headers = {
        'User-Agent': 'PostmanRuntime/7.17.1',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': 'ethz.ch',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }


    sem = connectionInfo.semester
    id = connectionInfo.id
    depart = connectionInfo.department

    path = "https://legacy.amiv.ethz.ch/studium/unterlagen" + str(id)

    req = requests.get(
        url=path,
        params=None, headers=headers)

    return parser.parseAndGetMenus(req.text)

