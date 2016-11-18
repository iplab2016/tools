#!/usr/bin/python
#coding=utf-8
"""Get the information such as througput and hit rate 
from the files which is generated by ns-3 cache-app, 
they contains specific cache placement and policy information.

The format of the parsed files name:
    [0-3][0-3]-sram_size-dram_size(-xxx).txt 
"""
import sys
import os
import argparse


def init_parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', type=bool, 
                        choices=[True, False], default=False,
                        help="Print debug information") 
    parser.add_argument('-d', '--directory', type=str, default='./',
                        help="The directory containing parsed files") 
    parser.add_argument('-p', '--placement', type=int, choices=[0, 1, 2, 3], default='3',
                       help="Cache placement 0: cache in edge router, >0: betw or NDN")
    parser.add_argument('-a', '--algorithm', type=int, choices=[0, 1, 2, 3], default='3',
                       help="Cache algorithm 0: None, 1: LRU, 2: OPC, 3: HCaching") 
    return parser

def main():
    parser = init_parse_args()
    args = parser.parse_args()
    d = args.directory
    p = args.placement
    a = args.algorithm
    v = args.verbose

    if not os.path.isdir(d):
        parser.print_help()
        sys.exit(1)
    

    files = os.listdir(d)
    sram = [2.39, 4.78, 7.17, 9.5, 12]
    dram = [1, 2, 3, 4, 5]
    throughput = []
    hit_ratio = []
    print("Processing:")
    for i,e in enumerate(sram):
        askedfor = ""
        time = ""
        requests = ""
        hits = ""

        prefix = "%d%d-%s-%s" % (p, a, str(e), str(dram[i]))
        result = [f for f in files if f.find(prefix) >= 0]
        if len(result) == 1:
            path = os.path.join(d, result[0])
            pass
        elif len(result) > 1:
            print("There are one more files, %s" % result)
            exit(1)
        else:
            print("There is not filename including the prefix %s" % prefix)
            exit(1)
        print("\tParsing %s" % path)          
        with open(path) as f:
            line = f.readline()
            while line:
               s = "askedfor="
               start = line.find(s)
               if start >=0:
                   end = line.find(",", start+len(s))
                   if end >= 0:
                       askedfor = line[start+len(s): end]
                       if v: print("askedfor = %s" % askedfor)
                       line = f.readline()
                       continue
                  
               s = "Overall service time: ms:"
               start = line.find(s)
               if start >=0:
                   end = line.find(" ps", start+len(s))
                   if end >= 0:
                       time = line[start+len(s): end]
                       if v: print("time = s" % time)
                       line = f.readline()
                       continue
               
               
               s = "Cache requests: "
               start = line.find(s)
               if start >=0:
                   s2 = " hits: "
                   end = line.find(s2, start+len(s))
                   if end >= 0:
                       requests = line[start+len(s): end]
                       if v: print("requests = %s" % requests)
                       start = end
                       end = line.find(" stored_packets", start+len(s2))
                       hits = line[start+len(s2): end]
                       if v: print ("hits = %s" % hits)
                       line = f.readline()
                       continue
               line = f.readline()
        if (int(askedfor) >= 0 and int(time) >= 0 and
           int(requests) >=0 and int(hits)) >0:
           throughput.append("%.2f" % (float(askedfor)*1500*8*1000/float(time)/1024/1024/1024))
           hit_ratio.append("%.2f" % (float(hits)*100/float(requests)))
        else:
           print("Error:askedfor = %s, time = %s, requests = %s, hits = %s" %
                 (askedfor, time, requests, hits))
           exit(1)
    
    print("\n\nResults:\n\tsram = %s" % sram)
    throughput = [float(e) for e in throughput]
    hit_ratio = [float(e) for e in hit_ratio]
    print("\tthroughput = %s" % throughput)
    print("\thit_ratio = %s" % hit_ratio)
       
if __name__ == '__main__':
    sys.exit(main())
