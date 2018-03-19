import sys
from deploynode import *

__author__ = "Sailik Sengupta"
__version__ = "1.0"
__email__ = "link2sailik [at] gmail [dot] com"

def main(k):
    s = ''
    dn = deploynode()
    nodes = dn.get_nodes()
    s += '{}\n{}\n'.format(len(nodes), k)
    
    s_d = ''
    s_a = ''
    for n in nodes:
        cve = n[1]
        b, i, e = dn.get_scores(cve)
        if b > -1 and i > -1 and e > -1:
            s_d += '0 {}\n'.format(-1*i)
            s_a += '{} {}\n'.format(-1*e,b)

    s += s_d.strip()
    s += '\n{}'.format(s_a)
    
    f = open('BSSG_input.txt','r')
    f.write(s.strip())
    f.close()

if __name__ == '__main__':
    main(sys.argv[1])

