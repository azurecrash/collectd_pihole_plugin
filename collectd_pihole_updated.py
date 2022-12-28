#UPDATED FOR PYTHON3 AND THE NEW PIHOLE API AUTH AS OF DEC 2022

import collectd
import json
import urllib.request
import sys

IP_PIHOLE = 'PUT_YOUR_IP_HERE'
API_TOKEN = 'PUT_YOUR_API_KEY_HERE'

def config_func(config):
    path_set = False

    for node in config.children:
        key = node.key.lower()
        val = node.values[0]

        if key == 'ip':
            global IP_PIHOLE
            IP_PIHOLE = val
            path_set = True
        else:
            collectd.info('IP-Pihole plugin: Unknown config key "%s"' % key)

    if path_set:
        collectd.info('IP-Pihole plugin: Using overridden ip %s' % IP_PIHOLE)
    else:
        collectd.info('IP-Pihole plugin: Using default ip %s' % IP_PIHOLE)

def request_summary():

    req = urllib.request.urlopen("http://"+IP_PIHOLE+"/admin/api.php?summaryRaw&auth="+API_TOKEN)
    req_body = req.read()
    output = json.loads(req_body.decode("utf-8"))

    return output

def dispatch_summary(output):

    dnstotal = (output['dns_queries_today'])
    dnsblocked = (output['ads_blocked_today'])
    domainsblocked = (output['domains_being_blocked'])
    percentage = (output['ads_percentage_today'])
    queriesForwarded = (output['queries_forwarded'])
    queriesCached = (output['queries_cached'])

    v_tot = collectd.Values(plugin='pihole', type='gauge', type_instance='dns_queries_today')
    v_tot.dispatch(values=[dnstotal])

    v_ad = collectd.Values(plugin='pihole', type='gauge', type_instance='ads_blocked_today')
    v_ad.dispatch(values=[dnsblocked])

    v_blocked = collectd.Values(plugin='pihole', type='gauge', type_instance='domains_being_blocked')
    v_blocked.dispatch(values=[domainsblocked])

    v_perc = collectd.Values(plugin='pihole', type='gauge', type_instance='ads_percentage_today')
    v_perc.dispatch(values=[percentage])

    v_cach = collectd.Values(plugin='pihole', type='gauge', type_instance='queries_cached')
    v_cach.dispatch(values=[queriesCached])
    
    v_for = collectd.Values(plugin='pihole', type='gauge', type_instance='queries_forwarded')
    v_for.dispatch(values=[queriesForwarded])

def read_func(): 
    summary = request_summary()
    dispatch_summary(summary)

collectd.register_config(config_func)
collectd.register_read(read_func)
