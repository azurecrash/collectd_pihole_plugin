#Collectc Pihole Pyhton Plugin
This litte plugin takes the summary request of Pihole and makes it available via Collectd. To check the request you can test it via http://192.168.0.2/admin/api.php where the ip is the piholes web interface
##Config
Copy the desired files to your target system. In this example the python plugin is saved under `/opt/collectd_plugins` and the types db under `/usr/share/collectd/`
Afterwards make following changes to the `collectd.conf`
- Add Types-Db
`TypesDB "/usr/share/collectd/types.db" "/usr/share/collectd/pihole_types.db"
- Load Python Plugin
`LoadPlugin python

<Plugin python>
    ModulePath "/opt/collectd_plugins"
    Import "collectd_pihole"
    <Module collectd_pihole>
        ip "192.168.0.2"
    </Module>
</Plugin>`
Make sure to change the ip to adress of the pihole web interface.
##License
MIT License, see LICENSE file.