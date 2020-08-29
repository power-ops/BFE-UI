from django.contrib import admin
from server_data_conf.admin import cluster_conf, host_rule, name_conf, route_rule, vip_rule
import server_data_conf.models as server_data_conf

admin.site.register(server_data_conf.cluster_conf.ClusterConfig, cluster_conf.ClusterConfigAdmin)
admin.site.register(server_data_conf.cluster_conf.ClusterConfigData, cluster_conf.ClusterConfigDataAdmin)
admin.site.register(server_data_conf.route_rule.RouteRule, route_rule.RouteRuleAdmin)
admin.site.register(server_data_conf.route_rule.RouteRuleData, route_rule.RouteRuleDataAdmin)
admin.site.register(server_data_conf.host_rule.HostTag, host_rule.HostTagAdmin)
admin.site.register(server_data_conf.host_rule.HostProduct, host_rule.HostProductAdmin)
admin.site.register(server_data_conf.host_rule.HostRuleData, host_rule.HostRuleDataAdmin)
admin.site.register(server_data_conf.name_conf.NameConfig, name_conf.NameConfigAdmin)
admin.site.register(server_data_conf.name_conf.NameConfigData, name_conf.NameConfigDataAdmin)
admin.site.register(server_data_conf.vip_rule.VipRule, vip_rule.VipRuleAdmin)
admin.site.register(server_data_conf.vip_rule.VipRuleData, vip_rule.VipRuleDataAdmin)
