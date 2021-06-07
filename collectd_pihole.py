import collectd
import json
import urllib2
import sys

IP_PIHOLE = '192.168.0.168'


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
    req = urllib2.Request("http://"+IP_PIHOLE+"/admin/api.php")
    opener = urllib2.build_opener()
    f = opener.open(req)
    output = json.load(f)
    return output

def dispatch_summary(output):
    dnstotal = output[u'dns_queries_today']
    dnsblocked = output[u'ads_blocked_today']
    domainsblocked = output[u'domains_being_blocked']
    percentage = output[u'ads_percentage_today']
    queriesForwarded = output[u'queries_forwarded']
    queriesCached = output[u'queries_cached']

    v_tot = collectd.Values(plugin='pihole', type='dns_queries_today', type_instance='dns_queries_today')
    v_tot.dispatch(values=[dnstotal])

    v_ad = collectd.Values(plugin='pihole', type='ads_blocked_today', type_instance='ads_blocked_today')
    v_ad.dispatch(values=[dnsblocked])

    v_blocked = collectd.Values(plugin='pihole', type='domains_being_blocked', type_instance='domains_being_blocked')
    v_blocked.dispatch(values=[domainsblocked])

    v_perc = collectd.Values(plugin='pihole', type='ads_percentage_today', type_instance='ads_percentage_today')
    v_perc.dispatch(values=[percentage])

    v_cach = collectd.Values(plugin='pihole', type='queries_cached', type_instance='queries_cached')
    v_cach.dispatch(values=[queriesCached])

    v_for = collectd.Values(plugin='pihole', type='queries_forwarded', type_instance='queries_forwarded')
    v_for.dispatch(values=[queriesForwarded])

def read_func():
    summary = request_summary()
    dispatch_summary(summary)

collectd.register_config(config_func)
collectd.register_read(read_func)