from django.db import models
from client.models import Requisition 
from account.models import CustomUser, Department 

class DepartmentApproval(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    approval_status = models.CharField(max_length=20, choices=[("APPROVED", "Approved"), ("REJECTED", "Rejected")])
    comments = models.TextField()
    approved_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Department Approval"
        verbose_name_plural = "Department Approvals"
