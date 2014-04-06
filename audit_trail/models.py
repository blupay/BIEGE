from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class AuditTrail(models.Model):
	AUDIT_TYPES = [(0, 'Admin'), (1, 'Public')]
    	AUDIT_ACTIONS = [(0, 'Modified'), (1, 'Created'), (2, 'Deleted')]
    	object_id = models.PositiveIntegerField(null=True)
    	#Audit Info
   	name = models.CharField(max_length=100, blank=True, null=True)
    	type = models.SmallIntegerField(choices=AUDIT_TYPES, db_index=True)
    	action = models.SmallIntegerField(choices=AUDIT_ACTIONS)
    	audit_on = models.DateField()
    	modified_by = models.ForeignKey(User, null=True)
    	
    	class Meta:
        	ordering = ['-audit_on']
        	
        def __unicode__(self):
              return "%s" %(self.name)
            
admin.site.register(AuditTrail)



