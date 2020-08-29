from tls_conf.admin.session_ticket_key import *
from tls_conf.admin.server_cert_conf import *
from tls_conf.admin.tls_rule_conf import *

admin.site.register(tls_rule_conf.TLSRule, TLSRuleAdmin)
admin.site.register(tls_rule_conf.TLSRuleData, TLSRuleDataAdmin)
admin.site.register(session_ticket_key.SessionTicketKey, SessionTicketKeyAdmin)
admin.site.register(server_cert_conf.Cert, CertAdmin)
admin.site.register(server_cert_conf.CertData, CertDataAdmin)
