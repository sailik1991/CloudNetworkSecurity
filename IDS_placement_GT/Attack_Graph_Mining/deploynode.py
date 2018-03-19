from bs4 import BeautifulSoup as bs
import requests

__author__ = "Sailik Sengupta"
__version__ = "1.0"
__email__ = "link2sailik [at] gmail [dot] com"

class cvss():
    scores = {}

    def get_cve_score(self, cve):
        link = 'https://nvd.nist.gov/vuln/detail/{}'.format(cve)
        r = requests.get(link)
        soup = bs(r.text, 'html5lib')

        try: b = float(str(soup.find_all('a',{'data-testid':'vuln-cvssv2-base-score-link'})).split('>')[1].split('<')[0].strip())
        except: b = -1.0
        try: i = float(str(soup.find_all('dd',{'data-testid':'vuln-cvssv2-impact-subscore'})).split('>')[1].split('<')[0].strip())
        except: i = -1.0
        try: e = float(str(soup.find_all('dd',{'data-testid':'vuln-cvssv2-exploitability-score'})).split('>')[1].split('<')[0].strip())
        except: e = -1.0

        return (b, i, e)

    def get_scores(self, cve_list):
        for cve in cve_list:
            self.scores[cve] = self.get_cve_score(cve)
        return self.scores

class deploynode():

    f = open('nessus.P','r')
    ip_n_vul_nodes = []
    vul_prop = {}
    vul_scores = {}

    def __init__(self):
        ''' Parse file to get vulnerability-node combinations '''
        for l in self.f:
            if 'vulProperty' in l:
                cve, tech, effect = l.split('(')[1].split(',')
                cve = cve.replace('\'','').strip()
                effect = effect.replace(').','').strip()
                self.vul_prop[cve] = (tech, effect)
            elif 'vulExists' in l:
                ip, cve, config = l.split('(')[1].split(',')
                ip = ip.replace('\'','').strip()
                cve = cve.replace('\'','').strip()
                self.ip_n_vul_nodes.append((ip,cve))

        #print(self.vul_prop)
        #print(self.ip_n_vul_nodes)

        ''' Obtain the cvss for the cve vulnerabilities '''
        c = cvss()
        self.vul_scores = c.get_scores(self.vul_prop.keys())
        
    def get_scores(self, cve):
        try:    return self.vul_scores[cve]
        except:
            print('CVSS values for {} could not be found'.format(cve)) 
            return (-1, -1, -1)
    def get_nodes(self):
        return self.ip_n_vul_nodes