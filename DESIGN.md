# Part 2 — Low Level System Design

## Class/Module Design
- **EmployeeService**
  - add_employee()
  - get_employee()

- **LeaveService**
  - apply_leave()
  - approve_leave()
  - reject_leave()

---

## Pseudocode for Leave Approval Logic

```python
function approve_leave(request_id, approver_id):
    request = get_leave_request(request_id)
    if request.status != "Pending":
        return "Already processed"

    if approver_has_permission(approver_id):
        request.status = "Approved"
        update_leave_balance(request.employee_id)
        return "Leave Approved"
    else:
        return "Permission Denied"
