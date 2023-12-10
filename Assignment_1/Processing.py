from ipwhois import IPWhois
import ipaddress
import pandas as pd
import re
import numpy as np
import csv


def cidr_to_range(cidr):
    '''
    Input : CIDR (string) 
    Output :
        (
            IP range start : string
            IP range end   : string
        )
    '''
    if(cidr == 'N/A'):
        return '', ''
    ip_network = ipaddress.ip_network(cidr, strict=False)
    return ip_network.network_address, ip_network.broadcast_address # start and end IP addresses for given CIDR


def get_ip_info(ip_address):
    '''
    Input : ip_address (string) 
    Output :
        (
            IP range          : string [] or  NA
            ASN               : int or NA
            Geolocation       : string (Country code) or NA
            Organisation Name : string  or NA
        )
        or None
    '''
    # some of the IP addresses can be private and some IP addresses will don't  have ASN listing. In these cases, this part of code raises exception, so, by using try catch we can ignore those IP's  
    try:
        ip = IPWhois(ip_address)
        result = ip.lookup_whois() # whois lookup for given IP

        # to convert from CIDR range to normal (by default IP range is in CIDR format)
        ip_range = [str(i)
                    for i in cidr_to_range(result.get('asn_cidr', 'N/A'))]
        as_number = result.get('asn', 'N/A')
        geolocation = result.get('asn_country_code', 'N/A')
        as_name = result.get('asn_description', 'N/A')
        return ip_range, as_number, geolocation, as_name
    except Exception as e:
        # for IPs where we can't get info or no ASN listing from whois 
        return None
    

def getData(pattern,hopinfo):
    ip_range, as_number, geolocation, as_name = get_ip_info(pattern) 
    match_latencies = re.findall(
                            r'[0-9\.]+ ms', hopinfo) # get latency from each hop data in ms
    latency = float(re.findall(
                            r'[0-9\.]+', match_latencies[0])[0]) # filtering above latency to get number only
    a = {"sno": rownum, "ip_address": pattern, "ip_range": f"{ip_range[0]}-{ip_range[1]}", "as_number": as_number,"geolocation": geolocation, "as_name": as_name, "latency": latency}

    return a


df = np.array(pd.read_excel('./Raw_data.xlsx')) # Read Raw_data file and process the raw data
info = [] # stores processed data for all hops for all source and destination combinations

for row in df: 
    # row represents source-destination combination
    rownum = row[0]
    lines = row[5].splitlines() # traceroute raw data for given source and destination
    ignore = 0
    for index, i in enumerate(lines): # looping through each hop 
        hopinfo = i.strip(' ') # removing any whitespaces before to get clean unprocessed each hop info
        if(len(hopinfo) >= 2):
            try:
                x1 = hopinfo.split(" ")
                sno = int(x1[0]) 
                if(sno == index+1-ignore):
                    pattern = re.findall(
                        r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', hopinfo) # finds IP patterns for each hop
                    if pattern and get_ip_info(pattern[0]): # checking whether there is any IP in that hop info(as we have hop giving all * s)
                        a = getData(pattern[0],hopinfo)
                        info.append(a)
                    else:
                        for i in range(0, 2):
                            # if in one iteration we cannot extract IP due to *s then as traceroute tries 3 times we will consider another two trials at  each hop
                            if(index+1+i < len(lines)):
                                p = lines[index+i+1].strip(' ')
                                x1 = p.split(" ")
                                if(not x1[0].isnumeric()):
                                    pattern = re.findall(
                                        r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', p)
                                    if pattern and get_ip_info(pattern[0]):
                                        a = getData(pattern[0],p)
                                        info.append(a)
                                        break
                                else:
                                    break
                            else:
                                break
                else:
                    ignore += 1
            except Exception as e:
                ignore += 1


with open("Processed_data.csv", 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
                            "sno", "ip_address", "ip_range", "as_number", "geolocation", "as_name", "latency"])
    writer.writeheader()
    writer.writerows(info)

